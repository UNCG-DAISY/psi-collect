from PIL import Image
import os

"""
#creates all folders
os.makedirs('G:\\Shared drives\\C-Sick\\smallerJPGImage')
os.makedirs('G:\\Shared drives\\C-Sick\\smallerJPGImage\\Barry')
os.makedirs('G:\\Shared drives\\C-Sick\\smallerJPGImage\\Dorian')
os.makedirs('G:\\Shared drives\\C-Sick\\smallerJPGImage\\Florence')
os.makedirs('G:\\Shared drives\\C-Sick\\smallerJPGImage\\Gordon')
os.makedirs('G:\\Shared drives\\C-Sick\\smallerJPGImage\\Michael')
"""

# Declare the size to convert the image
size_300 = (300, 300)

# Declare the path
path = 'G:\\Shared drives\\C-Sick\\data\\'

# Empty file to store all the jpg files
files = []

# Loop through the path and find all the jpg files
# r = root, d = directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        filePath = os.path.join(r, file)
        if '.jpg' in file and os.path.getsize(filePath) > 0:
            files.append(filePath)

# Resize all the jpg files and save it to the appropriate folder
index = 0
for f in files:
    index += 1
    print(f)
    i = Image.open(f)

    # Save all the Barry images to the Barry folder
    if f.startswith('G:\\Shared drives\\C-Sick\\data\\Barry'):
        fn, f_ext = os.path.splitext(f)
        i = i.resize(size_300, Image.ANTIALIAS)
        path = 'G:\\Shared drives\\C-Sick\\smallerJPGImage\\Barry\\'
        fileName = os.path.basename(f)
        name = fileName
        i.save(path + name)
    # Save all the Dorian images to the Dorian folder
    elif f.startswith('G:\\Shared drives\\C-Sick\\data\\Dorian'):
        fn, f_ext = os.path.splitext(f)
        i = i.resize(size_300, Image.ANTIALIAS)
        path = 'G:\\Shared drives\\C-Sick\\smallerJPGImage\\Dorian\\'
        fileName = os.path.basename(f)
        name = fileName
        i.save(path + name)
    # Save all the Florence images to the Florence folder
    elif f.startswith('G:\\Shared drives\\C-Sick\\data\\Florence'):
        fn, f_ext = os.path.splitext(f)
        i = i.resize(size_300, Image.ANTIALIAS)
        path = 'G:\\Shared drives\\C-Sick\\smallerJPGImage\\Florence\\'
        fileName = os.path.basename(f)
        name = fileName
        i.save(path + name)
    # Save all the Gordon images to the Gordon folder
    elif f.startswith('G:\\Shared drives\\C-Sick\\data\\Gordon'):
        fn, f_ext = os.path.splitext(f)
        i = i.resize(size_300, Image.ANTIALIAS)
        path = 'G:\\Shared drives\\C-Sick\\smallerJPGImage\\Gordon\\'
        fileName = os.path.basename(f)
        name = fileName
        i.save(path + name)
    # Save all the Michael images to the Michael folder
    elif f.startswith('G:\\Shared drives\\C-Sick\\data\\Michael'):
        fn, f_ext = os.path.splitext(f)
        i = i.resize(size_300, Image.ANTIALIAS)
        path = 'G:\\Shared drives\\C-Sick\\smallerJPGImage\\Michael\\'
        fileName = os.path.basename(f)
        name = fileName
        i.save(path + name)
