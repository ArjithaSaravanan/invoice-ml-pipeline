import os
from pathlib import Path
from invoice_pipeline.ingestion.pdf_loader import convert_pdf_to_images

def test_convert_pdf_to_images():
    """Test that convert_pdf_to_images function works correctly."""
    # Check if sample PDF exists
    pdf_path = "data/raw/sample_invoice.pdf"
    output_folder = "data/processed/"
    
    # Only run test if sample PDF exists
    if os.path.exists(pdf_path):
        images = convert_pdf_to_images(pdf_path, output_folder)
        assert isinstance(images, list), "Expected list of image paths"
        assert len(images) > 0, "Expected at least one image"
        
        # Check that image files exist
        for img_path in images:
            assert os.path.exists(img_path), f"Image file not created: {img_path}"
    else:
        print(f"Warning: Sample PDF not found at {pdf_path}. Test skipped.")

if __name__ == "__main__":
    test_convert_pdf_to_images()