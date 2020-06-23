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

    # Start the clocker
    gu.startClocker('img2ascii')

    # ac.processImageToAscii('testImage2.png', 'output', FONT_FONT, FONT_SIZE)
    # ac.processBatchImagesToAscii(['testImage.jpg', 'testImage2.png', 'testImage3.jpg', 'testImage4.jpg', 'testImage5.jpg', 'testImage6.jpg'], FONT_FONT, FONT_SIZE)

    ac.videoToAsciiVideoFile('testVideo.mp4', 'output.mp4', FONT_FONT, FONT_SIZE)

    # End the clocker
    gu.endClocker('img2ascii')

# Functions

# Main Thread Execution
if __name__=='__main__':
    main()