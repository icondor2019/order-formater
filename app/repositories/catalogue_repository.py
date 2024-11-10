from loguru import logger
from sqlalchemy import text
from configuration.database import db
from sqlalchemy.exc import SQLAlchemyError
from responses.catalogue_response import CatalogueResponse
from repositories.queries.catalogue_query import (
    CREATE_PRODUCT_QUERY,
    VECTOR_SEARCH_QUERY,
    GET_PRODUCT_QUERY
)


class CatalogueRepository:
    """Manage Catalogue records & embeddings"""

    def add_new_product(self, product_record: CatalogueResponse):
        try:
            params = product_record.model_copy().model_dump()
            db.execute(text(CREATE_PRODUCT_QUERY), params)
            db.commit()
            logger.debug(f"New product created. uuid: {params['uuid']}")
        except SQLAlchemyError as ex:
            db.rollback()
            logger.error(f"Error saving seller. uuid {params['uuid']}. Error: {ex}")

    def get_similar_product(self, vector: str):
        logger.debug(VECTOR_SEARCH_QUERY)
        result = None
        try:
            params = {'embedding': vector}
            result = db.execute(text(VECTOR_SEARCH_QUERY), params).fetchone()
            logger.debug(result)
            db.commit()
        except SQLAlchemyError as ex:
            db.rollback()
            logger.error(f"Error consulting vecto. Error: {ex}")
        return result

    def get_product(self, product_uuid: str):
        result = None
        try:
            params = {'product_uuid': product_uuid}
            result = db.execute(text(GET_PRODUCT_QUERY), params).fetchone()
            logger.debug(result)
            db.commit()
        except SQLAlchemyError as ex:
            db.rollback()
            logger.error(f"Error consulting vecto. Error: {ex}")
        return result
