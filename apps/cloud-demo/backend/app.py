from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from pathlib import Path
import shutil

app = FastAPI(title="Cloud Storage API")

STORAGE_DIR = Path("./storage")
STORAGE_DIR.mkdir(parents=True, exist_ok=True)


@app.get("/")
def health_check():
    return {
        "status": "ok",
        "service": "cloud-storage",
        "message": "Cloud storage API is running"
    }


@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    file_path = STORAGE_DIR / file.filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "File uploaded successfully",
        "filename": file.filename
    }


@app.get("/files")
def list_files():
    files = [file.name for file in STORAGE_DIR.iterdir() if file.is_file()]
    return {"files": files}


@app.get("/download/{filename}")
def download_file(filename: str):
    file_path = STORAGE_DIR / filename

    if not file_path.exists():
        return {"error": "File not found"}

    return FileResponse(file_path, filename=filename)


@app.delete("/files/{filename}")
def delete_file(filename: str):
    file_path = STORAGE_DIR / filename

    if not file_path.exists():
        return {"error": "File not found"}

    file_path.unlink()

    return {
        "message": "File deleted successfully",
        "filename": filename
    }
