# tasks.py

from crewai import Task
from tools import ResearchPaperReaderTool
from agent import extractor_agent, analyst_agent, chat_agent

# Instantiate the tool
reader_tool = ResearchPaperReaderTool()

# Task 1: Extract info from one paper
def create_extraction_task(file_path: str):
    return Task(
        description=f"Read and extract models, methods, and results from the research paper at {file_path}.",
        agent=extractor_agent,
        tools=[reader_tool],
        expected_output="Structured summary of the research paper with models used, methodologies, and results."
    )

# Task 2: Analyze multiple summaries
def create_analysis_task(summaries: list[str]):
    joined_summaries = "\n\n".join(summaries)
    return Task(
        description=f"Analyze the following summaries of research papers to identify common models, methodologies, and result trends:\n\n{joined_summaries}",
        agent=analyst_agent,
        expected_output="A performance pattern report showing which models and methods perform best under what conditions."
    )

# Task 3: Predict result from model+method input
def create_prediction_task(user_query: str, pattern_report: str):
    return Task(
        description=f"Based on the pattern report:\n{pattern_report}\nPredict the expected result for: {user_query}",
        agent=chat_agent,
        expected_output="An estimated outcome or expected performance for the provided model-method combination."
    )
