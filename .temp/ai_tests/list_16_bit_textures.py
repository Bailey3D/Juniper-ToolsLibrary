# Import the required modules
from PIL import Image
from os import listdir


# Define a function to list all 16-bit texture files in the given folder
def list_16bit_textures(folder):
    # Get the names of all files in the folder
    filenames = listdir(folder)

    # Iterate over the files and check if they are 16-bit texture files
    for filename in filenames:
        # Open the file using PIL and check its bit depth
        img = Image.open(folder + filename)
        if img.bits == 16:
            # Print the file name if it is a 16-bit texture file
            print(filename)


# Call the function with a sample folder
list_16bit_textures("C:\\example\\folder\\")
