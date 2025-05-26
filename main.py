from docx import Document
import sys
import parser
import json

if len(sys.argv) != 2:
    print("Usage: python3 main.py <docx_file>")
    sys.exit(1)
else:
    pass

path_name = sys.argv[1]

def convert_docx_to_text(path_name):
    """
    Convert a .docx file to plain text.
    
    :param docx_path: Path to the .docx file
    :return: Plain text content of the .docx file
    """
    try:
        doc = Document(path_name)
        text = []
        for para in doc.paragraphs:
            text.append(para.text)
        return '\n'.join(text)
    except Exception as e:
        print(f"Error reading {path_name}: {e}")
        return None

# --- Run the parsing ---
print("Sending CV text to Gemini LLM for parsing...")
parsed_cv_data = parser.parse_cv_with_gemini(convert_docx_to_text(path_name))

# Print the resulting JSON
print("\n--- Parsed CV Data (JSON) ---")
print(json.dumps(parsed_cv_data, indent=4)) # Pretty print the JSON
print("-" * 30)

# --- Save the parsed data to a JSON file ---

output_file = "parsed_cv_data.json"  # Define the output file name

with open(output_file, "w", encoding="utf-8") as file:
    json.dump(parsed_cv_data, file, indent=4)  # Save JSON data to the file

    
if __name__ == "__main__":
    text_content = convert_docx_to_text(path_name)
    if text_content:
        print(text_content)
    else:
        print("Failed to convert the document to text.")