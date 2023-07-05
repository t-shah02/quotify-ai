import numpy as np
from langchain.llms import OpenAI
from langchain import PromptTemplate, LLMChain
from langchain.schema import Document
from ai.quote_selector import QuoteSelector
from typing import List, Dict


class PromptTemplateEmpty(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class PromptInputsEmpty(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class QuoteLLM:

    MIN_QUOTE_CATEGORIES = 1
    MAX_QUOTE_CATEGORIES = 3

    def __init__(self, api_key: str, model_name: str, model_temperature: float,
                 quote_selector: QuoteSelector, quote_categories: np.ndarray[np.str_]):
        self.llm = OpenAI(openai_api_key=api_key,
                          model=model_name,
                          temperature=model_temperature)
        self.quote_selector = quote_selector
        self.quote_categories = quote_categories
        self.prompt_inputs: None | Dict[str, str] = None
        self.prompt_template: None | PromptTemplate = None
        self.quote_result: None | str = None

    def generate_prompt_template(self) -> None:
        num_quote_categories = np.random.randint(
            QuoteLLM.MIN_QUOTE_CATEGORIES, QuoteLLM.MAX_QUOTE_CATEGORIES)
        categories_to_use: np.ndarray[np.str_] = np.random.choice(
            self.quote_categories, size=num_quote_categories)

        quote_corpus: Dict[str, List[Document]] = {}

        for category in categories_to_use:
            category_matches = self.quote_selector.find_most_similar_quotes(
                category)
            quote_corpus[category] = category_matches

        final_quotes: List[str] = [np.random.choice(
            quote_documents).page_content for quote_documents in quote_corpus.values()]
        final_quotes_str = '\n'.join(final_quotes)

        category_vars = [f'category{i}' for i in range(num_quote_categories)]
        category_vars_formatted = [
            f'{{{category_var}}}' for category_var in category_vars]
        category_str = ', '.join(
            category_vars_formatted[0:-1]) + f' and {category_vars_formatted[-1]}' if len(category_vars_formatted) > 1 else \
            category_vars_formatted[0]

        template = f'Write a creative, expressive quote with the following themes in mind: {category_str} \n Feel free to use sample quotes relating to those categories as inspiration in the new quote: \n {final_quotes_str}'

        self.prompt_template = PromptTemplate(
            input_variables=category_vars,
            template=template
        )
        self.prompt_inputs = {category_var: selected_quote_category for category_var,
                              selected_quote_category in zip(category_vars, quote_corpus.keys())}

    def run_chain(self) -> None:
        if self.prompt_template is None:
            raise PromptTemplateEmpty(
                'The prompt template for this quote llm is empty, please generate it first!')

        if self.prompt_inputs is None:
            raise PromptInputsEmpty(
                'The prompt inputs for this quote llm is empty, please generate the prompt template first!')

        llm_chain = LLMChain(llm=self.llm, prompt=self.prompt_template)
        result = llm_chain.run(self.prompt_inputs)

        self.quote_result = result
