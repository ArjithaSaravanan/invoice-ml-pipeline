from invoice_pipeline.extraction.table_extractor import extract_table_contents

rows = extract_table_contents("data/processed/cleaned_page_0.jpg")

for r in rows:
    print(r)