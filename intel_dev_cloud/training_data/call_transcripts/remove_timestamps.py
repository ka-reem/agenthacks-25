import os
import re

def remove_timestamps(text):
    # Regular expression to match the timestamp pattern
    pattern = r'^\[\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}\.\d{3}\]\s*'
    return re.sub(pattern, '', text, flags=re.MULTILINE)

def process_files():
    # Get the current directory
    current_dir = os.getcwd()
    # Iterate through all files in the current directory
    for filename in os.listdir(current_dir):
        if filename.endswith('.txt'):
            file_path = os.path.join(current_dir, filename)
            # Read the content of the file
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            # Remove timestamps
            updated_content = remove_timestamps(content)
            # Write the updated content back to the file
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(updated_content)
            print(f"Processed: {filename}")

if __name__ == "__main__":
    process_files()
    print("All files have been processed.")
