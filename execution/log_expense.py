import sys
from append_sheet_row import append_sheet_row

# Configuration (Same Spreadsheet as before, but different sheet if needed)
SPREADSHEET_ID = "197jyQTE8Fd3hpIR2qsW0Z2mVTSqSsv0Q9Byrv83knuA" # Assuming same Bookkeeping sheet
SHEET_NAME = "Reciepts Summary" # User corrected to "Reciepts Summary"

def log_expense(data, file_link):
    """
    Logs the extracted expense data to Google Sheets.
    data: JSON object with keys: Expense Date, Vendor, Expense Amount, Expense Type, Expense Description, Reference
    """
    
    # Map JSON fields to columns: 
    # Mapped Fields from prompt: Expense Date, Expense Type, Expense Description, Expense Amount, Vendor, Reference#, link to file
    
    row_values = [
        data.get("Expense Date", ""),
        data.get("Expense Type", ""),
        data.get("Expense Description", ""),
        data.get("Expense Amount", ""),
        data.get("Vendor", ""),
        data.get("Reference", ""),
        file_link
    ]
    
    range_name = f"'{SHEET_NAME}'!A:G" # Append to columns A-G with quoted sheet name
    
    print(f"Logging row: {row_values}")
    append_sheet_row(SPREADSHEET_ID, range_name, row_values)

if __name__ == '__main__':
    import json
    if len(sys.argv) < 3:
        print("Usage: python log_expense.py <json_data_string> <file_link>")
        sys.exit(1)
        
    data_str = sys.argv[1]
    file_link = sys.argv[2]
    
    try:
        data = json.loads(data_str)
        log_expense(data, file_link)
    except json.JSONDecodeError:
        print("Error: Invalid JSON data")
