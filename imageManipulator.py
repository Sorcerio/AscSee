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
        pass
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

# Main Thread Execution
if __name__=='__main__':
    main()