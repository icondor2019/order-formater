from sentence_transformers import SentenceTransformer
# from loguru import logger


def embedding_text(text_list: list) -> list:
    model = SentenceTransformer('intfloat/e5-base-v2')  # TODO probar el destile BERT
    input_texts = text_list
    embeddings = model.encode(input_texts, normalize_embeddings=True)
    return embeddings
