import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')

def query_agent(question, collection, k=3):
    results = collection.query(
        query_texts=[question],
        n_results=k
    )
    context = "\n\n".join(results['documents'][0])
    
    prompt = f"""
    Use ONLY the following context to answer the question. 
    If the information is not in the context, say 'Not found in document'.
    
    Context:
    {context}
    
    Question: {question}
    """
    
    response = model.generate_content(prompt)
    return response.text.strip()

def analyze_pitch_deck(collection):
    # Summary Agent
    summary_question = (
        "What is the company's core product, who is the target customer, "
        "and what problem does it solve? Provide a concise one-paragraph summary."
    )
    summary = query_agent(summary_question, collection)
    
    # Team Agent
    team_question = (
        "Identify the key founders or team members mentioned in the deck "
        "and summarize their roles and previous experience as listed in the document."
    )
    team_analysis = query_agent(team_question, collection)
    
    return {
        "summary": summary,
        "team_analysis": team_analysis
    }