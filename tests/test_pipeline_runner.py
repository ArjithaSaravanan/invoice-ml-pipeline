from pathlib import Path
import pytest
from invoice_pipeline.pipeline.runner import process_single_pdf

SAMPLE_INVOICE = "data/raw/digital/clean_template/sample_invoice.pdf"

@pytest.mark.skipif(
    not Path(SAMPLE_INVOICE).exists(),
    reason=f"Sample invoice not found at {SAMPLE_INVOICE}. Please ensure the file exists."
)
def test_process_single_pdf(tmp_path):
    """
    Test the process_single_pdf function with a sample invoice PDF.

    This is intentionally a small integration test that runs the entire 
    pipeline on a single PDF. It checks that the function completes 
    successfully and returns the expected keys in the result dictionary.
    """
    processed_root = tmp_path / "processed"
    output_root = tmp_path / "outputs"

    result = process_single_pdf(
        pdf_path=str(SAMPLE_INVOICE), 
        processed_root=str(processed_root), 
        output_root=str(output_root)
    )

    assert result["status"] == "success"
    assert result["extracted_data"] is not None
    assert result["error"] is None