import os
import shutil
import time
from upload_to_drive import upload_to_drive
from analyze_document import analyze_document
from log_expense import log_expense

# Configuration
INPUT_DIR = "input_expenses"
PROCESSED_DIR = "processed_expenses"
DRIVE_FOLDER_ID = "1Rfu4eQvD6YV1HVYnfqRamxXIcwb-XNMO" # Receipts/Accounting folder 

def process_all_expenses():
    if not os.path.exists(INPUT_DIR):
        os.makedirs(INPUT_DIR)
    if not os.path.exists(PROCESSED_DIR):
        os.makedirs(PROCESSED_DIR)

    files = [f for f in os.listdir(INPUT_DIR) if os.path.isfile(os.path.join(INPUT_DIR, f))]
    
    if not files:
        print("No files found in input_expenses/")
        return

    print(f"Found {len(files)} files to process.")

    for filename in files:
        file_path = os.path.join(INPUT_DIR, filename)
        print(f"\n--- Processing: {filename} ---")

        # 1. Upload to Drive
        print("[1/3] Uploading to Drive...")
        try:
            drive_link = upload_to_drive(file_path, DRIVE_FOLDER_ID)
        except Exception as e:
            print(f"Upload failed: {e}")
            continue

        # 2. Analyze Document
        print("[2/3] Analyzing Document...")
        expense_data = analyze_document(file_path)
        if not expense_data:
            print("Analysis failed. Skipping logging.")
        else:
            print(f"      Extracted: {expense_data['Vendor']} - {expense_data['Expense Amount']}")

            # 3. Log to Sheets
            print("[3/3] Logging to Sheets...")
            try:
                log_expense(expense_data, drive_link)
                
                # 4. Move to Processed (Only if successful)
                try:
                    shutil.move(file_path, os.path.join(PROCESSED_DIR, filename))
                    print("      Moved to processed_expenses/")
                except Exception as e:
                    print(f"Move failed: {e}")
                    
            except Exception as e:
                print(f"Logging failed: {e}")

    print("\n--- Batch Processing Complete ---")

if __name__ == "__main__":
    process_all_expenses()
