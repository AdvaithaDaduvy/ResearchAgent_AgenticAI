# crew_debug.py - For debugging CrewAI output structure

from crewai import Crew
from tasks import create_extraction_task, create_analysis_task, create_prediction_task
import json

def debug_crew_output(result, stage_name):
    """Debug function to inspect CrewAI output structure"""
    print(f"\n🔍 === DEBUGGING {stage_name.upper()} OUTPUT ===")
    print(f"Type: {type(result)}")
    print(f"String representation: {str(result)}")
    
    if hasattr(result, '__dict__'):
        print(f"Object attributes: {list(result.__dict__.keys())}")
        for key, value in result.__dict__.items():
            print(f"  {key}: {type(value)} = {str(value)[:100]}{'...' if len(str(value)) > 100 else ''}")
    
    # Check common attributes
    common_attrs = ['output', 'raw', 'result', 'content', 'data', 'response']
    for attr in common_attrs:
        if hasattr(result, attr):
            attr_value = getattr(result, attr)
            print(f"✅ Found attribute '{attr}': {type(attr_value)} = {str(attr_value)[:100]}{'...' if len(str(attr_value)) > 100 else ''}")
    
    print(f"=== END {stage_name.upper()} DEBUG ===\n")

def run_research_bot_debug(pdf_paths: list[str], user_query: str):
    try:
        # Step 1: Extract summaries from each paper
        print("📄 Creating extraction tasks...")
        extraction_tasks = [create_extraction_task(path) for path in pdf_paths]
        print(f"Created {len(extraction_tasks)} extraction tasks")
        
        crew_extraction = Crew(
            agents=[task.agent for task in extraction_tasks],
            tasks=extraction_tasks
        )
        
        print("📄 Running extraction tasks...")
        summaries_result = crew_extraction.kickoff()
        
        # Debug the result
        debug_crew_output(summaries_result, "EXTRACTION")
        
        # Try to extract the actual data
        summaries = None
        if hasattr(summaries_result, "output"):
            summaries = summaries_result.output
        elif hasattr(summaries_result, "raw"):
            summaries = summaries_result.raw
        elif isinstance(summaries_result, (str, list)):
            summaries = summaries_result
        else:
            # If it's an object, try to find string/list attributes
            for attr_name in dir(summaries_result):
                if not attr_name.startswith('_'):
                    attr_value = getattr(summaries_result, attr_name)
                    if isinstance(attr_value, (str, list)) and attr_value:
                        summaries = attr_value
                        print(f"🎯 Using attribute '{attr_name}' as summaries")
                        break
        
        if summaries is None:
            print("❌ Could not extract summaries from result")
            return None
        
        print(f"✅ Successfully extracted summaries: {type(summaries)}")
        if isinstance(summaries, str):
            summaries = [summaries]
        
        print(f"📄 Got {len(summaries)} summaries")
        
        # For now, let's stop here and see what we get
        return summaries
        
    except Exception as e:
        print(f"❌ Error in debug function: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

# Alternative simple test function
def simple_extraction_test(pdf_path):
    """Test extraction with a single PDF"""
    print(f"🧪 Testing extraction with: {pdf_path}")
    try:
        task = create_extraction_task(pdf_path)
        crew = Crew(agents=[task.agent], tasks=[task])
        result = crew.kickoff()
        
        debug_crew_output(result, "SIMPLE_TEST")
        return result
    except Exception as e:
        print(f"❌ Simple test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return None