import json
import os







# 1. Create a JSON file (if it doesn’t exist)
def create_json_if_not_exists(file_path, default_data={}):
    """
    Creates a JSON file if it does not exist.
    """
    if not os.path.exists(file_path):
        if default_data is None:
            default_data = {}

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(default_data, f, indent=4)

        return True  # file created
    return False  # file already exists



# 2. Open & read a JSON file
def read_json(file_path):
    """
    Reads and returns JSON data from a file.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


# 3. Save (write) updated data to a JSON file
def write_json(file_path, data):
    """
    Writes updated data to a JSON file.
    """
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


