from paddleocr import PaddleOCR  # main OCR dependencies
from matplotlib import pyplot as plt  # plot images
import os  # folder directory navigation
import re
import cv2

# Setup model
image_path = 'img/dat.jpg'
image = cv2.imread(image_path)

# Get the dimensions of the image
height, width, _ = image.shape

# Define the region of interest (ROI) to include only the MRZ lines
# Adjust the mrz_top and mrz_bottom to precisely match the provided MRZ image
mrz_top = height - 200  # Adjust as needed
mrz_bottom = height     # Adjust as needed
roi = image[mrz_top:mrz_bottom, 0:width]

# Save the cropped image
output_path = 'img/dat.jpg'
cv2.imwrite(output_path, roi)

output_path

ocr_model = PaddleOCR(lang='en')

img_path = os.path.join(output_path)

# Run the OCR method on the OCR model
result = ocr_model.ocr(img_path)

# Specify the output directory and file path
output_dir = r'icao'
output_file = os.path.join(output_dir, 'result.txt')

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Function to process and format the OCR result
def process_ocr_result(text):
    text = text.replace('<', '')  # Remove "<" characters
    formatted_output = []

    # Extract and format ID
    if text.startswith('ID'):
        formatted_output.append(f"id: {text[:5]}")
        formatted_output.append(f"cccd number1: {text[5:14]}")
        formatted_output.append(f"checksum: {text[14]}")
        formatted_output.append(f"cccd number: {text[15:27]}")
        formatted_output.append(f"checksum: {text[27]}")

    # Extract and format birthdate, sex, and expiry date
    elif text.startswith('0'):
        birth = f"{text[4:6]}/{text[2:4]}/{text[:2]}"
        expire = f"{text[12:14]}/{text[10:12]}/{text[8:10]}"
        formatted_output.append(f"birth: {birth}")
        formatted_output.append(f"checksum: {text[6]}")
        formatted_output.append(f"Sex: {text[7]}")
        formatted_output.append(f"expire: {expire}")
        formatted_output.append(f"checksum: {text[14]}")
        formatted_output.append(f"checksum: {text[15:18]}")
        formatted_output.append(f"checksum: {text[18]}")

    # Extract and format name
    else:
        # Custom split function to handle uppercase letters correctly
        def custom_split(name):
            parts = []
            current_part = name[0]
            for char in name[1:]:
                if char.isupper():
                    parts.append(current_part)
                    current_part = char
                else:
                    current_part += char
            parts.append(current_part)
            return parts
        
        name_parts = custom_split(text)
        formatted_output.append(f"name: {' '.join(name_parts)}")

    return "\n".join(formatted_output)

# Extract and process the text, then save it to a file
with open(output_file, 'w', encoding='utf-8') as f:
    for res in result:
        for line in res:
            processed_text = process_ocr_result(line[1][0])
            f.write(processed_text + '\n')

# Print to terminal for verification
for res in result:
    for line in res:
        processed_text = process_ocr_result(line[1][0])
        print(processed_text)
