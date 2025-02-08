from flask import Flask, render_template, request
from color_analysis import dominant_RGB

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    # Check if both files are uploaded
    if "logo" not in request.files or "advertisement" not in request.files:
        return "Both files are required", 400
    
    logo_file = request.files["logo"]
    advertisement_file = request.files["advertisement"]

    # Check if files have a filename
    if logo_file.filename == "" or advertisement_file.filename == "":
        return "No file selected", 400

    # Save the logo and advertisement files
    logo_path = "static/uploads/uploaded_logo.jpg"
    advertisement_path = "static/uploads/uploaded_advertisement.jpg"
    logo_file.save(logo_path)
    advertisement_file.save(advertisement_path)
    
    # Optionally process the logo to extract dominant colors
    logo_colors = dominant_RGB(logo_path)

    # Render the report page and pass the file paths and extracted colors
    return render_template("report.html",
                           image_url=logo_path,  # Path for the company logo image
                           ad_image_url=advertisement_path,  # Path for the advertisement image
                           analytics_text="This ad performs well with audience aged 18-25...",
                           color_palette=logo_colors)  # Use the colors extracted from the logo

@app.route("/report")
def report():
    # Since the values are directly passed from analyze, no need to get them from query params.
    image_url = request.args.get('image_url')  # Logo image path
    ad_image_url = request.args.get('ad_image_url')  # Advertisement image path
    color_palette = request.args.getlist('color_palette')  # Color palette
    
    # If color palette is passed as a string, we need to process it to a list of tuples
    if color_palette:
        color_palette = [tuple(map(int, color.strip('[]').replace(' ', '').split(','))) for color in color_palette]

    # Render the report page with images and color palette
    return render_template("report.html",
                           image_url=image_url,
                           ad_image_url=ad_image_url,
                           analytics_text="This ad performs well with audience aged 18-25...",
                           color_palette=color_palette)

if __name__ == "__main__":
    app.run(debug=True)
