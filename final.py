import json
from openai import OpenAI
import openai
import requests
from io import BytesIO
import os
import torch
import base64
import requests
from PIL import Image as PILImage
import fitz  # PyMuPDF pip install pymupdf
import re
from dotenv import load_dotenv


#------------API key setup----------------
load_dotenv()
AI_TOKEN = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=AI_TOKEN)

# # List all models
# models = client.models.list()

# # Print model IDs
# for model in models.data:
#     print(model.id)


#-----------Load data----------------

def load_json_data(json_path):
    """Load model data from JSON file."""
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"JSON file not found: {json_path}")
    
    with open(json_path, "r") as f:
        return json.load(f)
    

def extract_pdf_summary(pdf_path):
    # === Step 1: Extract Text ===
    with fitz.open(pdf_path) as doc:
        text = ""
        for page in doc:
            text += page.get_text()

    # === Step 3: Prompt GPT to extract core info ===
    title_prompt = f"""
    You are analyzing a scientific article. From the text below, extract:
    1. A 4-6 words clean and accurate title that captures the paper’s topic
    2. The final human-engineered object or system (e.g., "Train", "Sensor", "Wing", "Nose Cone", "Surface Coating")

    Be concise. Output JSON like this:
    {{
      "title": "...",
      "organism_": "..."
    }}

    Article:
    \"\"\"
    {text}
    \"\"\"
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert in summarizing scientific papers for visual infographic generation."},
            {"role": "user", "content": title_prompt}
        ],
        temperature=0.2
    )

    answer = response.choices[0].message.content
    answer = answer.strip().removeprefix("```json").removesuffix("```").strip()

    return answer



# ----------summary json    ----------------

def generate_summary_prompt_multiple(model_data, filename):
    """Generate prompt for multiple models (pdf = True case)."""
    base_title = os.path.splitext(os.path.basename(filename))[0].replace("_", " ").title()
    
    return f"""
You are given a JSON file that contains **multiple biological or technical models** under a key called "models".

Each model has a `title`, an `organism`, and a list of `functional_components`.

You should return a single structured JSON object summarizing **all models** as a multi-layer system.

The output must include:
- title: Use the filename as the global title (e.g., "{base_title}")
- organism: object or organism based on the title
- layers: Each model becomes a layer, derived from its first functional component.

Each layer must include:
  - name
  - function: from the model's first functional component
  - description
  - caption: a condensed version of the function in ≤10 words
  - scale: from the component
  - visual: what to draw based on model + function

Sort the layers by descending scale string (but do not convert units).

Here is the data:
{json.dumps(model_data, indent=2)}
"""


def generate_summary_prompt_single(model_data):
    """Generate prompt for single model (pdf = False case)."""
    return f"""
You are given the JSON below that describes a **single** biological or technical system.

Extract a structured summary as a clean, valid JSON object with the following keys:
- title
- organism
- layers: a list of objects sorted from largest to smallest based on the scale string (but do not convert the units), make sure it's sorted from the largest to the smallest

Each layer should include:
  - name
  - function
  - description
  - caption (a condensed version of the function in ≤10 words)
  - scale
  - visual (a short instruction on what to draw)

Here is the data:
{json.dumps(model_data, indent=2)}
"""


def extract_json_content(prompt, model="gpt-4o", temperature=0.2):
    """
    Extract and organize JSON content for scientific diagram generation.
    
    Args:
        prompt (str): The user prompt to send to the model
        model (str): The OpenAI model to use (default: "gpt-4o")
        temperature (float): Temperature setting for the model (default: 0.2)
    
    Returns:
        dict: Parsed JSON data as Python dictionary
    """
    client = OpenAI()
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You extract and organize JSON content for scientific diagram generation."},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature
    )
    
    raw_output = response.choices[0].message.content
    
    # Remove the triple backticks and optional 'json'
    cleaned = raw_output.strip().removeprefix("```json").removesuffix("```").strip()
    
    # Parse into Python dict
    data = json.loads(cleaned)
    if type(data) == list:
        data = data[0]
    
    return data


#---------- Generate prompt ----------------

def generate_infographic_prompt(summary, pdf= True, title_pdf=False):

    title =  title_pdf['title'] if pdf else summary['title']
    print(title_pdf['organism_'])

    organism = title_pdf["organism_"] if pdf else summary['organism']
    layers = summary["layers"]

    prompt = f"""Create an isometric scientific infographic titled “{title}”, featuring vertically exploded layers aligned on a central axis, evenly spaced, and viewed from a 30° isometric camera angle on both X and Y axes.

Layout & Visual Style:
- Background: Flat grey (#CCCCCC) with a light isometric grid
- No shadows, no icons, no decorative elements
- Title: Bold, centered at the top: {title}

Top Layer (Organism/System):
- A photo-realistic rendering of the {organism}, viewed from above, centered.
- No background environment—only the grid.

Lower Layers (Functional Components, in black-and-white architectural line style):"""

    for layer in layers:
        prompt += f"""

- “{layer['name']}”
    - Left caption: “{layer['name']} – {layer['caption']}”
    - Right label: {layer['scale']}
    - Visual: {layer['visual']}"""

    prompt += """

Final Visual Instructions:
- Top layer: Full-color, photo-realistic
- Lower layers: Black-and-white line drawings
- Vertical black ruler on the right, aligned to scales
- Captions and labels outside the visuals, no overlaps
- Maintain blueprint-style visual consistency"""

    return prompt

#----------Generate image----------------

def generate_and_display_image(prompt, model="gpt-image-1", n=1, size="1024x1536", display_image=True):
    """
    Generate an image using OpenAI's image generation API and optionally display it.
    
    Args:
        prompt (str): The text prompt for image generation
        model (str): The OpenAI image model to use (default: "gpt-image-1")
        n (int): Number of images to generate (default: 1)
        size (str): Image size in format "widthxheight" (default: "1024x1536")
        display_image (bool): Whether to display the image in notebook (default: True)
    
    Returns:
        PIL.Image: The generated image as a PIL Image object
    """
    client = OpenAI()
    
    result = client.images.generate(
        model=model,
        prompt=prompt,
        n=n,
        size=size
    )
    
    image_base64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)
    image = PILImage.open(BytesIO(image_bytes))
    
    if display_image:
        image.show()  # This opens the image in your default image viewer

    
    return image

#---------- Save image ---------------
def save_image(image_data, filename, overwrite=False):
    """
    Save image data to a file.
    
    Args:
        image_data: Can be either:
            - bytes: Raw image bytes
            - PIL.Image: PIL Image object
        filename (str): Path and filename to save the image
        overwrite (bool): Whether to overwrite existing files (default: False)
    
    Returns:
        str: The full path where the image was saved
    
    Raises:
        FileExistsError: If file exists and overwrite=False
        ValueError: If image_data type is not supported
    """
    # Check if file exists and handle overwrite logic
    if os.path.exists(filename) and not overwrite:
        raise FileExistsError(f"File '{filename}' already exists. Set overwrite=True to replace it.")
    
    # Handle different input types
    if isinstance(image_data, bytes):
        # Save raw bytes directly
        with open(filename, "wb") as f:
            f.write(image_data)
    elif isinstance(image_data, PILImage.Image):
        # Save PIL Image object
        image_data.save(filename)
    else:
        raise ValueError(f"Unsupported image_data type: {type(image_data)}. Expected bytes or PIL.Image.")
    
    return os.path.abspath(filename)



#----- main code ---------
def main(json_path, pdf_path):
    # Load model data from JSON file
    model_data = load_json_data(json_path)
    
    # Extract summary from PDF if needed
    if os.path.exists(pdf_path):
        title_pdf = extract_pdf_summary(pdf_path)
        pdf = True
    else:
        title_pdf = {"title": "Default Title", "organism_": "Default Organism"}
        pdf = False
    
    # Generate prompt based on whether it's a single or multiple models
    if isinstance(model_data, dict) and "models" in model_data:
        models = model_data["models"]
        num_models = len(models)
        if num_models > 1:
            prompt = generate_summary_prompt_multiple(model_data, pdf_path)
        else:
            prompt = generate_summary_prompt_single(model_data)
    
    # Extract structured JSON content
    summary = extract_json_content(prompt)
    
    # Generate infographic prompt
    infographic_prompt = generate_infographic_prompt(summary, title_pdf, pdf)
    
    # Generate and display image
    image = generate_and_display_image(infographic_prompt)
    
    # Save the generated image
    save_image(image, "infographic.png", overwrite=True)

json_path = "models_water purification.json"  # Path to your JSON file
pdf_path = "water purification.pdf"  # Path to your PDF file (if applicable)
main(json_path, pdf_path)