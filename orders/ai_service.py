import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def generate_cake_image(
    cake_type,
    size,
    flavor,
    cream_type,
    message,
    special_instructions
):

    prompt = f"""
    Create a realistic bakery cake design.

    Cake type: {cake_type}
    Size: {size}
    Flavor: {flavor}
    Cream: {cream_type}
    Message on cake: {message}
    Instructions: {special_instructions}

    Describe the cake visually like a bakery catalog product photo.
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-flash-latest")

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:
        return f"Error: {str(e)}"