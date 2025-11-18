Image Storage Microservice – Instructions

Overview:

This Python-based microservice allows a client to upload image files (as Base64-encoded JSON) and retrieve those images later.
Images are stored locally on the server in the images/ directory.
The service uses the Flask framework and communicates via HTTP requests returning JSON responses.

1. Requirements

  Python 3.8 or newer
  
  The following Python packages (install via pip):
  pip install flask requests

  A local image file (e.g., cat.png) in the same directory as the scripts.

2. File Structure
    ASSIGNMENT7/
    │
    ├── image_service.py      ← Flask microservice
    ├── testfiles.py          ← Client test script *(just for testing)
    ├── images/               ← Folder where uploaded images are saved
    ├── cat.png               ← Example image to test *(just for testing)
    └── README.txt            ← This instruction file

3. How to Run the Service

  Open a terminal and navigate to this directory.
  
  Start the Flask service:
      python image_service.py
  You should see:
      * Running on http://127.0.0.1:5000
  Leave this terminal running — it hosts your microservice.

4. How to Run the Client Test

  Open a second terminal in the same directory.
  
  Run:
    python testfiles.py
  Expected output:
    Starting test script...
    Upload status: 200
    Upload response: {"message":"Saved 1 image(s)","saved_files":["cat.png"]}
    Retrieve status: 200
    ✅ Saved cat_retrieved.png successfully.

  After it runs, you’ll see a new file cat_retrieved.png confirming the round-trip worked.

5. JSON Request Formats
Upload (POST /upload)

Request body:
    {
      "images": [
        {
          "filename": "cat.png",
          "image_data": "<base64 encoded string>"
        }
      ]
    }
Response:
    {
      "message": "Saved 1 image(s)",
      "saved_files": ["cat.png"]
    }

Retrieve (POST /get)

Request body:
    {
      "filenames": ["cat.png"]
    }

Response
    {
      "count": 1,
      "images": [
        {
          "filename": "cat.png",
          "image_data": "<base64 encoded string>"
        }
      ]
    }
          
6. Notes

  Files are saved in the local images/ directory.
  
  The service only runs locally (http://127.0.0.1:5000).
  
  To test with multiple images, modify testfiles.py and add more entries under "images".
  
  Base64 encoding allows binary data to be transferred safely inside JSON, but it increases size by ~33%.
  
  For production or large images, a multipart/form-data upload would be more efficient.    

7. UML
  
  Client                Flask Microservice            OS File System
    |                           |                            |
    |---- POST /upload -------->|                            |
    |    JSON {images[...] }    |                            |
    |                           |-- write files to /images -->|
    |                           |                            |
    |<--- JSON response --------|                            |
    |   {"message": "..."}      |                            |
    |                           |                            |
    |---- POST /get ----------->|                            |
    |    JSON {filenames[]}     |                            |
    |                           |-- read files from /images->|
    |                           |                            |
    |<--- JSON response --------|                            |
    |   {count, images[...] }   |                            |
    |                           |                            |

