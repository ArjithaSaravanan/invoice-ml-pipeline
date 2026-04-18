## Invoice Processing Pipeline (OCR + FastAPI)
A beginner-friendly project where I built an end-to-end invoice processing system that extracts structured information from PDF invoices using OCR, preprocesses the image and applies rule-based parsing and exposes the workflow through a FastAPI service.

## Problem Statement
Invoice documents are often received as PDFs and many of them are semi-structured or image based. This makes direct extraction difficult because,
- PDFs may not contain clean machine readable text
- OCR quality could vary depending on document quality
- Extracted text is often noisy and not properly structured
- Businesses requires structured output for example invoice number, date, total amount, line items
The objective of this project is to build an end-to-end pipeline that takes an invoice PDF as input and returns structured invoice data as JSON.

## Project Overview
The system performs the following steps:
1. Accept a PDF invoice
2. Convert PDF pages into images
3. Preprocess the images to improve OCR quality
4. Extract text using Tesseract OCR
5. Parse the OCR text into structured invoice fields
6. Returns the extracted result through a REST API
This project currently focuses on **clean digital invoice templates** as the primary supported format.
Example output:
```json
{
  "invoice_number": "INV-1001",
  "date": "2026-04-15",
  "total_amount": 900,
  "items": [
    {
      "item": "Software Development",
      "quantity": 10,
      "price": 50,
      "total": 500
    }
  ]
}
```
## How I approached it
# 1. PDF to Image Conversion
Since OCR works on images and not directly on PDFs, I used `pdf2image` to convert each page of the invoice into an image.
This standardized the input format allowing further image processing.

# 2. Image Preprocessing
Raw images from PDFs often contain noise or low contrast, which reduces OCR accuracy. To improve this, I applied:
  - grayscale conversion
  - thresholding
  - basic noise reduction
These steps helped make the text more readable for the OCR engine.

# 3. OCR (Text Extraction)
I used **Tesseract OCR** to extract text from th eprocessed images.
During this step, I faced challenges such as broken words, incorrect characters and inconsistent spacing. This made it clear that OCR output is rarely perfect and needs further processing.

# 4. Field Extraction
After extracting raw text, I implemented simple parsing logic to identify key fields such as:
  - invoice number
  - date
  - total amount
For this, I used keyword matching and basic pattern matching (regex).
For item-level data, I attempted to extract structured rows, though this part can vary depending on invoice format.

# 5. API (FastAPI)
To make the pipeline usable, I exposed it through a FastAPI REST API.
**Endpoint**
```
POST /v1/invoice/process
```
Users can upload an invoice PDF and receive strctured JSON in response.
This step helped me understand how to integrate data pipelines into real-world services.

## Tech Stack
- Python
- Tesseract OCR
- OpenCV
- FastAPI
- pdf2image

## Limitations
- Works best with simple and clean invoice formats
- OCR accuracy depends on image quality and formatting
- Parsing logic is rule-based and may not generalize to all layouts
- Item extraction can be inconsistent across different invoice styles

## What I learned
- How OCR works in real-world scenarios and its limitations
- Importance of preprocessing in improving test extraction
- Challenges of converting unstructured data into structured formats
- Designing modular pipelines for document processing
- Exposing data pipelines as APIs using FastAPI

## What I would improve next
- Support multiple invoice formats more robustly
- Improve item table extraction
- Replace rule-based parsing with ML-based approaches
- Integrate with a document classification model

## How to run
```
pip install -r requirements.txt
uvicorn src.api.main:app --reload
```
Open:
```
http://127.0.0.1:8000/docs
```
Upload an invoice PDF and test the pipeline

## Prerequisites
**Tesseract OCR**
Install Tesseract and add it to your system PATH
**Poppler (for PDF processing)**
Required for `pdf2image`
  **Windows**
  Download: [Poppler-Windows](https://github.com/oschwartz10612/poppler-windows/releases/)
  Add the `bin` folder to PATH.









