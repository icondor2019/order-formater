
import re
import requests
import pandas as pd
from uuid import uuid4
from loguru import logger
from bs4 import BeautifulSoup as bs
from utils.embedding_tool import embedding_text
from responses.catalogue_response import CatalogueResponse
from repositories.catalogue_repository import CatalogueRepository


class ScrapingCatalogue:
    def __init__(self) -> None:
        self.url = 'https://eagle-linkflowers.com/flower/roses/premium-roses/'
        self.headers_ = {'User-Agent':
                         'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
                         }
        self.session = requests.session()
        self.stem_qty = {40: 400, 50: 350, 60: 300, 70: 150, 80: 150}
        self.__catalogue_repository = CatalogueRepository()

    def get_product_grid(self):
        res = self.session.get(self.url, headers=self.headers_)
        soup = bs(res.content, 'html.parser')

        # Get the grid with the target products
        __grid = soup.find('div', {'id': 'mf-shop-content'})
        ul = __grid.find('ul')
        li_list = ul.find_all('a')
        raw_url_list = []
        for a in li_list:
            prod_url = a.get('href')
            raw_url_list.append(prod_url)
        base_url_list = list(set(raw_url_list))
        return base_url_list

    @staticmethod
    def clean_number(raw_number):
        return int(re.sub("[^0-9]", "", raw_number))

    @staticmethod
    def clean_name(texto):
        partes = texto.split("–")
        return partes[0].strip()

    @staticmethod
    def concatenate_columns(row):
        return row['package'] + ' ' + row['name'] + ' ' + str(row['size']) + 'cm x ' + str(row['stems']) + ' stems' + ' ' + row['color']

    def request_products(self, base_url_list: list):
        prod_list = []

        for url_product in base_url_list[15:]:
            res = self.session.get(url_product, headers=self.headers_)
            soup = bs(res.content, 'html.parser')
            prod_details = {}
            try:
                raw_name = soup.find('h1', {'class': 'product_title entry-title'}).text
            except:
                raw_name = 'no visible name'

            prod_details['name'] = self.clean_name(raw_name)
            size_list = []

            try:
                div_sizes = soup.find('div', {'class': 'tawcvs-swatches'})
                span_list = div_sizes.find_all('span')
                for span in span_list:
                    size = span.text
                    size_list.append(self.clean_number(size))
            except:
                print('no size')

            prod_details['sizes'] = size_list
            try:
                tr_color = soup.find('tr', {'class': 'woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_color'})
                color = tr_color.find('td').text
            except:
                color = 'no visible color'
            prod_details['color'] = color.strip()
            prod_details['url'] = url_product
            rows = [{'name': prod_details['name'], 'size': size, 'color': prod_details['color'], 'url': prod_details['url']} for size in prod_details['sizes']]
            prod_list.append(rows)

        return prod_list

    def format_result(self, prod_list: list):
        flattened_data = [item for sublist in prod_list for item in sublist]
        df = pd.DataFrame(flattened_data)
        df['product_uuid'] = [str(uuid4()) for i in range(len(df))]
        df['stems'] = df['size'].map(self.stem_qty)
        df['package'] = 'HB'
        df['description'] = df.apply(self.concatenate_columns, axis=1)
        return df

    def generate_product_embedding(self, df):
        test_lst = df['description'].tolist()
        emb_lst = embedding_text(test_lst)
        df['embedding'] = emb_lst.tolist()
        return df

    def save_product_in_catalogue(self, df):
        output = df.to_dict(orient='records')
        for product in output:
            catalogue_response = CatalogueResponse(**product)
            self.__catalogue_repository.add_new_product(catalogue_response)

    def main(self):
        base_url_list = self.get_product_grid()
        raw_product_list = self.request_products(base_url_list)
        products = self.format_result(raw_product_list)
        products_embedding = self.generate_product_embedding(products)
        self.save_product_in_catalogue(products_embedding)
        logger.debug("Scraping process finished...")
