from flask import Flask, request, jsonify,  flash, redirect, url_for
from transformers import AutoTokenizer, AutoModelForImageTextToText, BlipForConditionalGeneration, BlipProcessor
from PIL import Image
import os
from werkzeug.utils import secure_filename
def get_model(model_path):
    """Load a Hugging Face model and tokenizer from the specified directory"""
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    processor = BlipProcessor.from_pretrained(model_path)
    model = AutoModelForImageTextToText.from_pretrained(model_path)
    return model, processor, tokenizer


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
# Load the models and tokenizers for each supported language
captioning_model, captioning_processor, captioning_tokenizer = get_model('models/')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/Caption', methods=['POST'])
def Create_Caption():
    file = request.files['file']
    if not file or not allowed_file(file.filename):
        raise Exception("no file uploaded or file is not supported")

    processor = captioning_processor
    model = captioning_model.to("cuda")

    raw_image = Image.open(request.files['file'].stream).convert('RGB')

    # unconditional image captioning
    inputs = processor(raw_image, return_tensors="pt").to("cuda")

    out = model.generate(**inputs)
    print(processor.decode(out[0], skip_special_tokens=True))
    return_result2 = processor.decode(out[0], skip_special_tokens=True)
    #language model sometimes throws in these words.
    return_result2 = return_result2.replace('araffe', '')
    return_result2 = return_result2.replace('arafed ', '')


    return jsonify({f'result': return_result2})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000, debug=True)
