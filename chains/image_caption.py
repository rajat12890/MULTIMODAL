# from transformers import pipeline
# from huggingface_hub import InferenceClient
# from PIL import Image
# import os
# from dotenv import load_dotenv

# load_dotenv()

# # Load once
# api_key = os.getenv("HUGGINGFACE_TOKEN")
# client = InferenceClient(api_key=api_key)

# # Initialize BLIP pipeline once
# image_captioner = pipeline(
#     "image-to-text",
#     model="Salesforce/blip-image-captioning-large",
#     token=api_key
# )

# def generate_image_caption(image: Image.Image) -> str:
#     response = image_captioner(image)
#     return response[0]["generated_text"] if response else "No caption generated."

# def remix_caption_as_character(caption: str, character: str) -> str:
#     character_prompts = {
#         "rapper": f"Describe this caption like you're a rapper: {caption}.",
#         "shrek": f"Describe this caption like you're Shrek: {caption}.",
#         "unintelligible": f"Describe this caption in a way that makes no sense: {caption}.",
#         "cookie monster": f"Describe this caption like you're cookie monster: {caption}."
#     }

#     prompt = character_prompts.get(character, caption)

#     messages = [{"role": "user", "content": prompt}]
#     stream = client.chat.completions.create(
#         model="meta-llama/Llama-3.2-3B-Instruct",
#         messages=messages,
#         max_tokens=500,
#         stream=True
#     )

#     response = ''
#     for chunk in stream:
#         if chunk.choices[0].delta.content:
#             response += chunk.choices[0].delta.content

#     return response

# def generate_character_caption(image: Image.Image, character: str) -> str:
#     base_caption = generate_image_caption(image)
#     character_caption = remix_caption_as_character(base_caption, character)
#     return character_caption
