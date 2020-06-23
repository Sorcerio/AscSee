# Image Manipulator
# Manipulates the provided image with the appropriate settings

# Imports
import asciiConverter as ac
import generalUtilities as gu

# Variables
FONT_FONT = 'arial.ttf' # Only in .ttf
FONT_SIZE = 16

# Main Thread
def main():
    # Set the ASCII Converter to Verbose
    ac.toggleVerbose()

    batchProcessImageToAscii(['testImage.jpg', 'testImage2.png', 'testImage3.jpg'])
    # batchProcessImageToAscii(['testImage.jpg', 'testImage2.png', 'testImage3.jpg', 'testImage4.jpg', 'testImage5.jpg', 'testImage6.jpg'])
    # processImageToAscii('testImage.jpg', 'output')
    # processImageToAscii('testImage2.png', 'output')
    # processImageToAscii('testImage3.jpg', 'output')

# Functions
# Processes a single filepath into an ASCII image rendered .png file
def processImageToAscii(filepath, outputName):
    # Process the image to an ASCII image
    outputImage = ac.imageToAsciiImage(filepath, FONT_FONT, FONT_SIZE)

    # Save the image
    outputImage.save(str(outputName)+'.png')

# Processes a list of filepaths into ASCII image rendered .png files
def batchProcessImageToAscii(filepaths):
    # Print the batch process start
    print('Starting batch process with '+str(len(filepaths))+' images...')

    # Loop through the filepath array
    i = 1
    for filepath in filepaths:
        # Print the image being process
        print('Processing image #'+str(i)+': '+str(filepath))

        # Process the image
        processImageToAscii(filepath, ('output'+str(i)))

        # Iterate
        i = i+1

    # Print the batch process end
    print('Finished batch process.')

# Main Thread Execution
if __name__=='__main__':
    main()