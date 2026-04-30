from model.cyclone import chatbot_response

test_cases = [
    ("Where is Cyclone?", "simple"),
    ("What is the salary?", "simple"),
    ("Tell me about product manager role", "complex"),
    ("How do I apply?", "medium"),
    ("I know Flutter, Dart, and Firebase", "complex"),
]

print("\n" + "="*70)
print("DYNAMIC RESPONSE LENGTH BASED ON QUESTION COMPLEXITY")
print("="*70)

for query, expected_type in test_cases:
    resp = chatbot_response(query)
    lines = len(resp.splitlines())
    chars = len(resp)
    
    print(f"\nQuery: {query}")
    print(f"Expected: {expected_type.upper()}")
    print(f"Response: {lines} lines, {chars} characters")
    print(f"Preview: {resp[:100]}{'...' if len(resp) > 100 else ''}")

print("\n" + "="*70)
