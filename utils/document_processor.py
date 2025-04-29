import fitz  # PyMuPDF
import re
import logging
import os

# Configure logging
logger = logging.getLogger(__name__)

def read_pdf(file_path):
    """Extract text from a PDF file."""
    if not os.path.exists(file_path):
        logger.error(f"PDF file not found: {file_path}")
        raise FileNotFoundError(f"PDF file not found: {file_path}")
    
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        logger.info(f"Successfully extracted text from PDF: {file_path}")
        return text
    except Exception as e:
        logger.error(f"Error reading PDF file {file_path}: {str(e)}")
        raise ValueError(f"Error reading PDF file: {str(e)}")

def read_txt(file_path):
    """Read text from a TXT file."""
    if not os.path.exists(file_path):
        logger.error(f"TXT file not found: {file_path}")
        raise FileNotFoundError(f"TXT file not found: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        logger.info(f"Successfully read text from file: {file_path}")
        return text
    except UnicodeDecodeError:
        # Try with a different encoding if UTF-8 fails
        try:
            with open(file_path, 'r', encoding='latin-1') as file:
                text = file.read()
            logger.info(f"Successfully read text from file with latin-1 encoding: {file_path}")
            return text
        except Exception as e:
            logger.error(f"Error reading TXT file with latin-1 encoding {file_path}: {str(e)}")
            raise ValueError(f"Error reading TXT file: {str(e)}")
    except Exception as e:
        logger.error(f"Error reading TXT file {file_path}: {str(e)}")
        raise ValueError(f"Error reading TXT file: {str(e)}")

def clean_text(text):
    """Clean the extracted text."""
    try:
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters that might not be relevant
        text = re.sub(r'[^\w\s.,;:!?\'"-]', '', text)
        return text.strip()
    except Exception as e:
        logger.error(f"Error cleaning text: {str(e)}")
        return text  # Return original text if cleaning fails

def process_document(file_path, file_type):
    """Process document based on file type."""
    logger.info(f"Processing document: {file_path} of type {file_type}")
    
    if file_type.lower() == "pdf":
        text = read_pdf(file_path)
    elif file_type.lower() == "txt":
        text = read_txt(file_path)
    else:
        logger.error(f"Unsupported file type: {file_type}")
        raise ValueError(f"Unsupported file type: {file_type}")
    
    cleaned_text = clean_text(text)
    logger.info(f"Document processed. Original length: {len(text)}, Cleaned length: {len(cleaned_text)}")
    
    return cleaned_text