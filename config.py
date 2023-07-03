import dotenv
import os
import logging
import pandas as pd
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from quote_llm import QuoteLLM
from quote_selector import Quote, QuoteSelector
from typing import List

logging.basicConfig(level=logging.INFO)
dotenv.load_dotenv()

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
OPENAI_MODEL_NAME = os.environ['OPENAI_MODEL_NAME']
OPENAI_MODEL_TEMPERATURE = float(os.environ['OPENAI_MODEL_TEMPERATURE'])
RAW_DATA_FOLDER_NAME = os.environ['RAW_DATA_FOLDERNAME']
RAW_DATA_FILENAME = os.environ['RAW_DATA_FILENAME']
VECTORDB_COLLECTION_NAME = os.environ['VECTORDB_COLLECTION_NAME']
VECTORDB_PERSIST_FOLDERNAME = os.environ['VECTORDB_PERSIST_FOLDERNAME']
NUMBER_OF_SIMILARITY_RESULTS = int(os.environ['NUMBER_OF_SIMILARITY_RESULTS'])

quote_csv_path = os.path.join(RAW_DATA_FOLDER_NAME, RAW_DATA_FILENAME)
logging.info(msg=f'Loading quotes csv from {quote_csv_path}')
quote_df = pd.read_csv(quote_csv_path)
quote_examples: List[Quote] = quote_df.to_dict(orient='records')
logging.info(msg=f'Done loading quotes csv from {quote_csv_path}')

quote_df['category'] = quote_df['category'].str.split(',')
category_df_exploded = quote_df.explode('category')
quote_categories = category_df_exploded['category'].unique()

logging.info(msg='Loading sentence transformer embeddings model')
embedding_function = SentenceTransformerEmbeddings(
    model_name="all-MiniLM-L6-v2")
logging.info(
    msg='Finished loading sentence transformers embeddings model')

quote_selector = QuoteSelector(
    examples=quote_examples,
    collection_name=VECTORDB_COLLECTION_NAME,
    persist_directory=VECTORDB_PERSIST_FOLDERNAME,
    k=NUMBER_OF_SIMILARITY_RESULTS,
    embedding_function=embedding_function
)

if not os.path.exists(f'./{VECTORDB_PERSIST_FOLDERNAME}'):
    logging.info(
        msg=f'Saving quotes and their meta to ChromaDB vector storage in the folder: {VECTORDB_PERSIST_FOLDERNAME}')
    quote_selector.save_examples()
    logging.info(
        msg=f'Finished saving quotes and their metadata to ChromaDB vector storage in the folder: \
              {VECTORDB_PERSIST_FOLDERNAME}')

logging.info(msg='Quote Selector is now finished initializing')


quote_llm = QuoteLLM(api_key=OPENAI_API_KEY,
                     model_name=OPENAI_MODEL_NAME,
                     model_temperature=OPENAI_MODEL_TEMPERATURE,
                     quote_selector=quote_selector,
                     quote_categories=quote_categories)
