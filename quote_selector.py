from langchain.prompts.example_selector.base import BaseExampleSelector
from langchain.schema import Document
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
from typing import Dict, List, TypedDict

class Quote(TypedDict):
    category: str
    quote: str


class QuoteSelector(BaseExampleSelector):

    def __init__(self,
                 examples: List[Quote],
                 collection_name: str,
                 persist_directory: str,
                 k: int,
                 embedding_function: SentenceTransformerEmbeddings):

        self.embedding_function = embedding_function
        self.k = k
        self.examples = examples
        self.vectordb = Chroma(collection_name=collection_name,
                               persist_directory=persist_directory,
                               embedding_function=embedding_function)

    def add_example(self, example: Quote):
        self.examples.append(example)

    def select_examples(self, input_variables: Dict[str, str]) -> List[Quote]:
        try:
            categories = set(input_variables['categories'])
            return [example for example in self.examples if set(example['category'].split(',')).intersection(categories)]
        except KeyError:
            return []

    def find_most_similar_quotes(self, quote_query: str) -> List[Document]:
        matching_quote_documents = self.vectordb.similarity_search(
            query=quote_query,
            k=self.k)
        return matching_quote_documents

    def save_examples(self) -> None:
        documents = [Document(page_content=example['quote'],
                              metadata={'category': example['category']}) for example in self.examples]
        self.vectordb.add_documents(documents=documents)
        self.vectordb.persist()
