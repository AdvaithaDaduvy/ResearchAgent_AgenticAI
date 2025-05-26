# main.py

from anothercrew import run_research_bot
import os

def main():
    # PDF file paths 
    pdfs = [
        "../data/algorithms-16-00176.pdf",
        "../data/Applied Computational Intelligence and Soft Computing - 2022 - Khan - Intelligent Model for Brain Tumor Identification.pdf"
    ]
    
    
    print("🔍 Verifying PDF files...")
    for i, pdf_path in enumerate(pdfs):
        if os.path.exists(pdf_path):
            print(f"✅ PDF {i+1}: Found - {os.path.basename(pdf_path)}")
        else:
            print(f"❌ PDF {i+1}: NOT FOUND - {pdf_path}")
            print("Please check the file path and try again.")
            return
    
    # Research question
    user_question = "What result can I expect if I use EfficientNet-B0 with Adam optimizer and a learning rate of 0.001?"
    
    print(f"\n🤔 Research Question: {user_question}")
    print(f"📚 Analyzing {len(pdfs)} research papers...")
    print("=" * 80)
    
    try:
        
        final_answer = run_research_bot(pdfs, user_question)
        
        print("\n" + "=" * 80)
        print("🧠 FINAL PREDICTION:")
        print("=" * 80)
        print(final_answer)
        print("=" * 80)
        
        
        save_results = input("\n💾 Would you like to save the results to a file? (y/n): ").lower().strip()
        if save_results == 'y':
            output_file = "research_prediction_results.txt"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("RESEARCH QUESTION:\n")
                f.write(f"{user_question}\n\n")
                f.write("ANALYZED PAPERS:\n")
                for i, pdf in enumerate(pdfs, 1):
                    f.write(f"{i}. {os.path.basename(pdf)}\n")
                f.write(f"\nPREDICTION RESULTS:\n")
                f.write(final_answer)
            print(f"✅ Results saved to: {output_file}")
        
    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")
        print("\n🔧 Troubleshooting tips:")
        print("1. Make sure all PDF files exist and are readable")
        print("2. Check that your tasks.py file is properly configured")
        print("3. Ensure all required dependencies are installed")
        print("4. Verify your CrewAI agents are properly set up")
        
        
        import traceback
        print(f"\n🐛 Full error details:")
        traceback.print_exc()

if __name__ == "__main__":
    print(" Starting AI Research Assistant...")
    print("This tool will analyze research papers and provide predictions based on your query.")
    print()
    
    main()
    
    print("\n👋 Research analysis complete!")

# main.py

from anothercrew import run_research_bot
import os

def run_ai_research(pdfs, user_question):
    print("🔍 Verifying PDF files...")
    for i, pdf_path in enumerate(pdfs):
        if os.path.exists(pdf_path):
            print(f"✅ PDF {i+1}: Found - {os.path.basename(pdf_path)}")
        else:
            raise FileNotFoundError(f"❌ PDF {i+1}: NOT FOUND - {pdf_path}")
    
    print(f"\n🤔 Research Question: {user_question}")
    print(f"📚 Analyzing {len(pdfs)} research papers...")
    print("=" * 80)
    
    final_answer = run_research_bot(pdfs, user_question)
    return final_answer

