from flask import Flask, render_template, request, jsonify
from color_analysis import extract_dominant_colors

app = Flask(__name__)

@app.route('/')
def index():
    # This could render a page with a form to upload an image, etc.
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    # Assuming you're sending an image file via a POST request.
    # Save the file and pass the file path to the color analysis function.
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided.'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file.'}), 400

    # Save the file to a temporary location (or process it in-memory)
    image_path = f"./static/uploads/{file.filename}"
    file.save(image_path)

    # Run the color analysis function
    colors = extract_dominant_colors(image_path)
    
    # Return the colors as JSON
    return jsonify({'colors': colors.tolist()})

if __name__ == '__main__':
    app.run(debug=True)