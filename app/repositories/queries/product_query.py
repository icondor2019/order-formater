CREATE_SELLER_PRODUCT_QUERY = """
    INSERT INTO `products` (uuid, seller_uuid, product_uuid, raw_description, stock, price, status)
    VALUES (:uuid, :seller_uuid, :product_uuid, :raw_description, :stock, :price, :status)
"""

DEACTIVATE_SELLER_PRODUCTS_QUERY = """
    UPDATE `products`
    SET
        status = 'inactive'
    WHERE seller_uuid = :seller_uuid
    AND status = 'active'
"""

GET_ALL_SELLER_ACTIVE_PRODUCTS_QUERY = """
    SELECT
        raw_description,
        stock,
        price
    FROM products
    WHERE seller_uuid = :seller_uuid
    AND status = 'active';
"""
