import os
import google.generativeai as genai
import json


# --- Configuration ---
# Load API key from environment variable (recommended)
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY environment variable not set. Please set it before running.")

# Configure the generative AI library with the API key
genai.configure(api_key=api_key)

MODEL_NAME = "gemini-2.0-flash" 

# --- CV Text ---
def parse_cv_with_gemini(cv_text):
    """
    Sends the CV text to Google's Gemini LLM and requests structured JSON output.
    """
    
    # Define the prompt for the LLM. It's similar to the OpenAI one, emphasizing JSON output.
    prompt = f"""
    You are a CV parsing assistant. Your task is to extract key information from the provided Curriculum Vitae text.
    
    Extract the following fields:
    - **name**: The full name of the candidate.
    - **email**: The email address.
    - **phone**: The phone number.
    - **address**: The physical address.
    - **summary**: The professional summary/objective.
    - **skills**: A list of key skills.
    - **experience**: A list of work experiences, where each experience is an object with:
        - **title**: Job title.
        - **company**: Company name.
        - **location**: Location of the company (if available).
        - **dates**: Employment dates (e.g., "Jan 2022 - Present").
        - **responsibilities**: A list of key responsibilities/achievements for that role.
    - **education**: A list of educational entries, where each entry is an object with:
        - **degree**: Degree obtained.
        - **institution**: Name of the institution.
        - **dates**: Years attended/graduated.
    - **certifications**: A list of certifications.
    - **affiliations**: A list of professional affiliations.
    - **languages**: A list of languages with their fluency level. Use the European framework for languages (A1, A2, B1, B2, C1, C2)

    Return the extracted information strictly as a JSON object. Do not include any additional text or formatting outside the JSON object. Ensure the JSON is valid and can be directly parsed.
    If a field is not found or is empty, its value should be null or an empty list/object as appropriate.
    
    CV Text:
    ---
    {cv_text}
    ---
    """

    try:
        # Initialize the generative model
        model = genai.GenerativeModel(MODEL_NAME)
        
        # Generate content. Gemini models don't have a direct `response_format` parameter
        # like OpenAI yet, so we emphasize it heavily in the prompt.
        # We also set generation configuration to be precise.
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.1,  # Lower temperature for more deterministic output
                top_p=0.1,        # Lower top_p for more focused output
                candidate_count=1 # Request only one candidate response
            )
        )

        # Access the text output. It might be in `response.text` or `response.candidates[0].text`
        llm_output_str = response.text.strip()
        
        # Sometimes LLMs wrap JSON in markdown code blocks, try to clean it up.
        if llm_output_str.startswith("```json") and llm_output_str.endswith("```"):
            llm_output_str = llm_output_str[7:-3].strip() # Remove ```json and ```

        # Parse the JSON string
        parsed_json = json.loads(llm_output_str)
        return parsed_json

    except Exception as e:
        print(f"An error occurred during Gemini API call or JSON parsing: {e}")
        # Print raw output for debugging if JSON parsing fails
        if 'llm_output_str' in locals():
            print(f"LLM Raw Output:\n{llm_output_str}")
        return {"error": str(e)}

