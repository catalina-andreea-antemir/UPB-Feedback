# ...existing code...
import pickle
# ...existing code...
with open('feedback-raw-no-feedback-contents/courses.p', 'rb') as f:
    data = pickle.load(f)
# ...existing code...
print(type(data))
print(len(data))
# NEW: basic structure inspection
if isinstance(data, list):
    print("First item type:", type(data[0]) if data else None)
    sample = data[:3]
    print("Sample items:")
    for i, item in enumerate(sample):
        print(f"Item {i}:", item)
    if sample and isinstance(sample[0], dict):
        all_keys = set().union(*(d.keys() for d in sample))
        print("Keys in sample:", sorted(all_keys))
        # Show example values per key (first non-empty values)
        for k in sorted(all_keys):
            values = [d.get(k) for d in sample]
            print(f"Key '{k}' examples:", values)
else:
    print("Data is not a list; adjust approach.")