import os
import pyperclip

# Specify the directory containing the .md files
dir_path = 'C:/Users/alexo/Documents/hypertext/natural/📚 notes-and-quotes/experiences/internships-work/PDS summer 2022/Documentation of EPLI’s Trading System'

formatted_data = []

# Iterate through each .md file in the directory
for file_name in os.listdir(dir_path):
    if file_name.endswith('.md'):
        with open(os.path.join(dir_path, file_name), 'r') as file:
            content = file.readlines()
            
            # Extract title and details
            title = content[0].strip().replace('#', '').strip()
            details = [line.strip() for line in content[1:] if line.strip()]
            
            # Format the content
            formatted_details = "\n\t- ".join(details)
            formatted_content = f"- {title}\n\t- {formatted_details}"
            formatted_data.append(formatted_content)

# Combine all formatted contents
combined_content = '\n'.join(formatted_data)

# Copy the combined content to the clipboard
pyperclip.copy(combined_content)