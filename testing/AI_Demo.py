# Gemini API key = AIzaSyCIkNw70BE2clrN0yyNsseIDhx7P3p-H84

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
# AIzaSyCIkNw70BE2clrN0yyNsseIDhx7P3p-H84
# Configure the API key from environment variable
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

model = genai.GenerativeModel('models/gemini-1.5-pro-latest')

prompt = """
write me a short cv example for a front end developer

Respond only with the requested output. Do not include extra commentary, questions, or offers to help unless explicitly asked.
"""

response = model.generate_content(prompt)

# Print the response
print(response.text)

# Save the response to a text file
with open('cv_example.txt', 'w', encoding='utf-8') as file:
    file.write(response.text)