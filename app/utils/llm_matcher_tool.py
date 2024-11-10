from langchain.prompts import ChatPromptTemplate
# from langchain.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from utils.embedding_tool import embedding_text
from configuration.settings import settings
from repositories.catalogue_repository import CatalogueRepository
from repositories.product_repository import ProductRepository
from responses.product_response import ProductResponse
from loguru import logger
from uuid import uuid4
import pandas as pd
# import numpy as np
import json


class LlmMatcher:
    def __init__(self) -> None:
        self.llm = GoogleGenerativeAI(
            model="gemini-pro",
            temperature=0.5,
            top_p=0.8,
            top_k=40,
            google_api_key=settings.GEMINI_API_KEY)
        self.__catalogue_repository = CatalogueRepository()
        self.__product_repository = ProductRepository()

        self.template = """
            Vas a recibir un raw_text de varias filas. Puedes basarte en el ejemplo_1.
            Dentro de las filas vas a recibir productos que corresponden a rosas de distintos tipos.
            Entre la información de cada producto vas a encontra un precio en dolares, regularmente con centavos,
            que representan el valor por tallo de rosa.
            Además, en la información vas a encontrar la cantidad de cajas disponibles.
            Puedes identificar la cantidad de cajas por que contienen las siglas HB (half box).
            La cantidad disponible de cajas por lo regular está al principio de cada producto.

            Debes devolver en una lista de diccionarios. Cada diccionario corresponde a cada producto de raw_text.
            Los campos o key de cada diccionario son:
            "product": "toda la fila del producto excluyendo la cantidad de cajas y el precio"
            "quantity": "la cantidad de cajas como tipo int"
            "price": "el precio como typo float"

            Si no tienes suficiente información del precio o la cantidad de cajas, puedes dejar cualquiera de los dos campos como None.

            Ejemplo_1:
            "hola muchos gusto este es mi disponible
            2HB Magic Lips 40cm x 400 0.25
            3HB Magic Lips 60cm x 300st 0.50
            10 Freedom 50cm red 0.4
            Espero poder hacer negocio contigo
            "
            Resultado_ejemplo_1:
            [
            {{"product": "Magic Lips 40cm x 400", "quantity": 2, "price": 0.25}},
            {{"product": "Magic Lips 60cm x 300st", "quantity": 3, "price": 0.5}},
            {{"product": "Freedom 50cm red", "quantity": 10, "price": 0.4}}
            ]

            raw_text:
            {raw_text}

            Answer:
            """

    def llm_format_raw_availability(self, raw_text):
        prompt = ChatPromptTemplate.from_template(template=self.template)
        messages = prompt.format_messages(raw_text=raw_text)
        raw_response = self.llm.invoke(messages)
        offer_list = json.loads(raw_response)
        df = pd.DataFrame(offer_list)
        return df

    def create_product_embedding(self, raw_product_lst):
        raw_emb_array = embedding_text(raw_product_lst)
        return raw_emb_array.tolist()

    def match_seller_product(self, raw_df):
        match_lst = []
        for vector in raw_df['embedding']:
            match_product = self.__catalogue_repository.get_similar_product(vector)
            match_lst.append(match_product)
        raw_result = pd.DataFrame(match_lst)
        df = pd.concat([raw_df.reset_index(drop=True), raw_result.reset_index(drop=True)], axis=1)
        return df

    def save_seller_product_in_db(self, seller_uuid, df):
        for idx, row in df.iterrows():
            record = ProductResponse(
                uuid=str(uuid4()),
                seller_uuid=str(seller_uuid),
                product_uuid=str(row['uuid']),
                raw_description=row['description'],
                stock=row['quantity'],
                price=row['price']
            )
            # logger.debug(record)
            self.__product_repository.add_new_seller_product(record)

    def process_raw_availability(self, seller_uuid, raw_text):
        logger.debug('formating raw_test with llm...')
        raw_df = self.llm_format_raw_availability(raw_text)
        logger.debug(raw_df)

        raw_product_list = raw_df['product'].tolist()
        embedding_product_list = self.create_product_embedding(raw_product_list)
        raw_df['embedding'] = embedding_product_list
        raw_df['embedding'] = raw_df['embedding'].astype(str)
        logger.debug('products embedding created...')
        # raw_df.to_csv('llm_raw_df.csv', index=False)
        # raw_df = pd.read_csv('llm_raw_df.csv')

        df = self.match_seller_product(raw_df=raw_df)
        # df.to_csv('llm_final_df.csv', index=False)
        # df = pd.read_csv('llm_final_df.csv')
        self.__product_repository.deactivate_seller_products(seller_uuid=seller_uuid)
        self.save_seller_product_in_db(seller_uuid, df)
        return len(raw_product_list)
