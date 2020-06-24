# Image Manipulator
# Manipulates the provided image with the appropriate settings

# Imports
import asciiConverter as ac
import generalUtilities as gu

# Variables
FONT_FONT = 'arial.ttf' # Only in .ttf
FONT_SIZE = 16 # Lowering font size will increase the visual resolution of the image, but increase the render time of each
COLORS_WEB = ['AliceBlue', 'AntiqueWhite', 'Aqua', 'Aquamarine', 'Azure', 'Beige', 'Bisque', 'Black', 'BlanchedAlmond', 'Blue', 'BlueViolet', 'Brown', 'BurlyWood', 'CadetBlue', 'Chartreuse', 'Chocolate', 'Coral', 'CornflowerBlue', 'Cornsilk', 'Crimson', 'Cyan', 'DarkBlue', 'DarkCyan', 'DarkGoldenRod', 'DarkGray', 'DarkGrey', 'DarkGreen', 'DarkKhaki', 'DarkMagenta', 'DarkOliveGreen', 'DarkOrange', 'DarkOrchid', 'DarkRed', 'DarkSalmon', 'DarkSeaGreen', 'DarkSlateBlue', 'DarkSlateGray', 'DarkSlateGrey', 'DarkTurquoise', 'DarkViolet', 'DeepPink', 'DeepSkyBlue', 'DimGray', 'DimGrey', 'DodgerBlue', 'FireBrick', 'FloralWhite', 'ForestGreen', 'Fuchsia', 'Gainsboro', 'GhostWhite', 'Gold', 'GoldenRod', 'Gray', 'Grey', 'Green', 'GreenYellow', 'HoneyDew', 'HotPink', 'IndianRed ', 'Indigo', 'Ivory', 'Khaki', 'Lavender', 'LavenderBlush', 'LawnGreen', 'LemonChiffon', 'LightBlue', 'LightCoral', 'LightCyan', 'LightGoldenRodYellow', 'LightGray', 'LightGrey', 'LightGreen', 'LightPink', 'LightSalmon', 'LightSeaGreen', 'LightSkyBlue', 'LightSlateGray', 'LightSlateGrey', 'LightSteelBlue', 'LightYellow', 'Lime', 'LimeGreen', 'Linen', 'Magenta', 'Maroon', 'MediumAquaMarine', 'MediumBlue', 'MediumOrchid', 'MediumPurple', 'MediumSeaGreen', 'MediumSlateBlue', 'MediumSpringGreen', 'MediumTurquoise', 'MediumVioletRed', 'MidnightBlue', 'MintCream', 'MistyRose', 'Moccasin', 'NavajoWhite', 'Navy', 'OldLace', 'Olive', 'OliveDrab', 'Orange', 'OrangeRed', 'Orchid', 'PaleGoldenRod', 'PaleGreen', 'PaleTurquoise', 'PaleVioletRed', 'PapayaWhip', 'PeachPuff', 'Peru', 'Pink', 'Plum', 'PowderBlue', 'Purple', 'RebeccaPurple', 'Red', 'RosyBrown', 'RoyalBlue', 'SaddleBrown', 'Salmon', 'SandyBrown', 'SeaGreen', 'SeaShell', 'Sienna', 'Silver', 'SkyBlue', 'SlateBlue', 'SlateGray', 'SlateGrey', 'Snow', 'SpringGreen', 'SteelBlue', 'Tan', 'Teal', 'Thistle', 'Tomato', 'Turquoise', 'Violet', 'Wheat', 'White', 'WhiteSmoke', 'Yellow', 'YellowGreen']

# TODO: Provide defaults for warp, textColors, and backgroundColor within asciiConverter
DEFAULT_WARP = 0
DEFAULT_TEXT_COLORS = ['white']
DEFAULT_BACKGROUND_COLOR = 'black'

# Main Thread
def main():
    # Set the ASCII Converter to Verbose
    ac.toggleVerbose()

    # Present the main menu
    gu.textMenu('AscSee', ['Convert Image', 'Convert Video', 'Settings'], 'Quit', menuMain)

    # # Start the clocker
    # gu.startClocker('img2ascii')

    # # ac.processImageToAscii('testImage2.png', 'output', FONT_FONT, FONT_SIZE)
    # # ac.processBatchImagesToAscii(['testImage.jpg', 'testImage2.png', 'testImage3.jpg', 'testImage4.jpg', 'testImage5.jpg', 'testImage6.jpg'], FONT_FONT, FONT_SIZE)

    # ac.videoToAsciiVideoFile('testVideo.mp4', 'output.mp4', FONT_FONT, FONT_SIZE)

    # # End the clocker
    # gu.endClocker('img2ascii')

# Functions
# Handles the main menu inputs
def menuMain(choice):
    if choice == '0':
        # Convert Image
        choiceConvertImage()
    elif choice == '1':
        # Convert Video
        pass
    elif choice == '2':
        # Settings Menu
        # Build the choices
        choices = [
            'Set Font File',
            'Set Font Size'
        ]

        # Open the settings menu
        gu.textMenu('AscSee Settings', choices, 'Back', menuSettings)

# Handles the settings menu inputs
def menuSettings(choice):
    # Scope the globals
    global FONT_FONT
    global FONT_SIZE

    # Handle choices
    if choice == '0':
        # Set the font file
        # Print the current file
        print('\nCurrent font file is at: '+str(FONT_FONT)+'.')

        # Ask for a new file path
        answer = gu.managedInput('Enter the file path to the font file', 'Cancel')

        # Check if an answer was provided
        if answer != None:
            # Change the value
            FONT_FONT = answer

            # Report the value changed
            print('\nFont changed to '+str(FONT_FONT))
    elif choice == '1':
        # Set the font size
        # Print the current size
        print('\nCurrent font size is: '+str(FONT_SIZE)+'px.')

        # Ask for a new font size
        answer = gu.managedInputNumberRange('Enter a new font size', 10000, 1, 'Cancel')

        # Check if an answer was provided
        if answer != None:
            # Change the value
            FONT_SIZE = answer

            # Report the value changed
            print('\nFont Size changed to '+str(FONT_SIZE))

# Triggers the Convert Image logic
def choiceConvertImage():
    # filepath, outputName, fontFile, fontSize, warp = 0, textColors = ['white'], backgroundColor = 'black'
    # Get the filepath
    filepath = gu.managedInputForced('Enter the filepath of the Image')

    # Get the output name
    outputName = gu.managedInputForced('Enter the name for the output file (without extension)')

    # Ask if advanced options are needed
    warp = 0
    textColors = ['white']
    backgroundColor = 'black'
    if gu.askUserYesNo('Modify advanced options?', True):
        # Advanced options
        # Get a warp
        print('\nDefault warp is '+str(DEFAULT_WARP)+'.')
        warp = gu.managedInputNumberForced('Enter a warp value')

        # Get a background color
        print('\nDefault background color is '+str(DEFAULT_BACKGROUND_COLOR)+'.')
        print('A list of webcolors can be found here: https://www.w3schools.com/colors/colors_names.asp')
        backgroundColor = gu.managedInputForcedWhitelist('Enter a Web Color as background color', COLORS_WEB, True)

    # Start the clocker
    gu.startClocker('img2ascii')

    # Process the image
    ac.processImageToAscii(filepath, outputName, FONT_FONT, FONT_SIZE, warp, textColors, backgroundColor)

    # End the clocker
    gu.endClocker('img2ascii')

# Main Thread Execution
if __name__=='__main__':
    main()