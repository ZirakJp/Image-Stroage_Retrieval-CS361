
# Image service should be able to receive a JSON with image data

from flask import Flask, request, jsonify
import base64
import os
from werkzeug.utils import secure_filename   # FIX: added for filename sanitization

app = Flask(__name__)
IMAGE_DIR = "images"
os.makedirs(IMAGE_DIR, exist_ok=True)

# ✅ FIX: define allowed extensions for content type validation
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

# ✅ FIX: helper function for extension validation
def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )

# ✅ FIX: extracted helper function to consolidate duplicate logic
def save_image(filename, image_data):
    filename = secure_filename(filename)   # FIX: sanitize filename
    if not allowed_file(filename):         # FIX: validate extension
        raise ValueError("Invalid file type")
    try:
        image_bytes = base64.b64decode(image_data)   # FIX: wrapped in try/except
    except Exception:
        raise ValueError("Invalid base64 data")
    path = os.path.join(IMAGE_DIR, filename)
    with open(path, 'wb') as f:
        f.write(image_bytes)
    return filename

@app.route('/upload', methods=['POST'])
def upload_images():
    """
    Expects JSON:
    {
        "images": [
            {"filename": "one.png", "image_data": "<base64 string>"},
            {"filename": "two.png", "image_data": "<base64 string>"}
        ]
    }
    """
    request_data = request.get_json()   # FIX: renamed from "data" → clearer
    images = request_data.get('images', [])
    if not isinstance(images, list):
        return jsonify({"error": "Invalid 'images' list"}), 400

    saved_files = []   # FIX: renamed from "saved" → clearer
    for entry in images:   # FIX: renamed from "item" → clearer
        try:
            saved_files.append(save_image(entry['filename'], entry['image_data']))
        except Exception as e:
            return jsonify({"error": str(e)}), 400   # FIX: explicit error return

    return jsonify({
        "message": f"Saved {len(saved_files)} image(s)",
        "saved_files": saved_files
    }), 200


@app.route('/get', methods=['POST'])
def get_images():
    """
    Expects JSON:
    {
        "filenames": ["one.png", "two.png"]
    }
    Returns:
    {
        "images": [
            {"filename": "one.png", "image_data": "<base64 string>"},
            {"filename": "two.png", "image_data": "<base64 string>"}
        ]
    }
    """
    request_data = request.get_json()   # FIX: renamed from "data" → clearer
    filenames = request_data.get('filenames')

    if not filenames or not isinstance(filenames, list):
        return jsonify({"error": "Missing or invalid 'filenames' list"}), 400

    results = []
    for filename in filenames:
        filename = secure_filename(filename)   # FIX: sanitize filename
        if not allowed_file(filename):         # FIX: validate extension
            continue
        path = os.path.join(IMAGE_DIR, filename)
        if not os.path.exists(path):
            continue
        with open(path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')
        results.append({"filename": filename, "image_data": image_data})

    return jsonify({"images": results, "count": len(results)}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

