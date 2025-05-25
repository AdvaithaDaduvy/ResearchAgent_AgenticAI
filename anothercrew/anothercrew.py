# crew.py

from crewai import Crew
from tasks import create_extraction_task, create_analysis_task, create_prediction_task

def run_research_bot(pdf_paths: list[str], user_query: str):
    # Step 1: Extract summaries from each paper
    extraction_tasks = [create_extraction_task(path) for path in pdf_paths]
    crew_extraction = Crew(
        agents=[task.agent for task in extraction_tasks],
        tasks=extraction_tasks
    )
    
    print("📄 Running extraction tasks...")
    summaries_result = crew_extraction.kickoff()

    # Handle CrewOutput correctly - use .raw attribute
    if hasattr(summaries_result, "raw") and summaries_result.raw:
        summaries = [summaries_result.raw] if isinstance(summaries_result.raw, str) else list(summaries_result.raw)
    elif hasattr(summaries_result, "output") and summaries_result.output:
        output = summaries_result.output
        summaries = [output] if isinstance(output, str) else list(output)
    else:
        raise ValueError("Could not extract summaries from CrewOutput")

    # Step 2: Analyze patterns in extracted summaries
    analysis_task = create_analysis_task(summaries)
    crew_analysis = Crew(
        agents=[analysis_task.agent],
        tasks=[analysis_task]
    )
    
    print("📊 Running analysis task...")
    analysis_result = crew_analysis.kickoff()
    
    # Handle CrewOutput correctly for analysis - use .raw attribute
    if hasattr(analysis_result, "raw") and analysis_result.raw:
        pattern_report = analysis_result.raw
    elif hasattr(analysis_result, "output") and analysis_result.output:
        pattern_report = analysis_result.output
    else:
        raise ValueError("Could not extract analysis report from CrewOutput")

    # Step 3: Answer user's prediction query
    prediction_task = create_prediction_task(user_query, pattern_report)
    crew_prediction = Crew(
        agents=[prediction_task.agent],
        tasks=[prediction_task]
    )
    
    print("🤖 Running prediction task...")
    prediction_result = crew_prediction.kickoff()
    
    # Handle CrewOutput correctly for prediction - use .raw attribute
    if hasattr(prediction_result, "raw") and prediction_result.raw:
        final_prediction = prediction_result.raw
    elif hasattr(prediction_result, "output") and prediction_result.output:
        final_prediction = prediction_result.output
    else:
        raise ValueError("Could not extract final prediction from CrewOutput")

    return final_prediction