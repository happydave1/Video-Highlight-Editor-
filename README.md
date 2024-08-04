# Python Video Highlight Editor

### Setting up project

Clone into the repository, then run `pip install requirements.txt` to install dependencies.
Note that moviepy requires ffmpeg and ImageMagick to run, so make sure to install those.
If you are on linux, you have to set the environment variable `IMAGEMAGICK_BINARY` to `usr/bin/convert`, or wherever the ImageMagick exectutable is located.
You can do this with: `env IMAGEMAGICK_BINARY=usr/bin/convert`
Linux users can use `which convert` to find where ImageMagick is installed.

Windows users must download ffmpeg and ImageMagick from their respective websites. Make sure that the ImageMagick environment variable in the code is changed to reflect the location of the executable.

Run the program with `python main.py`.

Place videos which you wish to turn into clips into the `highlights` folder. Note that the outputs will be available in `outputs` folder and if you create a final reel, it will be available in the `outputs/final_videos` folder

Users may delete the `IGNORE.txt` files once they have cloned the repository if they so choose to.
