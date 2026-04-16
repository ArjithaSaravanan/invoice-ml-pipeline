from invoice_pipeline.preprocessing.image_cleaner import preprocess_image
import os

if __name__ == "__main__":

    input_img = "data/processed/page_0.jpg"
    output_img = "data/processed/cleaned_page_0.jpg"

    if os.path.exists(input_img):
        result = preprocess_image(input_img, output_img)
        print(f"Preprocessed image saved at: {result}")
    else:
        print(f"Warning: Input image not found at {input_img}. Run ingestion first")