CREATE_SELLER_QUERY = """
    INSERT INTO `sellers` (uuid, user_id, name, created_at, status)
    VALUES (:uuid, :user_id, :name, :created_at, :status);
"""
UPDATE_SELLER_DATA_QUERY = """
    UPDATE `sellers`
    SET
        status = :status,
        name = :name
    WHERE user_id = :user_id;
"""
GET_SELLER_QUERY = """
    SELECT *
    FROM sellers
    WHERE user_id = :user_id
"""

UPDATE_SELLER_OFFER_QUERY = ""
