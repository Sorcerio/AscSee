# Image Manipulator
# Manipulates the provided image with the appropriate settings

# Imports
import asciiConverter as ac
import generalUtilities as gu

# Variables
FONT_FONT = 'arial.ttf' # Only in .ttf
FONT_SIZE = 16 # Lowering font size will increase the visual resolution of the image, but increase the render time of each
COLORS_WEB = ['AliceBlue', 'AntiqueWhite', 'Aqua', 'Aquamarine', 'Azure', 'Beige', 'Bisque', 'Black', 'BlanchedAlmond', 'Blue', 'BlueViolet', 'Brown', 'BurlyWood', 'CadetBlue', 'Chartreuse', 'Chocolate', 'Coral', 'CornflowerBlue', 'Cornsilk', 'Crimson', 'Cyan', 'DarkBlue', 'DarkCyan', 'DarkGoldenRod', 'DarkGray', 'DarkGrey', 'DarkGreen', 'DarkKhaki', 'DarkMagenta', 'DarkOliveGreen', 'DarkOrange', 'DarkOrchid', 'DarkRed', 'DarkSalmon', 'DarkSeaGreen', 'DarkSlateBlue', 'DarkSlateGray', 'DarkSlateGrey', 'DarkTurquoise', 'DarkViolet', 'DeepPink', 'DeepSkyBlue', 'DimGray', 'DimGrey', 'DodgerBlue', 'FireBrick', 'FloralWhite', 'ForestGreen', 'Fuchsia', 'Gainsboro', 'GhostWhite', 'Gold', 'GoldenRod', 'Gray', 'Grey', 'Green', 'GreenYellow', 'HoneyDew', 'HotPink', 'IndianRed ', 'Indigo', 'Ivory', 'Khaki', 'Lavender', 'LavenderBlush', 'LawnGreen', 'LemonChiffon', 'LightBlue', 'LightCoral', 'LightCyan', 'LightGoldenRodYellow', 'LightGray', 'LightGrey', 'LightGreen', 'LightPink', 'LightSalmon', 'LightSeaGreen', 'LightSkyBlue', 'LightSlateGray', 'LightSlateGrey', 'LightSteelBlue', 'LightYellow', 'Lime', 'LimeGreen', 'Linen', 'Magenta', 'Maroon', 'MediumAquaMarine', 'MediumBlue', 'MediumOrchid', 'MediumPurple', 'MediumSeaGreen', 'MediumSlateBlue', 'MediumSpringGreen', 'MediumTurquoise', 'MediumVioletRed', 'MidnightBlue', 'MintCream', 'MistyRose', 'Moccasin', 'NavajoWhite', 'Navy', 'OldLace', 'Olive', 'OliveDrab', 'Orange', 'OrangeRed', 'Orchid', 'PaleGoldenRod', 'PaleGreen', 'PaleTurquoise', 'PaleVioletRed', 'PapayaWhip', 'PeachPuff', 'Peru', 'Pink', 'Plum', 'PowderBlue', 'Purple', 'RebeccaPurple', 'Red', 'RosyBrown', 'RoyalBlue', 'SaddleBrown', 'Salmon', 'SandyBrown', 'SeaGreen', 'SeaShell', 'Sienna', 'Silver', 'SkyBlue', 'SlateBlue', 'SlateGray', 'SlateGrey', 'Snow', 'SpringGreen', 'SteelBlue', 'Tan', 'Teal', 'Thistle', 'Tomato', 'Turquoise', 'Violet', 'Wheat', 'White', 'WhiteSmoke', 'Yellow', 'YellowGreen']

# Main Thread
def main():
    # Set the ASCII Converter to Verbose
    ac.toggleVerbose()

    gu.presentPagedMultiSelect('Color Selection', COLORS_WEB, 'Confirm', cancelOption='Cancel')

    # # Present the main menu
    # gu.textMenu('AscSee', ['Convert Image', 'Convert Video', 'Settings'], 'Quit', menuMain)

# Functions
# Handles the main menu inputs
def menuMain(choice):
    if choice == '0':
        # Convert Image
        choiceConvertItem('image')
    elif choice == '1':
        # Convert Video
        choiceConvertItem('video')
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
def choiceConvertItem(targetType):
    # Get the filepath
    filepath = gu.managedInputForced('Enter the filepath of the source '+targetType)

    # Get the output name
    outputName = gu.managedInputForced('Enter the name for the output file (without extension)')

    # Ask if advanced options are needed
    warp = ac.getDefaultWarp()
    textColors = ac.getDefaultTextColors()
    backgroundColor = ac.getDefaultBackgroundColor()
    if gu.askUserYesNo('Modify advanced options?', True):
        # Advanced options
        (warp, backgroundColor) = askForAdvancedSettings()

    # Start the clocker
    gu.startClocker('img2ascii', '\nStarted clocking...')

    # Decide which function to run
    if targetType == 'image':
        # Process the image
        ac.processImageToAscii(filepath, outputName, FONT_FONT, FONT_SIZE, warp, textColors, backgroundColor)
    elif targetType == 'video':
        # Process the video
        ac.videoToAsciiVideoFile(filepath, outputName, FONT_FONT, FONT_SIZE, warp, textColors, backgroundColor)
    else:
        # Report a problem
        print(str(targetType)+' is not a valid conversion target type.')

    # End the clocker
    gu.endClocker('img2ascii')

# Asks the user for advanced settings
def askForAdvancedSettings():
    # Get a warp
    print('\nDefault warp is '+str(ac.getDefaultWarp())+'.')
    warp = gu.managedInputNumberForced('Enter a warp value')

    # TODO: Write a way to multiselect from colors neatly in a small console window

    # Get a background color
    print('\nDefault background color is '+str(ac.getDefaultBackgroundColor())+'.')
    print('A list of webcolors can be found here: https://www.w3schools.com/colors/colors_names.asp')
    backgroundColor = gu.askUser('Enter a Web Color as background color', COLORS_WEB,False)

    # Send back the result
    return (warp, backgroundColor)

# Main Thread Execution
if __name__=='__main__':
    main()