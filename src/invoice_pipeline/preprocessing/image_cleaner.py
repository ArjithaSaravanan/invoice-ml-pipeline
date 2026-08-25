import cv2
from pathlib import Path

# These are methods I'm experimenting with when comparing OCR results.
SUPPORTED_METHODS = ["adaptive", "otsu", "simple", "median"]

def preprocess_image(
    image_path:str, 
    output_path: str, 
    method: str = "adaptive"
    ) -> str:
    """
    Clean and preprocess the image for better OCR accuracy.
    """
    if method not in SUPPORTED_METHODS:
        raise ValueError(
            f"Unsupported preprocessing method: {method}"
            f"Supported methods are: {SUPPORTED_METHODS}")

    img = cv2.imread(image_path)

    # If OpenCV cannot read the file, cvtColor() below gives an unhelpful
    # error. So we check if img is None and raise a more informative error.
    if img is None:
        raise ValueError(f"Could not read image at {image_path}")

    # Convert to grayscale because OCR works better on single channel images
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # A small blur to reduce noise before thresholding. This can help with OCR accuracy.
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply different preprocessing strategies based on the method
    if method == "adaptive":
        processed = cv2.adaptiveThreshold(
            blur, 
            255, 
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 
            15, 
            3
        )
    elif method == "otsu":
        processed = cv2.threshold(
            blur,
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )[1]
    elif method == "simple":
        # This is deliberately kept simple. It gives me a useful baseline
        # for comparison with other methods.
        processed = cv2.threshold(
            blur, 
            150, 
            255, 
            cv2.THRESH_BINARY
        )[1]
    elif method == "median":
        # Median filtering is useful for some noisy scans. Here I'm using it before
        # Otsu's thresholding to see if it improves OCR results on certain documents.
        median = cv2.medianBlur(gray, 3)
        processed = cv2.threshold(
            median, 
            0, 
            255, 
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )[1]

    #kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    #thresh = cv2.dilate(thresh, kernel, iterations=1)
    # Keep generated files out of the source tree if the caller gives
    # us a nested output path.
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    if not cv2.imwrite(output_path, processed):
        raise IOError(f"Failed to write processed image to {output_path}")

    return output_path