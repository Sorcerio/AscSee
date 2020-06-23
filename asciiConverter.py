# ASCII Converter
# Converts given image files into ASCII stylized images.

# Imports
from PIL import Image, ImageDraw, ImageFont
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

    # print(len(imageAscii))
    # (tw, th) = image.size
    # tt = tw*th
    # print(tt)
    # print(tt/subsamble)

    # Convert the image ASCII lists to a string seperated by new lines
    imageAscii = '\n'.join(imageAsciiList)

    # Check if a subsampling size is set
    if subsamble > 0:
        imageAscii = imageAscii[0::subsamble]
        # # Loop through the data
        # resample = ''
        # removeIndex = subsamble
        # skipNext = False
        # for i in range(len(imageAscii)):
        #     # Check if the next character is being skipped
        #     if not skipNext:
        #         # Get the character
        #         char = imageAscii[i]

        #         # Check if at a remove index
        #         if i == removeIndex:
        #             # Check if the character is a new line
        #             if char == '\n':
        #                 # Mark the next character as being removed
        #                 skipNext = True

        #             # Iterate the remove index
        #             removeIndex = removeIndex+subsamble
        #         else:
        #             # Add the character
        #             resample = resample+char
        #     else:
        #         # Character skipped
        #         skipNext = False

        # # Assign resample to the output
        # imageAscii = resample

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

    # Try to get the input image
    inputImage = Image.open(filepath)

    # Get the size of the input image
    (inputW, inputH) = inputImage.size

    # Convert the image to ASCII
    asciiString = imageToAsciiString(inputImage, inputW, 7)

    # Print the build image response
    print('Building output image...')

    # Create an output image
    outputImage = Image.new('RGB', (inputW, inputH), 'black')

    # Prepare the output image to be drawn on
    outputDraw = ImageDraw.Draw(outputImage)

    # TODO: Consider looping through the items within the asciiString string and manually placing them indivigually

    # Build a wrapped text for the size
    textBundle = textwrap.wrap(asciiString, inputW, break_long_words=True, break_on_hyphens=True)

    # Calculate the font size
    fontSize = int(math.floor(inputW/len(textBundle)))

    # Build the draw font
    font = ImageFont.truetype(fontName, fontSize)

    # Loop through the lines
    cusorY = 0
    count = 0
    for line in textBundle:
        # Print the loading bar
        print('Working ('+str(count)+'/'+str(len(textBundle))+')...')

        # Get the font size
        (fW, fH) = font.getsize(line)

        # Draw the text on the line
        outputDraw.text(((inputW-fW)/2, cusorY), line, 'white', font)

        # Increase the cursor
        cusorY = cusorY+fH

        # Iterate the count
        count = count+1

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
