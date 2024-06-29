# -*- coding: utf-8 -*-
from pathlib import Path
from pprint import pprint
from types import MappingProxyType
from io import BytesIO
import requests

import openai
from PIL import Image

"""
Install the OpenAI library:
pip install --upgrade openai

More info about getting started with OpenAI:
https://platform.openai.com/docs/quickstart

----

To use PIL, you must install it:
pip install --upgrade Pillow
"""

params = {
    "dall-e-2": {
        "max_prompt_size": 1000,
        "n": {
            "min": 1,
            "max": 10
        },
        "quality": None,
        "response_format": [
            "url",  # Only available for 60 minutes after the request
            "b64_json"
        ],
        "size": [
            "256x256",   # Square
            "512x512",   # Bigger square
            "1024x1024"  # Even Bigger square
        ],
        "style": None
    },
    "dall-e-3": {
        "max_prompt_size": 4000,
        "n": {
            "min": 1,
            "max": 1
        },
        "quality": ["standard", "hd"],
        "response_format": [
            "url",  # Only available for 60 minutes after the request
            "b64_json"
        ],
        "size": [
            "1024x1792",  # Portrait
            "1792x1024",  # Landscape
            "1024x1024"   # Square
        ],
        "style": ["vivid", "natural"]
    }
}

default_model = "dall-e-3"

default_config = MappingProxyType({  # Immutable dictionary
    "n": params[default_model]["n"]["min"],
    "quality": params[default_model]["quality"][0],
    "response_format": params[default_model]["response_format"][0],
    "size": params[default_model]["size"][0],
    "style": params[default_model]["style"][0]
})


def _ensure_model_name_is_valid(model: str):
    if model is None:
        raise ValueError("Model name cannot be None.")

    if model in params:
        return

    raise ValueError(f"Model name must be one of the following: {', '.join(params.keys())}")


def _ensure_prompt_is_valid(prompt: str, model: str):
    max_prompt_size = params[model]["max_prompt_size"]

    if prompt is None:
        raise ValueError("Prompt cannot be None.")

    if len(prompt) <= max_prompt_size:
        return

    raise ValueError(f"Prompt must be less than or equal to {max_prompt_size} characters.")


def _ensure_config_is_valid(config: dict, model: str):
    for key, value in config.items():
        if key in params[model]:
            if value is None:
                raise ValueError(f"Value for key '{key}' cannot be None.")

            if key == "n":
                if value < params[model][key]["min"] or value > params[model][key]["max"]:
                    raise ValueError(f"Value for key '{key}' must be between {params[model][key]['min']} and {params[model][key]['max']}.")

            if key == "quality":
                if value not in params[model][key]:
                    raise ValueError(f"Value for key '{key}' must be one of the following: {', '.join(params[model][key])}")

            if key == "response_format":
                if value not in params[model][key]:
                    raise ValueError(f"Value for key '{key}' must be one of the following: {', '.join(params[model][key])}")

            if key == "size":
                if value not in params[model][key]:
                    raise ValueError(f"Value for key '{key}' must be one of the following: {', '.join(params[model][key])}")

            if key == "style":
                if value not in params[model][key]:
                    raise ValueError(f"Value for key '{key}' must be one of the following: {', '.join(params[model][key])}")


def generate_image(prompt: str, model: str = default_model, config: dict = default_config):
    # Validate inputs
    _ensure_model_name_is_valid(model)
    _ensure_prompt_is_valid(prompt, model)
    _ensure_config_is_valid(config, model)

    # Create the OpenAI client
    client = openai.OpenAI(api_key="use your API key here. maybe get it form an environment variable.")

    try:
        # Generate the image
        response = client.images.generate(
            prompt=prompt,
            model=model,
            **config
        )

        # Extracting and returning the image URL
        return response.data[0].url
    except openai.OpenAIError as e:
        print("Failed to generate image using OpenAI:")
        print(e.http_status)
        print(e.error)
        print("--------------------")
        print(e)
        raise Exception("Failed to generate image using OpenAI. Cannot proceed", e)


def download_image(image_url: str, filename_without_ext: str):
    try:
        # Download the image
        response = requests.get(image_url)

        # Check if the request was successful
        response.raise_for_status()

        # Open the image using PIL
        original_image = Image.open(BytesIO(response.content))

        # Insert _original into the filename
        original_filename = f"{filename_without_ext}_original.jpg"

        # Save the original image
        original_image.save(original_filename)
        print(f"Original image saved as {original_filename}")

        # Get the image width and height
        original_width, original_height = original_image.size

        # Calculate the ratio
        ratio = original_height / original_width

        # Return the image details
        return {
            "filename_without_ext": filename_without_ext,
            "original_filename": original_filename,
            "image_object": original_image,
            "path": Path(original_filename),
            "width": original_width,
            "height": original_height,
            "ratio": ratio
        }

    except requests.RequestException as e:
        print(f"Error downloading the image: {e}")
        raise Exception("Error downloading the image. Cannot proceed", e)
    except IOError as e:
        print(f"Error processing the image: {e}")
        raise Exception("Error processing the image. Cannot proceed", e)


def create_variants(image_details: dict, target_widths: list):
    # Create a dictionary to store the image details
    images = {
        "original": {
            "filename": image_details["original_filename"],
            "path": image_details["path"],
            "width": image_details["width"],
            "height": image_details["height"]
        }
    }

    try:
        # Loop through the sizes
        for width in target_widths:
            # Calculate the height
            height = int(width * image_details["ratio"])

            # Create reference for the variant image size
            size = f"{width}x{height}"

            # Resize the image
            resized_image = image_details["image_object"].resize((width, height))

            # Insert the size into the filename
            filename = f"{image_details['filename_without_ext']}_{size}.jpg"

            # Save the resized image
            resized_image.save(filename)
            print(f"Resized image saved as {filename}")

            # Add the image details to the dictionary
            images[size] = {
                "filename": filename,
                "path": Path(filename),
                "width": width,
                "height": height
            }

        # Return the image variants
        return images
    except IOError as e:
        print(f"Error processing the image: {e}")
        raise Exception("Error processing the image. Cannot proceed", e)


if __name__ == '__main__':
    # Prompt for the image
    img_prompt = "A cute corgi dog in a space suit, floating in space, and trying to reach a tasty treat."

    print("Generating image...")
    generated_image_url = generate_image(img_prompt)

    print("Downloading generated image...")
    original_image_details = download_image(generated_image_url, "doggo_in_space")

    # Define the desired target widths
    desired_target_widths = [780, 500, 342, 185, 154, 92]

    print("Creating image variants...")
    generated_images_details = create_variants(
        image_details=original_image_details,
        target_widths=desired_target_widths
    )

    print("Image processing completed.")
    print("Generated image details:")
    pprint(generated_images_details)
