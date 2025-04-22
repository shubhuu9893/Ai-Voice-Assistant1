import google.generativeai as genai

# Configure the Gemini API
GEMINI_API_KEY = "AIzaSyBVnhtBkr6mzDnC658geVqA9DrxZXFQYNY"  # Replace with your actual API key
genai.configure(api_key=GEMINI_API_KEY)

# Create a model instance
model = genai.GenerativeModel('gemini-2.0-flash-exp-image-generation') 