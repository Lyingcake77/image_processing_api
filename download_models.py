from transformers import AutoTokenizer, AutoModelForImageTextToText, BlipProcessor
import os

def download_model(model_path, model_name):
    """Download a Hugging Face model and tokenizer to the specified directory"""
    # Check if the directory already exists
    if not os.path.exists(model_path):
        # Create the directory
        os.makedirs(model_path)

    processor = BlipProcessor.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForImageTextToText.from_pretrained(model_name)

    # Save the model and tokenizer to the specified directory
    processor.save_pretrained(model_path)
    model.save_pretrained(model_path)
    tokenizer.save_pretrained(model_path)

# For this demo, download the English-French and French-English models
download_model('models/', 'Salesforce/blip-image-captioning-large')
#download_model('models/fr_en/', 'Helsinki-NLP/opus-mt-fr-en')