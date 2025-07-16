from google import genai
from dotenv import load_dotenv
import os

# load .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# define function for model and response
def get_response(message: str) -> str:
    client = genai.Client(api_key = api_key)
    response = client.models.generate_content(
        model = "gemini-2.0-flash",
        contents = [message]
    )
    return response.text

# if __name__ == "__main__":
#     print("responding..")
#     Message = input("How can I help you:")
#     result = response(Message)
#     print(result)