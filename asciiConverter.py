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
# Converts the provided 
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

# Converts an image at the specified filepath to an ASCII image object
# filepath -> The path to a valid image file with extension.
# fontName -> The path to a valid font file with extension. Only .ttf files supported.
# fontSize -> The size the font should be rendered at. Smaller sizes increase render time, but increase visual resolution.
# warp -> How much warp to apply to the generation of the string. Can create duplications of the image, etc.
# textColors -> The colors for the text to be (use the names of common HTML colors). A color is chosen randomly from the list.
#   for each drawn character. If None is provided, a color will be chosen randomly for each character
# backgroundColor -> The color the backgrond should be (use the name of a common HTML color).
def imagePathToAsciiImage(filepath, fontName, fontSize, warp = DEFAULT_WARP, textColors = DEFAULT_TEXT_COLORS, backgroundColor = DEFAULT_BACKGROUND_COLOR):
    # Try to get the input image
    try:
        # Try to get the input image
        inputImage = Image.open(filepath)

        # Convert and return the image
        return imageToAsciiImage(inputImage, fontName, fontSize, warp, textColors, backgroundColor)
    except Exception as err:
        # Print the problem
        print("Image at "+str(inputImage)+" could not opened.")

        # Return an error image
        return Image.new('RGB', (100, 100), 'red')

# Converts the provided image to an ASCII image object
# inputImage -> A PIL image object to convert to ASCII
# fontName -> The path to a valid font file with extension. Only .ttf files supported.
# fontSize -> The size the font should be rendered at. Smaller sizes increase render time, but increase visual resolution.
# warp -> How much warp to apply to the generation of the string. Can create duplications of the image, etc.
# textColors -> The colors for the text to be (use the names of common HTML colors). A color is chosen randomly from the list.
#   for each drawn character. If None is provided, a color will be chosen randomly for each character
# backgroundColor -> The color the backgrond should be (use the name of a common HTML color).
def imageToAsciiImage(inputImage, fontName, fontSize, warp = DEFAULT_WARP, textColors = DEFAULT_TEXT_COLORS, backgroundColor = DEFAULT_BACKGROUND_COLOR):
    # Check if text colors is None
    if textColors == None:
        textColors = COLORS_WEB

    # Get the size of the input image
    (inputW, inputH) = inputImage.size

    # Build the ascii image list
    imageAsciiList = imageToAsciiList(inputImage, warp)

    # Check if verbose status should be stated
    if VERBOSE:
        # Print the build image response
        print('Building output image...')

    # Create an output image
    outputImage = Image.new('RGB', (inputW, inputH), backgroundColor)

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
    for lineInd in range(0, len(imageAsciiList), widthStep):
        # Get the line
        line = imageAsciiList[lineInd]

        # Loop through the appropriate amount of characters for the row
        cursorX = 0
        for charInd in range(0, len(line), heightStep):
            # Draw the character
            outputDraw.text((cursorX, cursorY), line[charInd], random.choice(textColors), font)

            # Iterate x cursor
            cursorX = cursorX+fontSize

        # Increase y cursor
        cursorY = cursorY+fontSize

    # Check if verbose status should be stated
    if VERBOSE:
        # Print the build image done response
        print('Done building output image.')

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

## Deployment Functions
# Processes a single filepath into an ASCII image rendered .png file
def processImageToAscii(filepath, outputName, fontFile, fontSize, warp = DEFAULT_WARP, textColors = DEFAULT_TEXT_COLORS, backgroundColor = DEFAULT_BACKGROUND_COLOR):
    # Process the image to an ASCII image
    outputImage = imagePathToAsciiImage(filepath, fontFile, fontSize, warp, textColors, backgroundColor)

    # Save the image
    outputImage.save(str(outputName)+'.png')

# Processes a list of filepaths into ASCII image rendered .png files
def processBatchImagesToAscii(filepaths, fontFile, fontSize, warp = DEFAULT_WARP, textColors = DEFAULT_TEXT_COLORS, backgroundColor = DEFAULT_BACKGROUND_COLOR):
    # Check if verbose status should be stated
    if VERBOSE:
        # Print the batch process start
        print('Starting batch process with '+str(len(filepaths))+' images...')

    # Loop through the filepath array
    i = 1
    for filepath in filepaths:
        # Print the image being process
        print('Processing '+str(filepath)+'('+str(i)+'/'+str(len(filepaths))+')')

        # Process the image
        processImageToAscii(filepath, ('output'+str(i)), fontFile, fontSize, warp, textColors, backgroundColor)

        # Iterate
        i = i+1

    # Check if verbose status should be stated
    if VERBOSE:
        # Print the batch process end
        print('Finished batch process.')

# Converts a provided video file into an OpenCV video object
# NOTE: This function _will_ take a long time to execute. A video encoded at 1080p 60fps with a length of
#       15 seconds took about 30 minutes to render
# filepath -> The video file to convert with extension with .mp4 extension.
# outputPath -> The output path file to save the converted video to with .mp4 extension.
# fontName -> The path to a valid font file with extension. Only .ttf files supported.
# fontSize -> The size the font should be rendered at. Smaller sizes increase render time, but increase visual resolution.
def videoToAsciiVideoFile(filepath, outputPath, fontName, fontSize, warp = DEFAULT_WARP, textColors = DEFAULT_TEXT_COLORS, backgroundColor = DEFAULT_BACKGROUND_COLOR):
    # Report the video file being loaded
    print('> Loading video file...')

    # Capture the video file
    vidCap = cv.VideoCapture(filepath)

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
    vidWritter = cv.VideoWriter(outputPath+'.mp4', vidWritterFourCC, vidFrameSpeed, (vidW, vidH))

    # Enter the frame loop
    moreFrames = True
    frameCount = 1
    while(moreFrames):
        # Report the frame being processed
        print('> Processing frame '+str(frameCount)+'/'+str(vidFrameCount))

        # Capture the current frame
        moreFrames, imageCv = vidCap.read()

        # Check if more frames are present
        if moreFrames:
            # Convert the CV image to a Pil image
            imagePil = Image.fromarray(cv.cvtColor(imageCv, cv.COLOR_BGR2RGB))

            # Convert the Pil image to an ASCII image in Pil format
            imageAscii = imageToAsciiImage(imagePil, fontName, fontSize, warp, textColors, backgroundColor)

            # Convert the ASCII image to a numpy array
            imageAsciiArray = np.array(imageAscii)

            # Convert the image back to a CV image
            imageCvAscii = cv.cvtColor(imageAsciiArray, cv.COLOR_RGB2BGR)

            # Send the image to the video writter
            vidWritter.write(imageCvAscii)
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

    # Report the frames have been process
    print('> Video frames processed.')

## Main Thread Execution
if __name__=='__main__':
    # Report this is a package
    print('asciiConverter.py is a package, not an executable Python script.')
