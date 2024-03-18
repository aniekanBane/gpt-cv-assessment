"""
Helper functions
"""

import os
import json

def save_to_json(data: str | list | dict, filename = 'data.json'):
    """
    Save a Python data structure to a JSON file.

    Args:
    - data (`dict`, `list`, `str`): The Python data structure to be saved. Can be a string (that can be loaded as JSON) or a dictionary.
    - filename (`str`): The name of the JSON file.

    Returns:
    - None
    """

    if isinstance(data, str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            raise ValueError("The provided string is not valid JSON.")
        
    elif not isinstance(data, (dict, list)):
        raise TypeError("The data should either be a valid JSON string, dictionary, or list.")
    
    output_file = os.path.join('docs', filename)

    if not os.path.exists(output_file):
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'w') as file:
        json.dump(data, file)
