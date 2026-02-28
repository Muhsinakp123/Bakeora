import os
import replicate

os.environ["REPLICATE_API_TOKEN"] = os.getenv("REPLICATE_API_TOKEN")

def generate_cake_image(
    cake_type,
    size,
    flavor,
    cream_type,
    message,
    special_instructions,
    reference_image_url=None
):

    prompt = f"""
    A realistic professional bakery photo of a {size} {flavor} {cake_type} cake.
    Frosting: {cream_type}.
    Message on cake: "{message}".
    Special instructions: {special_instructions}.
    High quality, detailed, soft lighting.
    """

    input_data = {
        "prompt": prompt,
        "width": 768,
        "height": 768
    }

    try:
        output = replicate.run(
            "stability-ai/sdxl:7762fd07cf82e0a2b50d1f94a639a6a39aea66e68132c0a918645ed90e299887",
            input=input_data
        )

        if isinstance(output, list) and len(output) > 0:
            return output[0]
        else:
            return "No image generated"

    except Exception as e:
        return f"Error: {str(e)}"