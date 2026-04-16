from invoice_pipeline.pipeline.runner import process_folder

if __name__ == "__main__":
    results = process_folder(
        input_folder="data/raw",
        processed_root="data/processed",
        output_root="outputs"
    )

    for result in results:
        print(result["file_name"], "->", result["status"])
        if result["extracted_data"]:
            print("Extracted Data:", result["extracted_data"])
        if result["error"]:
            print("Error:", result["error"])
        print("-" * 40)