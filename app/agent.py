import os
from dotenv import load_dotenv

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types
from google.genai import Client

load_dotenv()  # Loads GEMINI_API_KEY from .env

def run_education_pipeline(text: str, target_language: str = "") -> str:
    """A strictly linear pipeline that acts as a Pedagogical Guide.
    
    Args:
        text: The raw input text/question from the student.
        target_language: The language to translate to (if specified). Defaults to Spanish if a translation keyword is present but unspecified.
        
    Returns:
        The final combined educational output.
    """
    if target_language is None:
        target_language = ""
        
    # Default to Spanish if translation requested but no specific language given.
    # The Orchestrator will pass a special flag or just empty string if it thinks translation is needed.
    if target_language.lower() == "default_translation":
        target_language = "Spanish"
        
    # Automatically use Vertex AI if deployed to Cloud Run (which sets GOOGLE_CLOUD_PROJECT)
    # Otherwise, fall back to Google AI Studio (local GEMINI_API_KEY)
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if project_id:
        client = Client(vertexai=True, project=project_id, location="us-central1")
    else:
        client = Client()
        
    model_id = "gemini-flash-latest"
    
    # 1. Socratic Cleaner Agent
    clean_prompt = f"Student Input:\n{text}"
    clean_config = types.GenerateContentConfig(
        system_instruction="""You are a Socratic Cleaner Agent.
Role: Sanitize the student's messy text (remove filler words like 'um', 'like', 'basically').
Pedagogical Task: Rewrite the student's concept into plain, highly accessible English. If the input is a question, identify and clearly state any underlying conceptual gaps.
Constraint: Do NOT translate. Output the accessible English and the identified conceptual gaps."""
    )
    cleaned_res = client.models.generate_content(model=model_id, contents=clean_prompt, config=clean_config)
    cleaned_text = cleaned_res.text
    
    # 2. Translator/Explanations Agent
    # If a language is specified, translate. Otherwise, just provide an explanation.
    if target_language:
        translate_prompt = f"Target Language: {target_language}\nStudent Concept:\n{cleaned_text}"
        translate_config = types.GenerateContentConfig(
            system_instruction="""You are a Translator & Explanations Agent.
Role: Translate the text accurately into the requested Target Language.
Pedagogical Task: Break down any hard terms into simple, analogical explanations in the Target Language, so a student doesn't have to scratch their head over jargon."""
        )
    else:
        translate_prompt = f"Student Concept:\n{cleaned_text}"
        translate_config = types.GenerateContentConfig(
            system_instruction="""You are an Explanations Agent.
Role: You are not translating today.
Pedagogical Task: Break down any hard terms in the provided text into simple, analogical explanations in English, so a student doesn't have to scratch their head over jargon."""
        )
        
    translated_res = client.models.generate_content(model=model_id, contents=translate_prompt, config=translate_config)
    explanation_text = translated_res.text
    
    # 3. Assessment & Feedback (QA) Agent
    check_prompt = f"Original Input: {text}\nProcessed Explanation: {explanation_text}"
    check_config = types.GenerateContentConfig(
        system_instruction="""You are an Assessment & Feedback (QA) Agent.
Role: Acts as a passive evaluator.
Pedagogical Task: Compare the original source text with the final explanation output. Provide formative feedback, highlighting specifically what part of the logic was correct and explaining any corrections conceptually. Output a PASS status or structured validation notes."""
    )
    qa_res = client.models.generate_content(model=model_id, contents=check_prompt, config=check_config)
    qa_notes = qa_res.text
    
    final_output = (
        f"### 🧹 Socratic Analysis\n{cleaned_text}\n\n"
        f"### 📖 Explanation " + (f"({target_language})" if target_language else "(English)") + f"\n{explanation_text}\n\n"
        f"### ✅ Assessment & Feedback\n{qa_notes}"
    )
    return final_output

# Root Orchestrator
root_agent = Agent(
    name="root_agent",
    model=Gemini(model="gemini-flash-latest", retry_options=types.HttpRetryOptions(attempts=3)),
    instruction="""You are the Orchestrator for a Pedagogical Educational Assistant.
Your ONLY job is to take the user's input and pass it exactly to the `run_education_pipeline` tool.
Determine if the user requested a translation. 
- If they specify a language (e.g. 'translate to French'), set target_language to that language.
- If they ask for translation but don't specify the language (e.g. 'translate this'), set target_language to 'default_translation'.
- If they don't mention translation, leave target_language blank.
Return the exact output from the pipeline to the user without adding any extra commentary.""",
    tools=[run_education_pipeline],
)

app = App(
    root_agent=root_agent,
    name="app",
)
