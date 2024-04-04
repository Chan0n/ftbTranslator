import os
import re
import json

from googletrans import Translator


translator = Translator()
lang = "th"


def insert_translations(obj):
  if isinstance(obj, dict):
      for key, value in obj.items():
          if isinstance(value, list):
              for i, item in enumerate(value):
                  if isinstance(item, dict) or isinstance(item, list):
                      insert_translations(item)
          elif isinstance(value, str) and key != "id":
              match = re.match(r'\(Translated: (.+)\)', value)
              if match:
                  obj[key] = [match.group(1)]  # Replace original text with translated text



def extract_description_contents(lines, index):
  content = []
  # Split the line by "[", then take the second part and split it by "]", take the first part
  content.append(lines[index].split("[")[1].split("]")[0].strip())
  # Start reading lines from the next index
  for i in range(index + 1, len(lines)):
      line = lines[i]
      # If "]" is found in the line, take the part before "]"
      if "]" in line:
          content.append(line.split("]")[0].strip())
          break
      # If there's no "]", just append the whole line
      else:
          content.append(line.strip())
  # Join all the lines together
  description = " ".join(content)

  # Extract text enclosed in double quotes
  quoted_texts = re.findall(r'"([^"]*)"', description)

  # Filter out empty texts
  quoted_texts = [text for text in quoted_texts if text.strip()]

  return quoted_texts


def translate_with_color_codes(text, dest):
# Extract Minecraft color codes
  color_codes = re.findall(r'&[0-9a-fA-Fk-oK-OrR]', text)
# Replace color codes with placeholders
  text_with_placeholders = re.sub(r'&[0-9a-fA-Fk-oK-OrR]', 'ᚠᛖᛚᛋᛖᛋᚢᛚᛖ'.lower(), text.lower())
# Translate the text without color codes
  translated_text = translator.translate(text_with_placeholders, dest=dest).text
# Replace placeholders with original color codes
  #print("Text with Placeholders:", text_with_placeholders)
  #print("Translated Text Before Replacement:", translated_text)
  for code in color_codes:
    translated_text = translated_text.replace('ᚠᛖᛚᛋᛖᛋᚢᛚᛖ'.lower(), code.lower(), 1)
    #print("Translated Text After Replacement:", translated_text)
    #print("----------------------------------------")
  return translated_text.lower()

# Get the current working directory.
cwd = os.getcwd()
# Get the absolute path to the file.
file = "3spirit.snbt"
filepath = os.path.join(cwd, file)







with open(file, 'r+') as f:
  #data_string = f.read()
  #data = json.loads(data_string)
  # Read all lines into a list
  lines = f.readlines()
  


  for i, line in enumerate(lines):
    # Check if the desired text is in the line
    #translated_text = "Couldnt translate this text"
    if ("subtitle: " in line) and ("Translated" not in line):

      # Append the new text to the line

      match = re.search(r'"([^"]*)"', line)
      if match:
          extracted_text = match.group(1)
          #print("Extracted text:", extracted_text)
          if extracted_text:  # Check if extracted_text is not None or empty
            #translated_text = translator.translate(extracted_text, dest='th')
            translated_text = translate_with_color_codes(extracted_text, dest=lang)

            # Access the translated text using the text attribute

            #cleaned_text = re.sub(r'&\s', '&', translated_text.text)
            print("Translated text:", translated_text)
            lines[i] = line[:-2] + "                                                                " + "" + "(Translate :" + ""+translated_text+ ')"' + "\n"
            
          else:
            print("No text to translate from subtitle")
      continue

  translated_lines = []
  
  for i, line in enumerate(lines):
    if "description: [" in line and "Translated" not in line:
        print("description!")
        quoted_texts = extract_description_contents(lines, i)
        print(quoted_texts)
        for text in quoted_texts:
            translated_text = translate_with_color_codes(text, dest=lang)
            if translated_text:
                # Insert translated text after each original text in the list
                original_index = quoted_texts.index(text) * 2
                quoted_texts.insert(original_index + 1, translated_text)

        # Join the modified quoted_texts list into a single string
        modified_description = ",\n".join(quoted_texts)
        # Replace the original description in the lines list with the modified one
        lines[i] = f"description: [\n{modified_description}\n]"


  for i, translated_line in enumerate(translated_lines):
    lines.insert(i * 2 + 1, translated_line)
       
  
  
    
        


          

        #lines[i] = line[:-2] + " " + "Translate :" + "\n" + cleaned_text + "\n" + '"'
   # Adding a space before the new text

  
  # Move the file pointer to the beginning of the file
  f.seek(0)

  # Write the modified lines back to the file
  f.writelines(lines)
print('end')