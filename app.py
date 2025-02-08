from flask import Flask, render_template, request, jsonify
from color_analysis import extract_dominant_colors

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    if "file" not in request.files:
        return "No file uploaded", 400
    
    file = request.files["file"]
    if file.filename == "":
        return "No selected file", 400

    file_path = "uploaded_image.jpg"
    file.save(file_path)
    
    colors = extract_dominant_colors(file_path)
    return render_template("index.html", colors=colors)

if __name__ == "__main__":
    app.run(debug=True)