# GenAI Series

My journey learning Generative AI, LangChain, and LLM application development.

## Notebooks

The following notebooks are available in the `notebooks/` directory:

### Day 1 
- **`1_basic_langchain_using_llama.ipynb`**: A beginner-friendly introduction to LangChain using the Llama 3.3 model via the Groq API.

## Steps
1. create virtual environment
```sh
python -m venv env
```

2. activate it
```sh
env\Scripts\activate
```

3. install requirements
```sh
pip install -r requirements.txt
```

4. create a .env file
5. add your api key and run the notebook  **`1_basic_langchain_using_llama.ipynb`**

## What I Learned
- LangChain basics
- Connecting to Groq API
- Prompting LLMs
- Environment variables using python-dotenv

### Day 2
**`2_prompting_and_chains.ipynb`**: Learned prompt engineering, dynamic prompts, prompt templates, and basic LCEL chains using LangChain with Groq API.
**What I Learned (Day 2)**
- Static vs dynamic prompts
- Role-based message formatting
- ChatPromptTemplate usage
- Building prompt templates with variables
- Basic LCEL chaining (prompt | llm | parser)
- Simple output transformation