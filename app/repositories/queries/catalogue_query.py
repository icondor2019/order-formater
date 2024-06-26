CREATE_PRODUCT_QUERY = """
    INSERT INTO `catalogue` (uuid, name, size, color, stems, package, description, embedding)
    VALUES (:uuid, :name, :size, :color, :stems, :package, :description, JSON_ARRAY_PACK(:embedding))
"""
VECTOR_SEARCH_QUERY = """
select uuid, description, dot_product(embedding, JSON_ARRAY_PACK(:embedding)) as score
from catalogue
order by score desc
limit 1
"""
