import sys
from google_service_auth import get_service

def append_sheet_row(spreadsheet_id, range_name, values):
    """Appends a row of values to a Google Sheet."""
    service = get_service('sheets', 'v4')

    body = {
        'values': [values]
    }

    result = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption='USER_ENTERED',
        body=body
    ).execute()

    print(f"{result.get('updates').get('updatedCells')} cells appended.")
    return result

if __name__ == '__main__':
    import json
    # Usage: python append_sheet_row.py <spreadsheet_id> <range> <json_list_values>
    if len(sys.argv) < 4:
        print("Usage: python append_sheet_row.py <spreadsheet_id> <range> <json_list_values>")
        sys.exit(1)

    spreadsheet_id = sys.argv[1]
    range_name = sys.argv[2]
    values_json = sys.argv[3]
    
    try:
        values = json.loads(values_json)
        if not isinstance(values, list):
            raise ValueError("Values must be a list")
    except Exception as e:
        print(f"Error parsing values: {e}")
        sys.exit(1)

    append_sheet_row(spreadsheet_id, range_name, values)
