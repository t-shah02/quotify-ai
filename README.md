# Quotify-AI
This is an AI-powered quote generator bot that can post transformative quotes, along with beautiful illustrations on various social media platforms. It was trained on a dataset of around 30k quotes, grouped by various category names. To generate content, it picks 1-3 random categories from that dataset and then uses a vector database (where the quote dataset content was vectorized), to find the closest matches. After finding the matches, it passes those categories and quotes to an LLM API (OpenAI), using a basic Langchain prompt template, to generate a new foreign quote with the inspiration of that data. Once the quote has been generated, an additional call is made to the Stability AI API, and uses the popular tx2img model called, **Stable Diffusion**. 

The bot currently only posts on Instagram, but I plan to add more social media platforms in the future.
- Instagram (supported)
- Reddit (not supported)
- Facebook (not supported)
- Twitter (not supported)

# Runing the project locally
Cloning the repository:
```bash
git clone https://github.com/t-shah02/quotify-ai.git
cd [project-directory]
```
Creating a Python virtual environment:
```bash
python -m venv venv
```
Installing project dependencies:
```bash
pip install -r requirements.txt
```
Setting up environment variables:
```bash
touch .env
```
Template for .env:
```
OPENAI_API_KEY=[your OpenAI API key]
STABILITY_API_KEY=[your StabilityAI API key]
STABILITY_HOST=grpc.stability.ai:443
OPENAI_MODEL_NAME=text-ada-001	
OPENAI_MODEL_TEMPERATURE=0.7
RAW_DATA_FILENAME=quotes.csv
RAW_DATA_FOLDERNAME=data
VECTORDB_COLLECTION_NAME=quotes
VECTORDB_PERSIST_FOLDERNAME=quotedb
NUMBER_OF_SIMILARITY_RESULTS=3
AI_IMAGES_SAVE_DIRECTORY=images
IMAGE_WIDTH=704
IMAGE_HEIGHT=704
IMAGE_ENGINE=stable-diffusion-xl-1024-v0-9
INSTAGRAM_USERNAME=[your Instagram username]
INSTAGRAM_PASSWORD=[your Instagram password]
```

Running the script:
```bash
python main.py [social-media-name]
```
Example:
```bash
python main.py instagram
```

# Resources
- https://platform.stability.ai/docs/features
- https://platform.openai.com/docs/api-reference
- https://www.kaggle.com/datasets/akmittal/quotes-dataset
- https://docs.trychroma.com
- https://python.langchain.com/docs/get_started/introduction.html
- https://github.com/UKPLab/sentence-transformers

