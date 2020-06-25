# AscSee Multi-Media Filter
![AscSee Social Image](./DemoImages/social.jpg)

AscSee allows for the conversion of standard multi-media to ASCII styled images in both image and video outputs using Python.
The package comes with both the methods to do so, in `asciiConverter.py`, and a command line interface powered by my [General Utilities Library](https://github.com/maximombro/Python-General-Utilities) for ease of use found in `imageManipulator.py`.

# Examples
## Images
See the banner above for examples of single image output.
Render time for indivigual images is dependent on input file size, but otherwise generally takes between 2 seconds (for web images) and 3 minutes (for images taken directly from a DSLR).

### Image Examples
![Comparison of Font Sizes on the Output Render](./DemoImages/FontSizeComparison.jpg)
Larger Images: [Base Image](./DemoImages/imageBase.png), [16px Image](./DemoImages/image16.png), [8px Image](./DemoImages/image8.png), [1px Image](./DemoImages/image1.png)

## Videos
Rendering ASCII styled videos is entirely possible within AscSee.
However, it should be noted that render times for these types of media are much longer than for an indivigual image. This is because video files are simply just a series of images shown at a designated frame rate. For example, a video at 30fps shows 30 indivigual frames per second and each of these frames is indivigually rendered.

It should also be noted, that rendering through AscSee _will_ strip the video of its audio. However, this can always be transfered from the original video file to the AscSee output video file through the use of video editing software.

### Video Examples
To put this in perspective here is an example:

The video below is the base video with no AscSee rendering. It is 1920x1080p, 60fps, and 3:03 minutes (>10000 frames) long with a file size of 354mbs.

[![Video Before Being Run Through AscSee](http://img.youtube.com/vi/dA6JgSP_CHE/0.jpg)](https://youtu.be/dA6JgSP_CHE)

The video below is the base video rendered with a 16px font. It took 5 hours, 31 minutes and the output file was 3.1gigs. When compressed with settings to match the source, with [HandBrake](https://handbrake.fr/), file size was reduced to 635mbs. [Premiere Pro](https://www.adobe.com/products/premiere.html) was then used to transfer the audio from the source file to the AscSee output file, before uploading the file to YouTube. _No other alterations were applied._

[![Video with 16px Rendering](http://img.youtube.com/vi/KaoTze7lNpc/0.jpg)](https://youtu.be/KaoTze7lNpc)

The video below is the base video rendered with an 8px font. It took 17 hours, 31 minutes, 12.86 seconds and the output file was 4.85gigs. When compressed with settings to match the source, with [HandBrake](https://handbrake.fr/), file size was reduced to 950mbs. [Premiere Pro](https://www.adobe.com/products/premiere.html) was then used to transfer the audio from the source file to the AscSee output file, before uploading the file to YouTube. _No other alterations were applied._

[![Video with 8px Rendering](http://img.youtube.com/vi/ihUtVyx3fqE/0.jpg)](https://youtu.be/ihUtVyx3fqE)

The video below shows all three videos next to each other for easy comparison.

[![Video Showing Rendering Comparison](http://img.youtube.com/vi/TPwV90AqXS8/0.jpg)](https://youtu.be/TPwV90AqXS8)

## Usage
### Requirements
* [Python 3.*](https://www.python.org/downloads/)
* [Pillow Library 7.*](https://pillow.readthedocs.io/en/stable/)
    * For all renders.
    * `pip install Pillow`
* [OpenCV Library](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_tutorials.html)
    * For videos render only.
    * `pip install opencv-python`
* [Numpy](https://numpy.org/)
* [General Utilities Library](https://github.com/maximombro/Python-General-Utilities)
    * Comes in the package.
* A TrueTypeFont Font
    * Be sure to link this font file within `imageManipulator.py`.

### Instructions for Command Line Interface
As the cliche goes, the Command Line Interface is simple to use. It can be run by simply by executing `imageManipulator.py` with Python. Once activated, the program will move through a series of menus allowing for the selection of images or videos and advanced settings for the render. Most errors are caught, however, it should be noted that the Command Line Interface is intended primarily as a demo for the functions within AscSee.
Regardless, be sure you have a _valid_ font file specified in the `imageManipulator.py` file. By default it uses `./arial.tff` which should be a font most computers will have. You just simply need to link to it where it exists on your computer with a direct filepath, or copy the `.tff` file to the AscSee directory (this is how it was done in testing).
