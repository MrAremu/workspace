import sys
import json
from google_service_auth import get_service

def update_docs_text(file_id, replacements):
    """
    Replaces text in a Google Doc.
    replacements: dict of {target_text: replacement_text}
    """
    service = get_service('docs', 'v1')

    requests = []
    for target, replacement in replacements.items():
        requests.append({
            'replaceAllText': {
                'containsText': {
                    'text': target,
                    'matchCase': True
                },
                'replaceText': replacement
            }
        })

    if not requests:
        print("No replacements provided.")
        return

    result = service.documents().batchUpdate(
        documentId=file_id,
        body={'requests': requests}
    ).execute()
    
    print(f"Updated {len(requests)} text fields in document {file_id}.")

if __name__ == '__main__':
    # Usage: python update_docs_text.py <file_id> <json_replacements>
    # Example: python update_docs_text.py 12345 '{"{{name}}": "John"}'
    
    if len(sys.argv) < 3:
        print("Usage: python update_docs_text.py <file_id> <json_replacements_string>")
        sys.exit(1)

    file_id = sys.argv[1]
    replacements_str = sys.argv[2]
    
    try:
        replacements = json.loads(replacements_str)
    except json.JSONDecodeError:
        print("Error: Replacements argument must be a valid JSON string.")
        sys.exit(1)

    update_docs_text(file_id, replacements)
