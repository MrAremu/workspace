import sys
import os
import json
import base64
import requests
from pypdf import PdfReader

# Load API Key from .env manually (simpler than dotenv for just one key)
def load_env_key():
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                if line.startswith('OPENROUTER_API_KEY='):
                    return line.strip().split('=', 1)[1]
    return os.environ.get('OPENROUTER_API_KEY')

OPENROUTER_KEY = load_env_key()
# Using a model that supports vision and text
MODEL = "openai/gpt-4o" 

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def extract_pdf_text(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"PDF Error: {e}")
        return ""

def analyze_document(file_path):
    if not OPENROUTER_KEY:
        print("Error: OPENROUTER_API_KEY not found in .env")
        return None

    filename = os.path.basename(file_path).lower()
    is_image = filename.endswith(('.png', '.jpg', '.jpeg', '.webp'))
    
    prompt = """
    Analyze this receipt/invoice. Extract the following fields in strict JSON format:
    {
        "Expense Date": "YYYY-MM-DD",
        "Vendor": "Name of vendor",
        "Expense Amount": "0.00",
        "Expense Type": "Category (e.g. Travel, Meals, Office Supplies, Software)",
        "Expense Description": "Brief description of items",
        "Reference": "Invoice number if available, else empty"
    }
    If the amount is an expense, ensure it is positive number.
    Only return the JSON.
    """

    messages = []
    
    if is_image:
        base64_image = encode_image(file_path)
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]
    else:
        # PDF Text Extraction
        text_content = extract_pdf_text(file_path)
        if not text_content.strip():
             messages = [{"role": "user", "content": prompt + "\n\n[Empty PDF Content]"}] # Handle empty PDF
        else:
             messages = [{"role": "user", "content": prompt + f"\n\nDocument Text:\n{text_content}"}]

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_KEY}",
                "Content-Type": "application/json",
                 "HTTP-Referer": "http://localhost:3000", # Optional for OpenRouter
            },
            json={
                "model": MODEL,
                "messages": messages,
                "response_format": { "type": "json_object" } 
            }
        )
        
        if response.status_code == 200:
            content = response.json()['choices'][0]['message']['content']
            # Clean md blocks if present
            content = content.replace('```json', '').replace('```', '').strip()
            return json.loads(content)
        else:
            print(f"API Error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"Exception during analysis: {e}")
        return None

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python analyze_document.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    result = analyze_document(file_path)
    if result:
        print(json.dumps(result, indent=2))
