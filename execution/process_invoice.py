import sys
import os
import argparse
import json

# Import existing tools
# Note: We need to import the functions, not just run the scripts.
# To make this clean, we'll assume the files are in the same dir and can be imported.
# We might need to slightly adjust the individual scripts if they don't expose clean functions, 
# but based on my earlier creation, they all have main functions like search_contact(name).

from search_contact import search_contact
from copy_drive_file import copy_drive_file
from update_docs_text import update_docs_text
from export_drive_file import export_drive_file
from send_gmail import send_gmail
from append_sheet_row import append_sheet_row

# HARDCODED CONFIG (Moved from my memory to code)
TEMPLATE_FILE_ID = "1cdU_3KFwq_cb8BMFJLhwR6Lpy2WLiU0MR_Wx1R1c6Jo"
INVOICES_FOLDER_ID = "1FBKX8p4-a86jdD7Mij_2JGanvc_RZzy4"
SPREADSHEET_ID = "197jyQTE8Fd3hpIR2qsW0Z2mVTSqSsv0Q9Byrv83knuA"
SPREADSHEET_RANGE = "Sent Invoices!A:G"

def process_invoice(client_name, billing_start, billing_end, amount, due_date):
    print(f"--- Starting Invoice Process for {client_name} ---")
    
    # 1. Search Contact
    print(f"[1/6] Searching for email...")
    email = search_contact(client_name)
    if not email:
        print(f"Error: Could not find email for {client_name}")
        return
    print(f"      Found: {email}")

    # 2. Copy Template
    print(f"[2/6] Creating invoice document...")
    new_filename = f"Invoice - {client_name} - {billing_start} to {billing_end}"
    drive_response = copy_drive_file(TEMPLATE_FILE_ID, INVOICES_FOLDER_ID, new_filename)
    new_file_id = drive_response.get('id')
    web_view_link = drive_response.get('webViewLink') # Docs link
    print(f"      Created: {web_view_link}")

    # 3. Update Text
    print(f"[3/6] Updating invoice details...")
    replacements = {
        "clientName": client_name,
        "billingStartPeriod": billing_start,
        "billingEndPeriod": billing_end,
        "billingAmount": str(amount),
        "toBePayedByDate": due_date
    }
    update_docs_text(new_file_id, replacements)

    # 4. Export PDF
    print(f"[4/6] Exporting to PDF...")
    pdf_path = export_drive_file(new_file_id, 'application/pdf')
    
    # 5. Send Email
    print(f"[5/6] Sending email...")
    subject = f"Invoice for {billing_start} - {billing_end}"
    body = "Please find attached the invoice for the recent period."
    send_gmail(email, subject, body, pdf_path)

    # 6. Log to Sheets
    print(f"[6/6] Logging to Google Sheets...")
    # Columns: Date, Name, Period, Amount, DueDate, Email, Url
    from datetime import date
    today = str(date.today())
    period_str = f"{billing_start} / {billing_end}"
    
    sheet_values = [
        today,
        client_name,
        period_str,
        str(amount),
        due_date,
        email,
        web_view_link
    ]
    
    append_sheet_row(SPREADSHEET_ID, SPREADSHEET_RANGE, sheet_values)

    # Cleanup
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
        print("      Cleaned up temp PDF.")

    print("--- Process Complete! ---")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automated Invoice Processor")
    parser.add_argument("--name", required=True, help="Client Name")
    parser.add_argument("--start", required=True, help="Billing Start Date (YYYY-MM-DD)")
    parser.add_argument("--end", required=True, help="Billing End Date (YYYY-MM-DD)")
    parser.add_argument("--amount", required=True, help="Billing Amount (e.g. 500)")
    parser.add_argument("--due", required=True, help="Due Date (YYYY-MM-DD)")
    
    args = parser.parse_args()
    
    process_invoice(args.name, args.start, args.end, args.amount, args.due)
