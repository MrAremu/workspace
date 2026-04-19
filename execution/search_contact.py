import sys
from google_service_auth import get_service

def search_contact(name):
    """Searches for a contact by name and returns the email address."""
    service = get_service('people', 'v1')
    
    # helper to print to stderr so we don't mix with stdout output if needed, 
    # but for this system we usually want pure stdout for the result key
    # print(f"Searching for contact: {name}", file=sys.stderr)

    results = service.people().searchContacts(
        query=name,
        readMask='names,emailAddresses'
    ).execute()

    connections = results.get('results', [])

    if not connections:
        print(f"No contact found for query: {name}")
        return None

    # Just take the first match
    person = connections[0].get('person', {})
    emails = person.get('emailAddresses', [])

    if emails:
        return emails[0].get('value')
    else:
        print(f"Contact found for {name} but has no email address.")
        return None

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python search_contact.py <name>")
        sys.exit(1)
    
    query_name = sys.argv[1]
    email = search_contact(query_name)
    
    if email:
        print(email)
    else:
        sys.exit(1)
