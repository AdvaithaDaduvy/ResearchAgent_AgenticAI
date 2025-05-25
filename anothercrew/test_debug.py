from crewdebug import run_research_bot_debug, simple_extraction_test

if __name__ == "__main__":
    pdfs = [
        "C:\\Users\\ADMIN\\Desktop\\Research\\p_r_o\\ag\\data\\algorithms-16-00176.pdf",
        "C:\\Users\\ADMIN\\Desktop\\Research\\p_r_o\\ag\\data\\Applied Computational Intelligence and Soft Computing - 2022 - Khan - Intelligent Model for Brain Tumor Identification.pdf"
    ]
    
    print("🧪 Starting debug session...")
    
    # First, try with a single PDF to see the structure
    print("\n=== TESTING SINGLE PDF ===")
    result = simple_extraction_test(pdfs[0])
    
    # Then try the full process
    print("\n=== TESTING FULL PROCESS ===")
    user_question = "What result can I expect if I use EfficientNet-B0 with Adam optimizer and a learning rate of 0.001?"
    final_result = run_research_bot_debug(pdfs, user_question)
    
    if final_result:
        print(f"\n🎉 Final result type: {type(final_result)}")
        print(f"🎉 Final result: {final_result}")
    else:
        print("\n❌ No final result obtained")