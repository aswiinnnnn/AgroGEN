import google.generativeai as genai
import streamlit as st
import wikipediaapi
import re

# Configure the GenerativeAI API key directly (not recommended for production)
api_key = "AIzaSyD6xhmLNlIANCW7ouSbWQ4h9k28amJufic"
genai.configure(api_key=api_key)

# Set up the model configuration for text generation
generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}

# Define safety settings for content generation
safety_settings = [
    {"category": f"HARM_CATEGORY_{category}", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
    for category in ["HARASSMENT", "HATE_SPEECH", "SEXUALLY_EXPLICIT", "DANGEROUS_CONTENT"]
]

# Initialize the GenerativeModel with the updated model name
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",  # Updated model name
    generation_config=generation_config,
    safety_settings=safety_settings,
    system_instruction="you should provide output in a layman terms.If there is no disease say that only. you should say the name of the plant and disease in 150 words with appropriate prescription.give me treatment method and medicine dosage on your own.write in this format:\nDisease description:in layman terms\nTreatment and Dosage in unit of Fungicide ,you should not say to follow the instruction in the package instead you recomend dosage by researching:in short\nPrevention and precaution:in short"
)

# Function to generate a response based on a prompt and an uploaded image
def generate_gemini_response(prompt, image_file):
    image_data = image_file.read()
    mime_type = image_file.type  # Dynamically get MIME type
    response = model.generate_content([prompt, {"mime_type": mime_type, "data": image_data}])
    return response.text

# Function to search Wikipedia for a given query
def search_wikipedia(query):
    wiki_wiki = wikipediaapi.Wikipedia('en')
    page = wiki_wiki.page(query)
    if page.exists():
        return page.summary
    return "No information found."

# Function to extract plant and disease names from the model's response
def extract_plant_disease_names(response):
    # Example response format: "The plant is Tomato, and it has Blight."
    match = re.search(r'The plant is (.*?), and it has (.*?).', response)
    if match:
        plant_name = match.group(1).strip()
        disease_name = match.group(2).strip()
        return plant_name, disease_name
    return None, None

# Function for the Streamlit application
def disease():
    st.title("AgriGEN - Plant Disease Analysis Tool")
    
    # File uploader for images
    uploaded_files = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            # Generate response to identify the plant and disease
            input_prompt = f"Analyze the uploaded image and identify the plant and any diseases present."
            response = generate_gemini_response(input_prompt, uploaded_file)
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
            st.subheader("Model Analysis Result:")
            st.write(response)

            # Extract plant and disease names from the model's response
            plant_name, disease_name = extract_plant_disease_names(response)

            if plant_name and disease_name:
                # Search Wikipedia for the identified plant and disease
                wiki_summary_plant = search_wikipedia(plant_name)
                wiki_summary_disease = search_wikipedia(disease_name)

                st.subheader(f"Information on {plant_name}:")
                st.write(wiki_summary_plant)

                st.subheader(f"Information on {disease_name}:")
                st.write(wiki_summary_disease)

# Run the disease function when the script is executed
if __name__ == "__main__":
    disease()
