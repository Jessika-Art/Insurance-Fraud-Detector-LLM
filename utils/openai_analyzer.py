import os
import logging
from openai import OpenAI
from dotenv import load_dotenv
import json

# Configure logging
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    logger.error("OpenAI API key not found. Please set OPENAI_API_KEY in your .env file.")

# Initialize OpenAI client
try:
    client = OpenAI(api_key=api_key)
except Exception as e:
    logger.error(f"Error initializing OpenAI client: {str(e)}")
    client = None

def analyze_claim(text):
    """
    Analyze the insurance claim text for inconsistencies using OpenAI.
    Returns a summary, trustworthiness score, and detailed analysis.
    """
    if not client:
        raise ValueError("OpenAI client not initialized. Check your API key.")
    
    if not text or len(text.strip()) == 0:
        raise ValueError("Empty document provided for analysis.")
    
    logger.info(f"Analyzing document of length: {len(text)} characters")
    
    prompt = f"""
    You are an expert insurance fraud investigator. Analyze the following insurance claim document for inconsistencies, logical errors, or suspicious elements.

    Document:
    {text}

    Instructions:
    1. Carefully check for inconsistencies in dates, people, events, and logical errors.
    2. Write a brief critical summary about any suspicious points you find.
    3. Provide a trustworthiness score between 1-100 where:
       - 1 = Very suspicious (many inconsistencies)
       - 100 = Fully coherent and believable
    4. Justify your score with specific examples from the text.
    5. Consider if the claimer has proof of the claim such pictures, videos, evidances, or documents, this should raise the score.

    Format your response as a JSON object with the following structure:
    {{
        "summary": "A brief paragraph summarizing your findings",
        "trustworthiness_score": [score between 1-100],
        "detailed_analysis": "A more detailed explanation of inconsistencies found"
    }}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert insurance fraud investigator."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.0  # Add this parameter for more consistent results
        )
        
        logger.info("Successfully received response from OpenAI")
        
        # Parse the JSON response
        try:
            result = json.loads(response.choices[0].message.content)
            return result
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing OpenAI response: {str(e)}")
            # Fallback in case the response is not valid JSON
            content = response.choices[0].message.content
            return {
                "summary": "Error parsing analysis results.",
                "trustworthiness_score": 50,
                "detailed_analysis": f"Error parsing OpenAI response: {content[:500]}..."
            }
    except Exception as e:
        logger.error(f"Error calling OpenAI API: {str(e)}")
        raise ValueError(f"Error calling OpenAI API: {str(e)}")