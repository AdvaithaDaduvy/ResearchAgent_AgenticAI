
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from crewai import Agent,LLM
from dotenv import load_dotenv
load_dotenv()


llm=LLM(api_key=os.getenv("GOOGLE_API_KEY"),model="gemini/gemini-1.5-flash")

extractor_agent = Agent(
    role='Scientific Summary Extractor',
    goal='Extract models, methodologies, and results from research papers',
    backstory='Expert in scientific literature review and summarization.',
    verbose=True,
    llm=llm
)

analyst_agent = Agent(
    role='Pattern Analyst',
    goal='Analyze summaries from multiple papers to find common trends and performance patterns',
    backstory='Specialist in comparing ML techniques and identifying performance benchmarks.',
    verbose=True,
    llm=llm
)

chat_agent = Agent(
    role='Prediction Assistant',
    goal='Given a model and method, predict likely result based on previous research patterns',
    backstory='Expert assistant trained on summarized literature to predict outcomes for model-method combos.',
    verbose=True,
    llm=llm
)