import cv2
from pathlib import Path

def preprocess_image(image_path:str, output_path: str):
    """
    Clean and preprocess the image for better OCR accuracy.
    """
    img = cv2.imread(image_path)
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #Reduce noise
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # Adaptive thresholding
    thresh = cv2.adaptiveThreshold(
        blur, 
        255, 
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 
        15, 
        3
    )
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    #thresh = cv2.dilate(thresh, kernel, iterations=1)
    # Save the cleaned image
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(output_path, thresh)

    return output_path