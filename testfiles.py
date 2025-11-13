import requests, base64, json, os

print("Starting test script...")

print("Starting test script...")

BASE_URL = "http://127.0.0.1:5000"
img_path = "cat.png"

# ✅ Confirm the file exists before upload
if not os.path.exists(img_path):
    raise FileNotFoundError(f"{img_path} not found in {os.getcwd()}")

# ✅ Encode to base64 string
with open(img_path, "rb") as f:
    encoded = base64.b64encode(f.read()).decode("utf-8")

# ✅ Build JSON payload
upload_data = {
    "images": [
        {
            "filename": "cat.png",
            "image_data": encoded
        }
    ]
}

print("Uploading image...")
r = requests.post(f"{BASE_URL}/upload", json=upload_data)
print("Upload status:", r.status_code)
print("Upload response:", r.text)

# ✅ Retrieve
get_data = {"filenames": ["cat.png"]}
print("\nRetrieving image...")
r = requests.post(f"{BASE_URL}/get", json=get_data)
print("Retrieve status:", r.status_code)
result = r.json()
print(json.dumps(result, indent=2))

# ✅ Decode image back to confirm
if "images" in result:
    img_b64 = result["images"][0]["image_data"]
    with open("cat_retrieved.png", "wb") as f:
        f.write(base64.b64decode(img_b64))
    print("\n✅ Saved cat_retrieved.png successfully.")
else:
    print("\n⚠️  No images returned:", result)