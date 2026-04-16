## Invoice Processing ML Pipeline
A production style end-to-end invoice processing system that extracts structured information from PDF invoices using OCR, image preprocessing and rule-based parsing and exposes the workflow through a FastAPI service.

## Table of Contents
-[Project Overview](#project-overview)
-[Problem Statement](#problem-statement)
-[Solution Overview](#solution-overview)
-[Key Features](#key-features)
-[Technology stack](#technology-stack)
-[Workflow](#workflow)
-[Supported Input](#supported-input)
-[Current Scope](#current-scope)
-[Example API Response](#example-api-response)
-[Setup Instructions](#setup-instructions)
-[Environment configuaration](#environment-configuration)

---
## Project Overview

This project processes invoice PDFs and converts them into structured JSON output. It is designed as a modular pipeline with clearly separated stages for ingestion, preprocessing, OCR, extraction and API exposure.

The goal is to simulate real-world business automation use case where invoice data must be extracted automatically for systems such as finance, ERP, analytics, etc

---
## Problem Statement

Invoice documents are often received as PDFs and many of them are semi-structured or image based. This makes direct extraction difficult because,

-PDFs may not contain clean machine readable text
-OCR quality could vary depending on document quality
-Extracted text is often noisy and not properly structured
-Businesses requires structured output for example invoice number, date, total amount, line items, etc

The objective of this project is to build an end-to-end pipeline that takes an invoice PDF as input and returns structured invoice data as JSON.

---
## Solution Overview

The system performs the following steps:
1. Accept a PDF invoice
2. Convert PDF pages into images
3. Preprocess the images to improve OCR quality
4. Extract text using Tesseract OCR
5. Parse the OCR text into structured invoice fields
6. Return the extracted result through a REST API

This project currently focuses on **clean digital invoice templates** as the primary supported format.

---
## Key Features

-PDF to image conversion
-Image preprocessing using OpenCV
-OCR text extraction using Tesseract
-Rule-based extraction of key invoice fields
-Batch pipeline support for processing multiple documents
-FastAPI endpoint for uploading and processing invoices
-Modular code structure suitable for extension
