
# Image service should be able to receive a JSON with image data

from flask import Flask, request, jsonify
import base64
import os

app = Flask(__name__)
IMAGE_DIR = "images"
os.makedirs(IMAGE_DIR, exist_ok=True)

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
    data = request.get_json()
    images = data.get('images')

    if not images or not isinstance(images, list):
        return jsonify({"error": "Missing or invalid 'images' list"}), 400

    saved = []
    for item in images:
        filename = item.get('filename')
        image_data = item.get('image_data')
        if not filename or not image_data:
            continue

        image_bytes = base64.b64decode(image_data)
        path = os.path.join(IMAGE_DIR, filename)
        with open(path, 'wb') as f:
            f.write(image_bytes)
        saved.append(filename)

    return jsonify({"message": f"Saved {len(saved)} image(s)", "saved_files": saved}), 200


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
    data = request.get_json()
    filenames = data.get('filenames')

    if not filenames or not isinstance(filenames, list):
        return jsonify({"error": "Missing or invalid 'filenames' list"}), 400

    results = []
    for filename in filenames:
        path = os.path.join(IMAGE_DIR, filename)
        if not os.path.exists(path):
            continue
        with open(path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')
        results.append({"filename": filename, "image_data": image_data})

    return jsonify({"images": results, "count": len(results)}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

