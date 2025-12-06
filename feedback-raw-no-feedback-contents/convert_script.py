import json
import pickle
import os
import glob
import sys

def convert_json_to_pickle(directory, file_type):
    """ Loads required JSON files and converts them to temporary Pickle files (.p). """
    
    json_file_path = os.path.join(directory, f"{file_type}.json")
    pickle_file_path = os.path.join(directory, f"{file_type}.p")
    
    if not os.path.exists(json_file_path):
        print(f"   [INFO] JSON file not found: '{json_file_path}'. Skipping conversion.")
        return False

    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        with open(pickle_file_path, 'wb') as f:
            pickle.dump(data, f)
            
        print(f"   [SUCCESS] '{json_file_path}' converted to '{pickle_file_path}'.")
        return True

    except Exception as e:
        print(f"   [ERROR] Failed to convert {json_file_path}: {e}")
        return False


def cleanup_pickle_files(directory):
    """ Deletes all .p files in the specified directory. """
    print("\n[STEP 3] Starting cleanup of temporary .p files...")
    
    search_path = os.path.join(directory, '*.p')
    pickle_files = glob.glob(search_path)
    
    if not pickle_files:
        print("   [INFO] No .p files found to delete.")
        return

    count = 0
    for file_path in pickle_files:
        try:
            os.remove(file_path)
            count += 1
        except Exception as e:
            print(f"   [ERROR] Failed to delete {file_path}: {e}")

    print(f"   [SUCCESS] Deleted {count} temporary .p files.")