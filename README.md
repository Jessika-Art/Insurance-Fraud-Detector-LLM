# Insurance Fraud Detector
A web application that analyzes insurance claim documents for potential fraud by detecting inconsistencies using OpenAI's GPT model.

## Features
- Upload and analyze insurance claim documents (PDF or TXT formats)
- AI-powered analysis of claim narratives for inconsistencies
- Trustworthiness scoring from 1-100
- Detailed analysis of potential fraud indicators
- Simple and intuitive web interface

## How It Works
1. User uploads a document (PDF or TXT) through the web interface
2. Document is read and cleaned (removing unnecessary spaces, junk)
3. Cleaned text is sent to OpenAI's GPT model for analysis
4. The AI checks for inconsistencies in dates, people, events, and logic errors
5. Results are displayed with a trustworthiness score and detailed analysis
6. Analysis results are saved as JSON files for future reference

## Requirements
The application requires the following Python libraries:

- openai
- pydantic
- python-dotenv
- PyMuPDF (fitz)
- fastapi
- uvicorn
- python-multipart
- jinja2

Remember to create the .env file on the root directory and paste your OpenAI api-key like this OPENAI_API_KEY=xx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

## Running the Application
To run the application, execute the following command in your terminal:
uvicorn app:app --reload
You can then access the application at:
http://localhost:8000

## Usage
1. Click the "Choose File" button to select a PDF or TXT document
2. Click "Analyze Document" to start the analysis
3. Wait for the analysis to complete
4. View the trustworthiness score and detailed analysis
5. Results are also saved in the results directory for future reference
## Project Structure

```
Insurance Fraud Detector
├─ 📁results
│  ├─ 📄Daneil Carter_analysis.json
│  └─ 📄Sarah Williams_analysis.json
├─ 📁static
│  ├─ 📁css
│  │  └─ 📄style.css
│  └─ 📁js
│     └─ 📄script.js
├─ 📁stories_sample
│  ├─ 📄Daneil Carter.txt
│  └─ 📄Sarah Williams.txt
├─ 📁templates
│  └─ 📄index.html
├─ 📁uploads
├─ 📁utils
│  ├─ 📄document_processor.py
│  └─ 📄openai_analyzer.py
├─ 📄.gitignore
├─ 📄app.py
└─ 📄README_.md
```

## Notes
- The application uses OpenAI's GPT-3.5-turbo model by default
- For more consistent results, the temperature parameter is set to 0
- Analysis results may still vary slightly between runs due to the nature of AI models
