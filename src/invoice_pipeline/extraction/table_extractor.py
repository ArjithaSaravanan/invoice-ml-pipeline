import pytesseract
import cv2

tesseract_path = os.getenv("TESSERACT_PATH")
if tesseract_path:
    pytesseract.pytesseract.tesseract_cmd = tesseract_path

def extract_table_contents(image_path: str):
    img = cv2.imread(image_path)

    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
    rows = []
    current_row = []
    last_y = -1
    threshold = 15

    for i, word in enumerate(data['text']):
        if word.strip() == "":
            continue
        x = data['left'][i]
        y = data['top'][i]
        
        if last_y == -1:
            current_row.append((x, word))
            last_y = y
            continue
        if abs(y - last_y) < threshold:
            current_row.append((x, word))
        else:
            rows.append(sorted(current_row, key=lambda x: x[0]))
            current_row = [(x, word)]
            last_y = y
    if current_row:
        rows.append(sorted(current_row, key=lambda x: x[0]))

    #convert to clean text rows
    structured_rows = []

    for row in rows:
        structured_rows.append([word for _, word in row])

    return structured_rows