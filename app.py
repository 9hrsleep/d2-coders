from flask import Flask, render_template, request, redirect, url_for
import os
from color_analysis import dominant_RGB

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

    # Create the 'uploads' folder if it doesn't exist
    uploads_folder = "static/uploads/"
    os.makedirs(uploads_folder, exist_ok=True)

    # Save the file in the 'uploads' folder
    file_path = os.path.join(uploads_folder, file.filename)
    file.save(file_path)

    # Extract dominant colors from the uploaded image
    colors = dominant_RGB(file_path)

    # After processing the file, redirect to the report page with the image path
    return redirect(url_for('report', image_path=file_path, colors = colors))

@app.route("/report")
def report():
    # Get the image path passed as a query parameter
    image_path = request.args.get('image_path', None)
    colors = request.args.getlist('colors') 
   
    colors = [tuple(map(int, color.strip('[]').replace(' ', '').split(','))) for color in colors]

    # Provide default data for the report (replace this as necessary)
    return render_template("report.html",
                           image_url=image_path,  # Dynamically set the image
                           analytics_text="This ad performs well with audience aged 18-25...",
                           color_palette=colors)

if __name__ == "__main__":
    app.run(debug=True)
