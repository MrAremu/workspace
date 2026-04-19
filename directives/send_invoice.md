# Send Invoice Directive

## Goal
Automate the process of generating and sending an invoice to a client.

## Inputs
- `clientName`: Name of the client (used for lookup and file naming)
- `billingStartPeriod`: Start date of billing period
- `billingEndPeriod`: End date of billing period
- `billingAmount`: Amount to bill
- `toBePayedByDate`: Due date
- `templateFileId`: ID of the invoice template GDoc
- `invoicesFolderId`: ID of the folder to save invoices to
- `spreadsheetId`: ID of the logging spreadsheet
- `spreadsheetRange`: Range to append to (e.g., "Sheet1!A:E")

## Step-by-Step Instructions

### Option 1: One-Click Automation (Recommended)
Run the master script with your dynamic values:
```bash
py execution/process_invoice.py --name "Client Name" --start "YYYY-MM-DD" --end "YYYY-MM-DD" --amount "500" --due "YYYY-MM-DD"
```

### Option 2: Manual Step-by-Step
1.  **Lookup Client Email**
    - **Tool**: `execution/search_contact.py`
    - **Args**: `clientName`
    - **Check**: If no email found, STOP and ask user for email.

2.  **Generate Invoice Document**
    - **Tool**: `execution/copy_drive_file.py`
    - **Args**:
        - `file_id`: `templateFileId`
        - `destination_folder_id`: `invoicesFolderId`
        - `new_name`: "Invoice - [clientName] - [billingStartPeriod] to [billingEndPeriod]"
    - **Output**: `newFileId`, `webViewLink`

3.  **Update Invoice Content**
    - **Tool**: `execution/update_docs_text.py`
    - **Args**:
        - `file_id`: `newFileId` (from step 2)
        - `replacements`: JSON string of mapping:
            - `clientName` -> `clientName`
            - `billingStartPeriod` -> `billingStartPeriod`
            - `billingEndPeriod` -> `billingEndPeriod`
            - `billingAmount` -> `billingAmount`
            - `toBePayedByDate` -> `toBePayedByDate`

4.  **Export to PDF**
    - **Tool**: `execution/export_drive_file.py`
    - **Args**: `newFileId`
    - **Output**: `pdfPath` (e.g., `.tmp/Invoice...pdf`)

5.  **Send Email**
    - **Tool**: `execution/send_gmail.py`
    - **Args**:
        - `to`: `clientEmail` (from step 1)
        - `subject`: "Invoice for [billingStartPeriod] - [billingEndPeriod]"
        - `body`: "Please find attached the invoice for the recent period." (or similar)
        - `attachment_path`: `pdfPath` (from step 4)

6.  **Log to Sheets**
    - **Tool**: `execution/append_sheet_row.py`
    - **Args**:
        - `spreadsheet_id`: `spreadsheetId`
        - `range`: `spreadsheetRange`
        - `values`: JSON list `[Date, clientName, billingStartPeriod + " / " + billingEndPeriod, billingAmount, toBePayedByDate, clientEmail, pdfLink]`

## Edge Cases
- **Missing Email**: Prompt user manually.
- **Quota Exceeded**: Wait and retry (handle in python script ideally, or report error).
- **Invalid Credentials**: Ensure `credentials.json` is valid.
