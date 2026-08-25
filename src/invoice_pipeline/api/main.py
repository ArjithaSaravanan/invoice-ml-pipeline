from fastapi import FastAPI, UploadFile, File, HTTPException
import shutil
from uuid import uuid4
from pathlib import Path
from invoice_pipeline.pipeline.runner import process_single_pdf

app = FastAPI()

UPLOAD_DIR = Path("temp_uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@app.post("/v1/invoice/process/")
async def process_invoice(file: UploadFile = File(...)):
    file_path = UPLOAD_DIR / file.filename

    if not file.filename:
        raise HTTPException(
            status_code=400, 
            detail="No filename supplied."
        )

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400, 
            detail="Only PDF files are supported."
        )   

    temp_filename = f"{uuid4().hex}.pdf"
    file_path = UPLOAD_DIR / temp_filename

    try:
        # Save the uploaded file tempoarily to the server
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        # Process the PDF and extract data
        result = process_single_pdf(
            pdf_path=str(file_path), 
            processed_root="data/processed", 
            output_root="outputs"
        )
    
        if result["status"] == "failed":
            raise HTTPException(
                status_code=500, 
                detail=result["error"]
            )
        if result["status"] == "unsupported":
            raise HTTPException(
                status_code=422, 
                detail=result["error"]
            )

        return {
            "status": result["status"],
            "file_name": file.filename,
            "data": result["extracted_data"],
            "document_type": result["document_type"]
        }
    finally:
        # The uploaded PDF is only needed while processing.
        # Clean up the temporary file
        file_path.unlink(missing_ok=True)
