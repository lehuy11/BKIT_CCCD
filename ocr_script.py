import os
import sys
import logging
from paddleocr import PaddleOCR
from PIL import Image
import json

# Suppress DEBUG and WARNING logs from PaddleOCR
logging.getLogger('ppocr').setLevel(logging.ERROR)

def cut_and_save_image(img_path, output_dir):
    img = Image.open(img_path)
    width, height = img.size
    top_height = (2 * height) // 3
    bottom_box = (0, top_height, width, height)
    bottom_img = img.crop(bottom_box)
    base_name = os.path.basename(img_path)
    bottom_img_path = os.path.join(output_dir, base_name)
    bottom_img.save(bottom_img_path)
    return bottom_img_path

def process_ocr_result(text):
    text = text.replace('<', '')
    data = {}

    if text.startswith('ID'):
        data["id"] = text[:5]
        data["cccdnumber1"] = text[5:14]
        data["checksum1"] = text[14] if len(text) > 14 else ''
        #data["cccdnumber"] = text[15:27]
        #data["checksum2"] = text[27] if len(text) > 27 else ''
    elif text.startswith('0'):
        birth = f"{text[:2]}{text[2:4]}{text[4:6]}"
        expire = f"{text[8:10]}{text[10:12]}{text[12:14]}"
        data["birth"] = birth
        data["checksum3"] = text[6] if len(text) > 6 else ''
        #data["Sex"] = text[7] if len(text) > 7 else ''
        data["expire"] = expire
        data["checksum4"] = text[14] if len(text) > 14 else ''
        #data["checksum5"] = text[15:18] if len(text) > 15 else ''
        #data["checksum6"] = text[18] if len(text) > 18 else ''

    # else:
    #     def custom_split(name):
    #         parts = []
    #         current_part = name[0]
    #         for char in name[1:]:
    #             if char.isupper():
    #                 parts.append(current_part)
    #                 current_part = char
    #             else:
    #                 current_part += char
    #         parts.append(current_part)
    #         return parts
    #     name_parts = custom_split(text)
    #     data["name"] = ' '.join(name_parts)

    return data
    
def process_images(img_path):
    output_dir = 'icao'
    os.makedirs(output_dir, exist_ok=True)
    cut_img_path = cut_and_save_image(img_path, output_dir)
    
    ocr_model = PaddleOCR(lang='en')
    result = ocr_model.ocr(cut_img_path)
    
    result_text = ""
    result_data = []
    
    with open(os.path.join(output_dir, 'result.txt'), 'w', encoding='utf-8') as f:
        for res in result:
            for line in res:
                data = process_ocr_result(line[1][0])
                formatted_text = "\n".join(f"{key}: {value}" for key, value in data.items())
                f.write(formatted_text + '\n')
                result_text += formatted_text + '\n'
                result_data.append(data)
    
    # Save JSON
    with open(os.path.join(output_dir, 'result.json'), 'w', encoding='utf-8') as json_file:
        json.dump(result_data, json_file, ensure_ascii=False, indent=4)
    
    return result_text


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(1)
    img_path = sys.argv[1]
    result_text = process_images(img_path)
