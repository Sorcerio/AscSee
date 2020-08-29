# Image Manipulator
# Manipulates the provided image with the appropriate settings

# Imports
import asciiConverter as ac
import generalUtilities as gu

# Variables
FONT_FONT = 'arial.ttf' # Only in .ttf
FONT_SIZE = 16 # Lowering font size will increase the visual resolution of the image, but increase the render time of each

# Main Thread
def main():
    # Set the ASCII Converter to Verbose
    ac.toggleVerbose()

    # Present the main menu
    gu.textMenu('AscSee', ['Process Order', 'Order Creation Wizard', 'Convert Image', 'Convert Video', 'Settings'], 'Quit', menuMain)

# Functions
# Handles the main menu inputs
def menuMain(choice):
    if choice == '0':
        # Process an order
        print('TODO: Process order files.')
    elif choice == '1':
        # Run the order creation wizard
        print('TODO: Run the Order Creation Wizard.')
    elif choice == '2':
        # Convert Image
        choiceConvertItem('image')
    elif choice == '3':
        # Convert Video
        choiceConvertItem('video')
    elif choice == '4':
        # Settings Menu
        gu.textMenu('AscSee Settings', ['Set Font File'], 'Back', menuSettings)

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

# Triggers the Convert Image logic
def choiceConvertItem(targetType):
    # Get the filepath
    filepath = gu.managedInputForced('Enter the filepath of the source '+targetType)

    # Get the output name
    outputName = gu.managedInputForced('Enter the name for the output file (without extension)')

    # Ask if advanced options are needed
    warp = ac.getDefaultWarp()
    fontSize = FONT_SIZE
    textColors = ac.getDefaultTextColors()
    backgroundColor = ac.getDefaultBackgroundColor()
    if gu.askUserYesNo('Modify advanced options?', True):
        # Advanced options
        (warp, fontSize, textColors, backgroundColor) = askForAdvancedSettings()

    # Start the clocker
    gu.startClocker('img2ascii', '\nStarted clocking...')

    # Decide which function to run
    if targetType == 'image':
        # Process the image
        ac.processImageToAscii(filepath, outputName, FONT_FONT, fontSize, warp, textColors, backgroundColor)
    elif targetType == 'video':
        # Process the video
        ac.videoToAsciiVideoFile(filepath, outputName, FONT_FONT, fontSize, warp, textColors, backgroundColor)
    else:
        # Report a problem
        print(str(targetType)+' is not a valid conversion target type.')

    # End the clocker
    gu.endClocker('img2ascii')

# Asks the user for advanced settings
def askForAdvancedSettings():
    # Get the colors
    webColors = ac.getColors()

    # Get a warp
    print('\nDefault warp is '+str(ac.getDefaultWarp())+'.')
    warp = gu.managedInputNumberForced('Enter a warp value')

    # Get a font size
    print('\nDefault font size is '+str(FONT_SIZE)+'.')
    fontSize = gu.managedInputNumberRangeForced('Enter a new font size', 10000, 1)

    # Get the text colors
    print('\nDefault text colors: '+', '.join(ac.getDefaultTextColors()))
    textColors = gu.presentPagedMultiSelect(None, webColors, 'Confirm')

    # Get a background color
    print('\nDefault background color is '+str(ac.getDefaultBackgroundColor())+'.')
    backgroundColor = gu.presentPagedMultiSelect(None, webColors, 'Confirm', maxSelect=1)[0]

    # Send back the result
    return (warp, fontSize, textColors, backgroundColor)

# Main Thread Execution
if __name__=='__main__':
    main()