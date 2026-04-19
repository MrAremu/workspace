# Process Expenses Directive

## Goal
Process receipt images and PDFs from a local folder, extract financial data, log it, and archive the files.

## Setup
1.  Ensure you have your receipts in `input_expenses/` folder on your Desktop.
2.  Ensure `.env` has your `OPENROUTER_API_KEY`.

## Usage
Run the following command to process all files in the input folder:

```bash
py execution/process_expenses.py
```

## What Happens
1.  **Iterates** through every file in `input_expenses/`.
2.  **Uploads** the file to Google Drive (Archive).
3.  **Analyzes** the file using AI (OpenRouter/Gemini) to extract:
    *   Date, Vendor, Amount, Type, Description.
4.  **Logs** the data to your Google Sheet ("Invoice Summary" tab).
5.  **Moves** the local file to `processed_expenses/`.

## Troubleshooting
-   **No files processed?**: Check if files are actually in `input_expenses`.
-   **API Error**: Check your OpenRouter key / credit balance.
-   **Drive Error**: Check `credentials.json`.
