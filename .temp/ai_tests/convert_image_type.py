from PIL import Image, ImageFile
from PySide2 import QtWidgets

ImageFile.LOAD_TRUNCATED_IMAGES = True

# Define a function to convert the given image to the specified output format
def convert_to_format(input_file, output_file, output_format):
    # Open the input image and create a new image in the specified format
    loaded_img = Image.open(input_file)
    new_img = Image.new("RGBA", loaded_img.size, (255, 255, 255, 255))

    # Paste the input image onto the new image and save it
    new_img.paste(loaded_img)
    new_img.save(output_file, format=output_format, quality=100)

    # Print a message to the console
    print(f"Successfully converted {input_file} to {output_file}!")

# Ask the user to select one or more images
file_dlg = QtWidgets.QFileDialog()
file_dlg.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
target_files = file_dlg.getOpenFileNames(None, "Select images", "", "Image Files (*.png; *.jpg; *.tga)")

# Convert each selected image to the specified output format
output_format = "TIF"  # Replace this with the desired output format
for input_file in target_files[0]:
    # Compute the output file name by replacing the image type in the input file name with the specified format
    output_file = input_file
    for img_type in ["jpg", "png", "tga", "JPG", "PNG", "TGA"]:
        output_file = output_file.replace("." + img_type, "." + output_format)

    # Convert the image to the specified format
    convert_to_format(input_file, output_file, output_format)