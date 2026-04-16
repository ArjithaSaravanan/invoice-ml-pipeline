from pdf2image import convert_from_path
from pathlib import Path

def convert_pdf_to_images(pdf_path:str, output_folder:str):
    """Converts a PDF file to images and saves them in the specified output folder."""
    output_path = Path(output_folder)
    output_path.mkdir(parents=True, exist_ok=True)

    images = convert_from_path(pdf_path)
    image_paths = []
    for i, img in enumerate(images):
        file_path = output_path / f"page_{i}.jpg"
        img.save(file_path, 'JPEG')
        image_paths.append(str(file_path))

    return image_paths