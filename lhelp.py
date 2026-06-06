import os
import numpy as np
import re

def make_data(file, distance): 
    with open(file, 'r') as f:
        data = f.read()
    entries = data.split(';')
    result = []
    # Uses loops to add distance instead of doing whatever
    for entry in entries:
        if entry.strip():
            parts = entry.split(',')
            # Modifies value 3
            if len(parts) > 3:
                try:
                    parts[3] = str(int(parts[3]) + distance)
                except (ValueError, IndexError):
                    pass
            result.append(','.join(parts))
        else:
            result.append(entry)
    return ';'.join(result)
