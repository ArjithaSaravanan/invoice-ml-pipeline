from fastapi import FastAPI, UploadFile, File
import shutil
from pathlib import Path
from invoice_pipeline.pipeline.runner import process_single_pdf

app = FastAPI()

UPLOAD_DIR = Path("temp_uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/v1/invoice/process/")
async def process_invoice(file: UploadFile = File(...)):
    file_path = UPLOAD_DIR / file.filename
    # Save the uploaded file to disk 
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    # Process the PDF and extract data
    result = process_single_pdf(
        pdf_path=str(file_path), 
        processed_root="data/processed", 
        output_root="outputs"
    )
    if result["status"] == "failed":
        return {
            "status": "error",
            "message": result["error"]
        }

    return {
        "status": result["status"],
        "file_name": result["file_name"],
        "data": result["extracted_data"],
    }
