"""Generate an image with OpenAI DALL-E and create resized variants.

Demonstrates using the OpenAI Images API to generate an image from a text
prompt, downloading it, and creating multiple resized copies with Pillow.
"""

from io import BytesIO
from pathlib import Path
from pprint import pprint
from types import MappingProxyType
from typing import Any

import openai
import requests
from PIL import Image

# Model parameters reference for validation
PARAMS: dict[str, dict[str, Any]] = {
    "dall-e-2": {
        "max_prompt_size": 1000,
        "n": {"min": 1, "max": 10},
        "quality": None,
        "response_format": ["url", "b64_json"],
        "size": ["256x256", "512x512", "1024x1024"],
        "style": None,
    },
    "dall-e-3": {
        "max_prompt_size": 4000,
        "n": {"min": 1, "max": 1},
        "quality": ["standard", "hd"],
        "response_format": ["url", "b64_json"],
        "size": ["1024x1792", "1792x1024", "1024x1024"],
        "style": ["vivid", "natural"],
    },
}

DEFAULT_MODEL = "dall-e-3"

DEFAULT_CONFIG: MappingProxyType[str, Any] = MappingProxyType({
    "n": PARAMS[DEFAULT_MODEL]["n"]["min"],
    "quality": PARAMS[DEFAULT_MODEL]["quality"][0],
    "response_format": PARAMS[DEFAULT_MODEL]["response_format"][0],
    "size": PARAMS[DEFAULT_MODEL]["size"][0],
    "style": PARAMS[DEFAULT_MODEL]["style"][0],
})


def _ensure_model_name_is_valid(model: str) -> None:
    """Raise ValueError if *model* is not a supported DALL-E model."""
    if model not in PARAMS:
        raise ValueError(f"Model must be one of: {', '.join(PARAMS)}")


def _ensure_prompt_is_valid(prompt: str, model: str) -> None:
    """Raise ValueError if *prompt* exceeds the model's character limit."""
    max_size = PARAMS[model]["max_prompt_size"]
    if len(prompt) > max_size:
        raise ValueError(f"Prompt must be at most {max_size} characters.")


def _ensure_config_is_valid(config: dict[str, Any], model: str) -> None:
    """Validate each config key against the allowed values for *model*."""
    model_params = PARAMS[model]
    for key, value in config.items():
        if key not in model_params:
            continue
        if value is None:
            raise ValueError(f"Value for '{key}' cannot be None.")

        allowed = model_params[key]
        if key == "n":
            if not (allowed["min"] <= value <= allowed["max"]):
                raise ValueError(
                    f"'{key}' must be between {allowed['min']} and {allowed['max']}."
                )
        elif isinstance(allowed, list) and value not in allowed:
            raise ValueError(
                f"'{key}' must be one of: {', '.join(allowed)}"
            )


def generate_image(
    prompt: str,
    model: str = DEFAULT_MODEL,
    config: dict[str, Any] | None = None,
) -> str:
    """Generate an image via the OpenAI API and return its URL.

    Args:
        prompt: Text description of the desired image.
        model: DALL-E model name.
        config: Generation parameters (n, quality, size, style, response_format).

    Returns:
        URL of the generated image.
    """
    if config is None:
        config = dict(DEFAULT_CONFIG)

    _ensure_model_name_is_valid(model)
    _ensure_prompt_is_valid(prompt, model)
    _ensure_config_is_valid(config, model)

    client = openai.OpenAI()  # Uses OPENAI_API_KEY env var

    try:
        response = client.images.generate(prompt=prompt, model=model, **config)
        return response.data[0].url
    except openai.OpenAIError as exc:
        raise RuntimeError(f"Failed to generate image: {exc}") from exc


def download_image(image_url: str, filename_without_ext: str) -> dict[str, Any]:
    """Download an image from *image_url* and save it locally.

    Returns:
        Dict with original filename, path, dimensions, and aspect ratio.
    """
    try:
        response = requests.get(image_url, timeout=60)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise RuntimeError(f"Error downloading image: {exc}") from exc

    try:
        original_image = Image.open(BytesIO(response.content))
        original_filename = f"{filename_without_ext}_original.jpg"
        original_image.save(original_filename)
        print(f"Original image saved as {original_filename}")
    except IOError as exc:
        raise RuntimeError(f"Error processing image: {exc}") from exc

    width, height = original_image.size
    return {
        "filename_without_ext": filename_without_ext,
        "original_filename": original_filename,
        "image_object": original_image,
        "path": Path(original_filename),
        "width": width,
        "height": height,
        "ratio": height / width,
    }


def create_variants(
    image_details: dict[str, Any],
    target_widths: list[int],
) -> dict[str, dict[str, Any]]:
    """Create resized copies of the original image at each target width.

    Returns:
        Dict keyed by size label (e.g. "780x1365") with path and dimensions.
    """
    images: dict[str, dict[str, Any]] = {
        "original": {
            "filename": image_details["original_filename"],
            "path": image_details["path"],
            "width": image_details["width"],
            "height": image_details["height"],
        }
    }

    try:
        for width in target_widths:
            height = int(width * image_details["ratio"])
            size_label = f"{width}x{height}"
            resized = image_details["image_object"].resize((width, height))
            filename = f"{image_details['filename_without_ext']}_{size_label}.jpg"
            resized.save(filename)
            print(f"Resized image saved as {filename}")
            images[size_label] = {
                "filename": filename,
                "path": Path(filename),
                "width": width,
                "height": height,
            }
    except IOError as exc:
        raise RuntimeError(f"Error processing image: {exc}") from exc

    return images


if __name__ == "__main__":
    img_prompt = (
        "A cute corgi dog in a space suit, floating in space, "
        "and trying to reach a tasty treat."
    )

    print("Generating image...")
    generated_image_url = generate_image(img_prompt)

    print("Downloading generated image...")
    original_image_details = download_image(generated_image_url, "doggo_in_space")

    desired_target_widths = [780, 500, 342, 185, 154, 92]

    print("Creating image variants...")
    generated_images_details = create_variants(
        image_details=original_image_details,
        target_widths=desired_target_widths,
    )

    print("Image processing completed.")
    print("Generated image details:")
    pprint(generated_images_details)
