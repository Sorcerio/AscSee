# ASCII Converter
# Converts given image files into ASCII stylized images.

## Imports
from PIL import Image, ImageDraw, ImageFont # pip install Pillow
import cv2 as cv # pip install opencv-python
import numpy as np
import math
import random

## Variables
VERBOSE = False
USED_CHARS = ['#','?','%','.','S','+','.','*',':',',','@']
COLORS_WEB = ['AliceBlue', 'AntiqueWhite', 'Aqua', 'Aquamarine', 'Azure', 'Beige', 'Bisque', 'Black', 'BlanchedAlmond', 'Blue', 'BlueViolet', 'Brown', 'BurlyWood', 'CadetBlue', 'Chartreuse', 'Chocolate', 'Coral', 'CornflowerBlue', 'Cornsilk', 'Crimson', 'Cyan', 'DarkBlue', 'DarkCyan', 'DarkGoldenRod', 'DarkGray', 'DarkGrey', 'DarkGreen', 'DarkKhaki', 'DarkMagenta', 'DarkOliveGreen', 'DarkOrange', 'DarkOrchid', 'DarkRed', 'DarkSalmon', 'DarkSeaGreen', 'DarkSlateBlue', 'DarkSlateGray', 'DarkSlateGrey', 'DarkTurquoise', 'DarkViolet', 'DeepPink', 'DeepSkyBlue', 'DimGray', 'DimGrey', 'DodgerBlue', 'FireBrick', 'FloralWhite', 'ForestGreen', 'Fuchsia', 'Gainsboro', 'GhostWhite', 'Gold', 'GoldenRod', 'Gray', 'Grey', 'Green', 'GreenYellow', 'HoneyDew', 'HotPink', 'IndianRed', 'Indigo', 'Ivory', 'Khaki', 'Lavender', 'LavenderBlush', 'LawnGreen', 'LemonChiffon', 'LightBlue', 'LightCoral', 'LightCyan', 'LightGoldenRodYellow', 'LightGray', 'LightGrey', 'LightGreen', 'LightPink', 'LightSalmon', 'LightSeaGreen', 'LightSkyBlue', 'LightSlateGray', 'LightSlateGrey', 'LightSteelBlue', 'LightYellow', 'Lime', 'LimeGreen', 'Linen', 'Magenta', 'Maroon', 'MediumAquaMarine', 'MediumBlue', 'MediumOrchid', 'MediumPurple', 'MediumSeaGreen', 'MediumSlateBlue', 'MediumSpringGreen', 'MediumTurquoise', 'MediumVioletRed', 'MidnightBlue', 'MintCream', 'MistyRose', 'Moccasin', 'NavajoWhite', 'Navy', 'OldLace', 'Olive', 'OliveDrab', 'Orange', 'OrangeRed', 'Orchid', 'PaleGoldenRod', 'PaleGreen', 'PaleTurquoise', 'PaleVioletRed', 'PapayaWhip', 'PeachPuff', 'Peru', 'Pink', 'Plum', 'PowderBlue', 'Purple', 'RebeccaPurple', 'Red', 'RosyBrown', 'RoyalBlue', 'SaddleBrown', 'Salmon', 'SandyBrown', 'SeaGreen', 'SeaShell', 'Sienna', 'Silver', 'SkyBlue', 'SlateBlue', 'SlateGray', 'SlateGrey', 'Snow', 'SpringGreen', 'SteelBlue', 'Tan', 'Teal', 'Thistle', 'Tomato', 'Turquoise', 'Violet', 'Wheat', 'White', 'WhiteSmoke', 'Yellow', 'YellowGreen']
DEFAULT_FONT_SIZE = 16
DEFAULT_NEW_WIDTH = 100
DEFAULT_WARP = 0
DEFAULT_TEXT_COLORS = ['white']
DEFAULT_BACKGROUND_COLOR = 'black'

## Management Functions
# Toggles the verbose flop
def toggleVerbose():
    # Scope the global
    global VERBOSE

    # Flop verbose
    VERBOSE = not VERBOSE

    # Check if verbose
    if VERBOSE:
        print('Verbose mode is on')

# Gets the current status of verbose mode
def isVerboseOn():
    return VERBOSE

# Get the default newWidth
def getDefaultNewWidth():
    return DEFAULT_NEW_WIDTH

# Get the default warp
def getDefaultWarp():
    return DEFAULT_WARP

# Get the default textColors
def getDefaultTextColors():
    return DEFAULT_TEXT_COLORS

# Get the default BackgroundColor
def getDefaultBackgroundColor():
    return DEFAULT_BACKGROUND_COLOR

# Get the (web) color options
def getColors():
    return COLORS_WEB

## Processing Functions
# Converts the provided to the image to a list of ASCII representing the image's pixels
def imageToAsciiList(image, warp = DEFAULT_WARP):
    # Check if verbose status should be stated
    if VERBOSE:
        print('Converting image to ASCII...')

    # Get the image's size
    (imgWidth, imgHeight) = image.size

    # Convert the image to grayscale
    image = image.convert('L')

    # Map the pixels to ASCII characters
    imageChars = mapPixelsToAscii(image)

    # Check if a subsampling size is set
    if warp > 0:
        imageChars = imageChars[0::warp]

    # Count the number of characters in the image
    imageCharsCount = len(imageChars)

    # Collapse the image characters to fit the width of the image using list compression
    imageAsciiList = [imageChars[index: index+imgWidth] for index in range(0, imageCharsCount, imgWidth)]

    # Check if verbose status should be stated
    if VERBOSE:
        print('Image to ASCII conversion done.')

    # Return the ascii list
    return imageAsciiList

# Gets the colors of the pixels within an image in list format. For each entry in the list a color is
#   represented in a tuple as the following: (R, G, B[, A]). Alpha value will only appear for images
#   using RGBA (like .pngs) and will not appear for images using RGB (like .jpgs)
def imageToColorList(image, warp = DEFAULT_WARP):
    # Check if verbose status should be stated
    if VERBOSE:
        print('Converting image to color list...')

    # Get the image's size
    (imgWidth, imgHeight) = image.size

    # Get the pixel data from the image
    pixelData = list(image.getdata())

    # Build the pixel color list
    pixelColors = [color for color in pixelData]

    # Check if a subsampling size is set
    if warp > 0:
        pixelColors = pixelColors[0::warp]

    # Check if verbose status should be stated
    if VERBOSE:
        print('Image to color conversion done.')

    # Return the pixel colors
    return pixelColors

# Converts the provided image to an ASCII representation string
# image -> The image to convert to ASCII
# newWidth -> The width to return the image at. (default: 100)
# subsample -> If not 0, starts with the first index in the final ASCII generation and creates a subsample of only
#               the nth values. This is useful because when generating the ASCII, the image will have an equal number
#               of characters as the image size in pixels. (default: 0, ie: subsample disabled)
def imageToAsciiString(image, newWidth = DEFAULT_NEW_WIDTH, warp = DEFAULT_WARP):
    # Scale the image down to the decided width
    image = scaleImage(image, newWidth)

    # Build the ascii image list
    imageAsciiList = imageToAsciiList(image, warp)

    # Convert the image ASCII lists to a string seperated by new lines
    imageAscii = '\n'.join(imageAsciiList)

    # Send the converted image back
    return imageAscii

# Scales the image down to the desired width keeping the aspect ratio
def scaleImage(image, newWidth = DEFAULT_NEW_WIDTH):
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

# Converts an image at the specified filepath to an ASCII image object with the provided render specifications.
# NOTE: Check the Read Me for details on the format of the specifications dictionary.
def imagePathToAsciiImage(specs):
    # Check if filepath is provided
    if 'path' in specs:
        # # Try to get the input image
        # try:
        # Try to get the input image
        inputImage = Image.open(specs['path'])

        # Convert and return the image
        return imageToAsciiImage(inputImage, specs)
        # except Exception as err:
        #     # Print the problem
        #     print("Image at "+str(specs['path'])+" could not opened.")

    # Return an error image
    return Image.new('RGB', (100, 100), 'red')

# Converts the provided image to an ASCII image object with the provided 
# NOTE: Check the Read Me for details on the format of the specifications dictionary.
# inputImage -> A PIL image object to convert to ASCII
def imageToAsciiImage(inputImage, specs):
    # Validate the provided specs
    specs = validateSpecs(specs)

    # Get the size of the input image
    (inputW, inputH) = inputImage.size

    # Build the ascii image list
    imageAsciiList = imageToAsciiList(inputImage, specs['warp'])

    # Check if verbose status should be stated
    if VERBOSE:
        # Print the build image response
        print('Building output image...')

    # Create an output image
    outputImage = Image.new('RGB', (inputW, inputH), specs['backgroundColor'])

    # Prepare the output image to be drawn on
    outputDraw = ImageDraw.Draw(outputImage)

    # Build the draw font
    font = ImageFont.truetype(specs['fontFile'], specs['fontSize'])

    # Calculate the max amount of characters for width and height
    maxCharW = int(inputW/specs['fontSize'])
    maxCharH = int(inputH/specs['fontSize'])

    # Calculate the required step for the width and height to match output
    widthStep = int(inputW/maxCharW) # for char
    heightStep = int(inputH/maxCharH) # for line

    # Loop through the ascii list
    cursorY = 0
    for lineInd in range(0, len(imageAsciiList), widthStep):
        # Get the line
        line = imageAsciiList[lineInd]

        # Loop through the appropriate amount of characters for the row
        cursorX = 0
        for charInd in range(0, len(line), heightStep):
            # Draw the character
            outputDraw.text((cursorX, cursorY), line[charInd], random.choice(specs['fontColors']), font)

            # Iterate x cursor
            cursorX = cursorX+specs['fontSize']

        # Increase y cursor
        cursorY = cursorY+specs['fontSize']

    # Check if verbose status should be stated
    if VERBOSE:
        # Print the build image done response
        print('Done building output image.')

    # Return the output image
    return outputImage

# Converts the provided image to an ASCII image object while retaining the colors of the pixel each character represents
# inputImage -> A PIL image object to convert to ASCII
# fontName -> The path to a valid font file with extension. Only .ttf files supported.
# fontSize -> The size the font should be rendered at. Smaller sizes increase render time, but increase visual resolution.
# warp -> How much warp to apply to the generation of the string. Can create duplications of the image, etc.
def imageToAsciiImageColor(inputImage, fontName, fontSize, warp = DEFAULT_WARP):
    # Get the size of the input image
    (inputW, inputH) = inputImage.size

    # Build the ascii image list
    imageAsciiList = imageToAsciiList(inputImage, warp)

    # Build the ascii color list
    imageColorList = imageToColorList(inputImage, warp)

    # Check if verbose status should be stated
    if VERBOSE:
        # Print the build image response
        print('Building output color image...')

    # Create an output image
    outputImage = Image.new('RGB', (inputW, inputH), 'black')

    # Prepare the output image to be drawn on
    outputDraw = ImageDraw.Draw(outputImage)

    # Build the draw font
    font = ImageFont.truetype(fontName, fontSize)

    # Calculate the max amount of characters for width and height
    maxCharW = int(inputW/fontSize)
    maxCharH = int(inputH/fontSize)

    # Calculate the required step for the width and height to match output
    widthStep = int(inputW/maxCharW) # for char
    heightStep = int(inputH/maxCharH) # for line

    # Loop through the ascii list
    cursorY = 0
    colorIndex = 0
    for lineInd in range(0, len(imageAsciiList), widthStep):
        # Get the line
        line = imageAsciiList[lineInd]

        # Loop through the appropriate amount of characters for the row
        cursorX = 0
        for charInd in range(0, len(line), heightStep):
            # Draw the character
            outputDraw.text((cursorX, cursorY), line[charInd], imageColorList[colorIndex], font)

            # Iterate x cursor
            cursorX = cursorX+fontSize

            # Iterate the color index
            colorIndex += 1

        # Increase y cursor
        cursorY = cursorY+fontSize

    # Check if verbose status should be stated
    if VERBOSE:
        # Print the build image done response
        print('Done building output color image.')

    # Return the output image
    return outputImage

# Calculates and return the aspect ratio of the provided size values
def calculateAspectRatio(width, height):
    # Calculate the greates common denominator
    gcd = math.gcd(width, height)

    # Calculate the aspect ratios
    arW = width/gcd
    arH = height/gcd

    # Return them in a tuple
    return (arW, arH)

# Checks for the required specs within the provided render specifications and fills them with the default values if they are not specified.
# For optional render specifications, the function simply adds the default value for the entry but does so silently.
def validateSpecs(specs):
    # Check if verbose status should be stated
    if VERBOSE:
        # Print the validating specs
        print('Validating provided render specifications...')

    # Check for a path
    if 'path' not in specs:
        print('Specifications Validator: No Input File was provided in the specs. Could not continue.')
        raise FileNotFoundError

    # Check for an output
    if 'output' not in specs:
        print('Specifications Validator: No Output File was provided in the specs. Could not continue.')
        raise FileNotFoundError

    # Check for a font file
    if 'fontFile' not in specs:
        print('Specifications Validator: No Font File was provided in the specs. Could not continue.')
        raise FileNotFoundError

    # Check for a font size
    if 'fontSize' not in specs:
        print('Specifications Validator: Set the font size to the default of '+str(DEFAULT_FONT_SIZE)+'.')
        specs['fontSize'] = DEFAULT_FONT_SIZE

    # Check for font colors
    if 'fontColors' not in specs:
        specs['fontColors'] = DEFAULT_TEXT_COLORS

    # Check for background color
    if 'backgroundColor' not in specs:
        specs['backgroundColor'] = DEFAULT_BACKGROUND_COLOR

    # Check for warp
    if 'warp' not in specs:
        specs['warp'] = DEFAULT_WARP

    # Check if verbose status should be stated
    if VERBOSE:
        # Print finished validating specs
        print('Finished validating render specifications.')

    # Return the modified specs
    return specs

## Deployment Functions
# Processes a single filepath into an ASCII image rendered .png file with the provided specs
# NOTE: Check the Read Me for details on the format of the specifications dictionary.
def processImageToAscii(specs):
    # Check if an output name was provided
    if 'output' in specs:
        # Process the image to an ASCII image
        outputImage = imagePathToAsciiImage(specs)

        # Save the image
        outputImage.save(specs['output']+'.png')
    else:
        # Report a problem
        print('ERROR: No output file was provided for conversion.')

# Converts a provided video file into an OpenCV video object
# NOTE: (1) This function _will_ take a long time to execute. A video encoded at 1080p 60fps with a length of 15 seconds took about 30 minutes to render.
# NOTE: (2) Check the Read Me for details on the format of the specifications dictionary.
def videoToAsciiVideoFile(specs):
    # Validate the provided specs
    specs = validateSpecs(specs)

    # Check if verbose status should be stated
    if VERBOSE:
        # Report the video file being loaded
        print('> Loading video file...')

    # Capture the video file
    vidCap = cv.VideoCapture(specs['path'])

    # Check if verbose status should be stated
    if VERBOSE:
        # Report the video file loaded and frame processing start
        print('> Loaded video file.')
        print('> Processing video frames, this may take a while...')

    # Get the details of the video
    vidFrameCount = int(vidCap.get(cv.CAP_PROP_FRAME_COUNT))
    vidFrameSpeed = vidCap.get(cv.CAP_PROP_FPS)
    vidW = int(vidCap.get(cv.CAP_PROP_FRAME_WIDTH))
    vidH = int(vidCap.get(cv.CAP_PROP_FRAME_HEIGHT))

    # Open the video writer
    vidWritterFourCC = cv.VideoWriter_fourcc(*'MP4V') # MP4V, X264
    vidWritter = cv.VideoWriter(specs['output']+'.mp4', vidWritterFourCC, vidFrameSpeed, (vidW, vidH))

    # Enter the frame loop
    moreFrames = True
    frameCount = 1
    prevFrame = None
    prevAscii = None
    while(moreFrames):
        # Check if verbose status should be stated
        if VERBOSE:
            # Report the frame being processed
            print('> Processing frame '+str(frameCount)+'/'+str(vidFrameCount))

        # Get if there are more frames and the current frame image
        moreFrames, imageCv = vidCap.read()

        # Check if more frames are present
        if moreFrames:
            # Make sure the current frame is not the same as the previous
            if not np.array_equal(imageCv, prevFrame):
                # Convert the CV image to a Pil image
                imagePil = Image.fromarray(cv.cvtColor(imageCv, cv.COLOR_BGR2RGB))

                # Convert the Pil image to an ASCII image in Pil format
                imageAscii = imageToAsciiImage(imagePil, specs)

                # Convert the ASCII image to a numpy array
                imageAsciiArray = np.array(imageAscii)

                # Convert the image back to a CV image
                imageCvAscii = cv.cvtColor(imageAsciiArray, cv.COLOR_RGB2BGR)

                # Send the image to the video writter
                vidWritter.write(imageCvAscii)

                # Assign the previous frame and ASCII render
                prevFrame = imageCv
                prevAscii = imageCvAscii
            else:
                # Check if verbose status should be stated
                if VERBOSE:
                    # Report the frame being processed
                    print('Skipping render for frame '+str(frameCount)+' because: duplicate')

                # Write the previous ASCII image to the video
                vidWritter.write(prevAscii)
        else:
            # Exit the loop
            break

        # Iterate the count
        frameCount += 1

    # Release the video processors
    vidCap.release()
    vidWritter.release()

    # Make sure any CV windows are closed
    cv.destroyAllWindows()

    # Check if verbose status should be stated
    if VERBOSE:
        # Report the frames have been process
        print('> Video frames processed.')

## Main Thread Execution
if __name__=='__main__':
    # Report this is a package
    print('asciiConverter.py is a package, not an executable Python script.')
