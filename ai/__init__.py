import os
import logging
import pandas as pd
import numpy as np
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from ai.quote_selector import Quote, QuoteSelector
from typing import List, Tuple


logging.basicConfig(level=logging.INFO)

logging.info(msg='Loading sentence transformer embeddings model')
embedding_function = SentenceTransformerEmbeddings(
    model_name="all-MiniLM-L6-v2")
logging.info(
    msg='Finished loading sentence transformers embeddings model')


def load_quote_examples(folder: str, date_filename: str) -> Tuple[List[Quote], np.ndarray]:
    data_filepath = os.path.join(folder, date_filename)
    logging.info(msg=f'Loading quotes csv from {data_filepath}')

    quote_df = pd.read_csv(data_filepath)
    quote_examples: List[Quote] = quote_df.to_dict(orient='records')
    logging.info(msg=f'Done loading quotes csv from {data_filepath}')

    quote_df['category'] = quote_df['category'].str.split(',')
    category_df_exploded = quote_df.explode('category')
    quote_categories = category_df_exploded['category'].unique()

    return quote_examples, quote_categories


def get_quotes(data_folder: str, data_filename: str, collection_name: str, persist_directory: str, k: int) -> Tuple[QuoteSelector, np.ndarray]:
    quote_examples, quote_categories = load_quote_examples(
        data_folder, data_filename)

    quote_selector = QuoteSelector(
        examples=quote_examples,
        collection_name=collection_name,
        persist_directory=persist_directory,
        k=k,
        embedding_function=embedding_function
    )

    if not os.path.exists(f'./{persist_directory}'):
        logging.info(
            msg=f'Saving quotes and their meta to ChromaDB vector storage in the folder: {persist_directory}')
        quote_selector.save_examples()
        logging.info(
            msg=f'Finished saving quotes and their metadata to ChromaDB vector storage in the folder: \
                {persist_directory}')

    logging.info(msg='Quote Selector is now finished initializing')

    return quote_selector, quote_categories
