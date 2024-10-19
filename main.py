from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
import os

app = FastAPI()

# Create necessary directories if they don't exist
os.makedirs("static", exist_ok=True)
os.makedirs("images", exist_ok=True)

# Serve static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve animal images
app.mount("/images", StaticFiles(directory="images"), name="images")

# Create index.html if it doesn't exist
index_html_path = os.path.join("static", "index.html")
if not os.path.exists(index_html_path):
    with open(index_html_path, "w") as f:
        f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ERA V3 Session 2 - Assignment</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
    </style>
</head>
<body class="min-h-screen flex items-center justify-center">
    <div class="bg-white rounded-lg shadow-2xl p-8 m-4 w-full max-w-3xl">
        <h1 class="text-4xl font-bold mb-8 text-center text-purple-600">ERA V3 Session 2 - Assignment</h1>
        
        <div class="mb-8 p-6 bg-purple-100 rounded-lg shadow-inner">
            <h2 class="text-2xl font-semibold mb-4 text-purple-800">Select an Animal</h2>
            <div class="flex justify-around mb-4">
                <label class="inline-flex items-center">
                    <input type="checkbox" name="animal" value="cat" class="form-checkbox h-5 w-5 text-purple-600">
                    <span class="ml-2 text-lg">Cat</span>
                </label>
                <label class="inline-flex items-center">
                    <input type="checkbox" name="animal" value="dog" class="form-checkbox h-5 w-5 text-purple-600">
                    <span class="ml-2 text-lg">Dog</span>
                </label>
                <label class="inline-flex items-center">
                    <input type="checkbox" name="animal" value="elephant" class="form-checkbox h-5 w-5 text-purple-600">
                    <span class="ml-2 text-lg">Elephant</span>
                </label>
            </div>
            <img id="animalImage" src="" alt="Animal Image" class="mx-auto hidden max-w-full h-auto rounded-lg shadow-lg">
        </div>

        <div class="p-6 bg-purple-100 rounded-lg shadow-inner">
            <h2 class="text-2xl font-semibold mb-4 text-purple-800">Upload a File</h2>
            <input type="file" id="fileInput" class="mb-4 p-2 w-full border border-purple-300 rounded">
            <div id="fileInfo" class="text-purple-800"></div>
        </div>
    </div>

    <script src="/static/script.js"></script>
</body>
</html>
""")

# Create script.js if it doesn't exist
script_js_path = os.path.join("static", "script.js")
if not os.path.exists(script_js_path):
    with open(script_js_path, "w") as f:
        f.write("""document.addEventListener('DOMContentLoaded', () => {
    const animalCheckboxes = document.querySelectorAll('input[name="animal"]');
    const animalImage = document.getElementById('animalImage');
    const fileInput = document.getElementById('fileInput');
    const fileInfo = document.getElementById('fileInfo');

    animalCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', (e) => {
            animalCheckboxes.forEach(cb => {
                if (cb !== e.target) cb.checked = false;
            });

            const animal = e.target.value;
            if (e.target.checked) {
                animalImage.src = `/images/${animal}.jpg`;
                animalImage.style.display = 'block';
            } else {
                animalImage.style.display = 'none';
            }
        });
    });

    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            const formData = new FormData();
            formData.append('file', file);

            fetch('/upload_file', {
                method: 'POST',
                body: formData
            })
                .then(response => response.json())
                .then(data => {
                    fileInfo.innerHTML = `
                        <p class="text-lg"><span class="font-bold">File Name:</span> ${data.filename}</p>
                        <p class="text-lg"><span class="font-bold">File Size:</span> ${data.file_size} bytes</p>
                        <p class="text-lg"><span class="font-bold">File Type:</span> ${data.file_type}</p>
                    `;
                })
                .catch(error => console.error('Error:', error));
        }
    });
});
""")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open(index_html_path, "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.post("/upload_file")
async def upload_file(file: UploadFile = File(...)):
    file_size = file.file.seek(0, 2)
    file.file.seek(0)
    
    return {
        "filename": file.filename,
        "file_size": file_size,
        "file_type": file.content_type
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
