import sys
import ai
from config import *
from social_media.instagram import InstagramPoster
from ai.quote_llm import QuoteLLM
from ai.quote_image import QuoteImageGenerator


def main(platform_name: str):
    quote_selector, quote_categories = ai.get_quotes(data_folder=RAW_DATA_FOLDER_NAME,
                                                     data_filename=RAW_DATA_FILENAME,
                                                     collection_name=VECTORDB_COLLECTION_NAME,
                                                     persist_directory=VECTORDB_PERSIST_FOLDERNAME,
                                                     k=NUMBER_OF_SIMILARITY_RESULTS)
    quote_llm = QuoteLLM(
        api_key=OPENAI_API_KEY,
        model_name=OPENAI_MODEL_NAME,
        model_temperature=OPENAI_MODEL_TEMPERATURE,
        quote_selector=quote_selector,
        quote_categories=quote_categories
    )

    quote_image_generator = QuoteImageGenerator(
        api_key=STABILITY_API_KEY,
        engine=IMAGE_ENGINE,
        verbose=True,
        width=IMAGE_WIDTH,
        height=IMAGE_HEIGHT,
        image_save_folder=AI_IMAGES_SAVE_DIRECTORY
    )

    # generate the quote prompt template, and run the chain against the OpenAI API
    quote_llm.generate_prompt_template()
    quote_llm.run_chain()

    # generate the image with the StabilityAI API (text2img diffusion model)
    image_prompt = f'Create a highly quality, evocative illustration with no text, portraying the following quote: {quote_llm.quote_result}'
    quote_image_generator.generate_image(image_prompt)
    image_destination = quote_image_generator.save_image()

    poster = None
    if platform_name == 'instagram':
        poster = InstagramPoster(
            INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD, headless=True, no_sandbox=True)
        poster.login()
        poster.post_content(image_destination, quote_llm.quote_result)


if __name__ == '__main__':
    main(sys.argv[1])
