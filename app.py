from flask import Flask, request, render_template, send_from_directory
from PIL import Image
import pillow_heif
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def convert_heic_to_jpg(input_path):
    output_path = os.path.splitext(input_path)[0] + '.jpg'
    heif_file = pillow_heif.open_heif(input_path)
    img = Image.frombytes(
        heif_file.mode, 
        heif_file.size, 
        heif_file.data, 
        "raw", 
        heif_file.mode, 
        heif_file.stride
    )
    img.save(output_path, "JPEG")
    return output_path

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        files = request.files.getlist("file")
        converted_files = []
        for file in files:
            if file.filename.endswith(".heic"):
                file_path = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(file_path)
                jpg_path = convert_heic_to_jpg(file_path)
                converted_files.append(os.path.basename(jpg_path))

        return render_template("download.html", files=converted_files)
    return render_template("index.html")

@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
