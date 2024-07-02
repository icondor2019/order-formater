from loguru import logger
from sqlalchemy import text
import json
from typing import Optional
from configuration.database import db
from sqlalchemy.exc import SQLAlchemyError
from responses.seller_response import SellerResponse
from repositories.queries.seller_query import (
    CREATE_SELLER_QUERY,
    UPDATE_SELLER_DATA_QUERY,
    UPDATE_SELLER_OFFER_QUERY,
    GET_SELLER_QUERY
    )


class SellerRepository:
    """Manage seller's records"""

    def create_seller(self, client_record: SellerResponse):
        try:
            params = client_record.model_copy().model_dump()
            db.execute(text(CREATE_SELLER_QUERY), params)
            db.commit()
            logger.debug(f"New seller created. user_id {params['user_id']}")
        except SQLAlchemyError as ex:
            db.rollback()
            logger.error(f"Error saving seller. user_id {params['user_id']}. Error: {ex}")

    def update_seller_data(self, seller_response: SellerResponse):
        try:
            params = seller_response.model_copy().model_dump()
            logger.debug(params)
            db.execute(text(UPDATE_SELLER_DATA_QUERY), params)
            db.commit()
            logger.debug(f"Seller status updated. user_id: {seller_response.user_id}")
        except SQLAlchemyError as ex:
            db.rollback()
            logger.error(f"Error updating Seller status. user_id: {seller_response.user_id}. Error:{ex}")

    def get_seller_record(self, user_id: int):
        seller_record = None
        params = {'user_id': user_id}
        try:
            result = db.execute(text(GET_SELLER_QUERY), params).fetchone()
            
            if result:
                logger.debug(result[0])
                logger.debug(result.user_id)
                logger.debug(f"name: {result.name}")
                seller_record = SellerResponse(
                    uuid=result.uuid,
                    user_id=result.user_id,
                    name=result.name,
                    status=result.status,
                    )
        except SQLAlchemyError as ex:
            logger.error(f"Error getting seller record. user_id: {user_id}. Error: {ex}")
        return seller_record

    def update_seller_offer_query():
        pass
