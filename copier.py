import os
import pyperclip

# Get list of all .py files in current directory, except this script
current_file = os.path.basename(__file__)
files = [f for f in os.listdir('.') if f.endswith(['.py', '.md']) and f != current_file]

# Read contents of each file and build string
contents = ''
for file in files:
    with open(file, 'r') as f:
        contents += f'\n```{file}\n'
        contents += f.read()
        contents += '\n```\n'

# Copy to clipboard    
pyperclip.copy(contents)

print('Copied contents of all .py files to clipboard')