# Image Manipulator
# Manipulates the provided image with the appropriate settings

# Imports
import asciiConverter as ac
import generalUtilities as gu
import json

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
        choiceProcessOrder()
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

    # Manipulate the image
    manipulateImage(targetType, filepath, outputName, FONT_FONT, fontSize, textColors, backgroundColor, warp)

# Runs the image manipulations with the provided parameters
def manipulateImage(targetType, filepath, outputName, fontFile, fontSize, fontColors, backgroundColor, warp):
    # Start the clocker
    gu.startClocker('img2ascii', '\nStarted clocking...')

    # Decide which function to run
    if targetType == 'image':
        # Process the image
        ac.processImageToAscii(filepath, outputName, FONT_FONT, fontSize, warp, fontColors, backgroundColor)
    elif targetType == 'video':
        # Process the video
        ac.videoToAsciiVideoFile(filepath, outputName, FONT_FONT, fontSize, warp, fontColors, backgroundColor)
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

# Trigger the process order logic process
def choiceProcessOrder():
    # Ask for the order filepath
    orderPath = gu.managedInput('Enter the path to the desired order file', 'Cancel')

    # Check if an order file was provided
    if orderPath != None:
        # Start the clocker
        gu.startClocker('orderProcesser', '\nStarted order clocking...')

        try:
            # Load the order file
            orderData = gu.readFullFile(orderPath)

            # Parse the json
            order = json.loads(orderData)

            # Loop through the order
            partNum = 1
            for part in order:
                # Report the current item
                print('\nProcessing order part '+str(partNum)+'/'+str(len(order))+': '+part['path'])
                
                # Manipulate the image according to the order
                manipulateImage(part['type'], part['path'], part['output'], part['fontFile'], part['fontSize'], part['fontColors'], part['backgroundColor'], part['warp'])

                # Iterate
                partNum += 1

        except FileNotFoundError:
            print("File at '"+orderPath+"' could not be found.")

        # End the clocker
        gu.endClocker('orderProcesser', message='\nOrder completed in ')

# Main Thread Execution
if __name__=='__main__':
    main()