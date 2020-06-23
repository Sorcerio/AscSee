# ASCII Converter
# Converts given image files into ASCII stylized images.

# Imports
from PIL import Image, ImageDraw, ImageFont # pip install Pillow
# import cv2 as cv # pip install opencv-python
import time
import math
import textwrap

# Variables
USED_CHARS = ['#','?','%','.','S','+','.','*',':',',','@']
VERBOSE = False

# Example Thread
def example(filepath, newWidth = 100):
    # Enter image conversion try/catch
    try:
        # Try to get the image
        image = Image.open(filepath)

        # Convert the image to ASCII
        image = imageToAsciiString(image, newWidth)

        # Return the image
        return image
    except Exception as err:
        # Print the problem
        print("Image at "+str(image)+" could not opened.")
        print(err)

        # Send back nothing
        return None

# Functions
# Toggles the verbose flop
def toggleVerbose():
    # Scope the global
    global VERBOSE

    # Flop verbose
    VERBOSE = not VERBOSE

    # Check if verbose
    if VERBOSE:
        print('Verbose mode is on')

# Converts the provided image to an ASCII representation
# image -> The image to convert to ASCII
# newWidth -> The width to return the image at. (default: 100)
# subsample -> If not 0, starts with the first index in the final ASCII generation and creates a subsample of only
#               the nth values. This is useful because when generating the ASCII, the image will have an equal number
#               of characters as the image size in pixels. (default: 0, ie: subsample disabled)
def imageToAsciiString(image, newWidth = 100, subsamble = 0, ):
    # Check if verbose status should be stated
    if VERBOSE:
        print('Converting image to ASCII...')

    # Scale the image down to the decided width
    image = scaleImage(image, newWidth)

    # Convert the image to grayscale
    image = image.convert('L')

    # Map the pixels to ASCII characters
    imageChars = mapPixelsToAscii(image)

    # Count the number of characters in the image
    imageCharsCount = len(imageChars)

    # Collapse the image characters to fit the width of the image using list compression
    imageAsciiList = [imageChars[index: index+newWidth] for index in range(0, imageCharsCount, newWidth)]

    # Convert the image ASCII lists to a string seperated by new lines
    imageAscii = '\n'.join(imageAsciiList)

    # Check if a subsampling size is set
    if subsamble > 0:
        imageAscii = imageAscii[0::subsamble]

    # Check if verbose status should be stated
    if VERBOSE:
        print('Image to ASCII conversion done.')

    # Send the converted image back
    return imageAscii

# Scales the image down to the desired width keeping the aspect ratio
def scaleImage(image, newWidth = 100):
    # Get the image's size
    (startWidth, startHeight) = image.size

    # Calculate the aspect ratio multiplier of the image
    ratio = startHeight/float(startWidth)

    # Calculate the new height for the new width
    newHeight = int(ratio*newWidth)

    # Resize the image
    newImage = image.resize((newWidth, newHeight))

    # Return the image
    return newImage

# Maps pixels from the provided image to ASCII characters and returns them in a string
def mapPixelsToAscii(image):
    # Calculate the range width
    rangeWidth = 256/len(USED_CHARS)

    # Get the pixel data from the image
    pixelData = list(image.getdata())

    # Convert the pixels to their associated characters using list compression
    pixelChars = [USED_CHARS[int(pixelValue/rangeWidth)] for pixelValue in pixelData]

    # Return the pixel characters list as a joined string
    return ''.join(pixelChars)

# Converts an image at the specified filepath to an ASCII image file
def imageToAsciiImage(filepath, fontName):
    # Mark the start time
    exStartTime = time.time()

    # # Try to get the input image
    # try:

    # FONT_SIZE
    fontSize = 16

    # Try to get the input image
    inputImage = Image.open(filepath)

    # Get the size of the input image
    (inputW, inputH) = inputImage.size

    inputImage = inputImage.convert('L')

    # Get the ascii string
    asciiString = mapPixelsToAscii(inputImage)

    # Collapse the image characters to fit the width of the image using list compression
    imageAsciiList = [asciiString[index: index+inputW] for index in range(0, len(asciiString), inputW)]

    # Print the build image response
    print('Building output image...')

    # Create an output image
    outputImage = Image.new('RGB', (inputW, inputH), 'black')

    # Prepare the output image to be drawn on
    outputDraw = ImageDraw.Draw(outputImage)

    # Build the draw font
    font = ImageFont.truetype(fontName, fontSize)

    # Loop through the ascii list
    cursorY = 0
    # for line in imageAsciiList:
    for lineInd in range(0, len(imageAsciiList), fontSize-1):
        # Get the line
        line = imageAsciiList[lineInd]

        # Loop through the appropriate amount of characters for the row
        cursorX = 0
        for charInd in range(0, len(line), fontSize-1):
            # Draw the character
            outputDraw.text((cursorX, cursorY), line[charInd], 'white', font)

            # Iterate x cursor
            cursorX = cursorX+fontSize

        # Increase y cursor
        cursorY = cursorY+fontSize

    # Check if verbose status should be stated
    if VERBOSE:
        # Print the build image done response
        print('Done building output image.')

        # Print the execution time
        print('Image converted in: %.2f seconds' % (time.time()-exStartTime))

    # Return the output image
    return outputImage

    # except Exception as err:
    #     # Print the problem
    #     print("Image at "+str(inputImage)+" could not opened.")
    #     print(err)

# Calculates and return the aspect ratio of the provided size values
def calculateAspectRatio(width, height):
    # Calculate the greates common denominator
    gcd = math.gcd(width, height)

    # Calculate the aspect ratios
    arW = width/gcd
    arH = height/gcd

    # Return them in a tuple
    return (arW, arH)

# Main Thread Execution
if __name__=='__main__':
    # Import System to get parameters
    import sys

    # Convert the image
    asciiString = example(sys.argv[1])

    # Save the ASCII image to a file
    with open('output.txt', 'w') as wFile:
        # Write the text out
        wFile.write(asciiString)
