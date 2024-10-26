from flask import Flask, request, jsonify, render_template  # Import necessary modules from Flask
import os  # Import os module for operating system functions
import pytesseract  # Import pytesseract for Optical Character Recognition (OCR)
from PIL import Image  # Import Image module from PIL for image processing
import cohere  # Import Cohere for text generation

# Set the path for Tesseract OCR executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Initialize the Flask application
app = Flask(__name__, template_folder='templates')  # Specify the template folder

# Set your Cohere API key for text generation
API_KEY = 'mIHHVjLSPFLw9YZitQHCQ5ADhvjNx55B8Tl703Qe'  # Replace with your actual API key
co = cohere.ClientV2(API_KEY)  # Initialize the Cohere client with the API key

@app.route('/')  # Define the route for the home page
def home():
    return render_template('index.html')  # Render the index.html template

@app.route('/ask', methods=['POST'])  # Define the route for handling POST requests to /ask
def ask():
    try:
        image = request.files.get('image')  # Get the uploaded image file from the request
        
        # Hardcoded prompt for the AI model
        prompt = "make this food label understand  with use of visual emojis and household quantities like tea spoon etc (make sure at last give 'rating:' out of 100)"  

        if image:  # Check if an image was uploaded
            # Open the image using PIL
            img = Image.open(image)
            # Extract text from the image using Tesseract OCR
            extracted_text = pytesseract.image_to_string(img)

            # Combine the extracted text with the hardcoded prompt
            extracted_text += ' ' + prompt

            # Create a request to generate a response using the Cohere API
            response = co.generate(
                model='command-r-plus-08-2024',  # Specify the model to use
                prompt=extracted_text,  # Provide the combined prompt
                max_tokens=512,  # Set the maximum number of tokens in the response
                temperature=0.7,  # Set the temperature for randomness in response
                stop_sequences=[],  # Specify stop sequences (empty in this case)
            )

            # Return a JSON response with the extracted text and AI-generated response
            return jsonify({'user': extracted_text, 'ai': response.generations[0].text})

        # If no image is provided, just use the hardcoded prompt
        else:
            # Generate a response using the Cohere API with the hardcoded prompt
            response = co.generate(
                model='command-r-plus-08-2024',  # Specify the model to use
                prompt=prompt,  # Provide the hardcoded prompt
                max_tokens=512,  # Set the maximum number of tokens in the response
                temperature=0.7,  # Set the temperature for randomness in response
                stop_sequences=[],  # Specify stop sequences (empty in this case)
            )

            # Return a JSON response with the prompt and AI-generated response
            return jsonify({'user': prompt, 'ai': response.generations[0].text})

    except Exception as e:  # Catch any exceptions that occur
        # Return a JSON response with the error message
        return jsonify({'error': str(e)}), 500  # Return a 500 status code for server error

if __name__ == "__main__":  # Check if the script is being run directly
    app.run(debug=True, port=5000)  # Run the Flask application in debug mode on port 5000