# imgs2tiktokvideo
Convert vertical images in a slideshow adapted to tiktok format.

## Goal
To be able to generate a slideshow from a set of images to create tiktok videos (and instagram reels) in the most convenient way.

The videos have a random animation between them between:
- Crossfade
- Slide left
- Slide right
- Slide top
- Slide bottom

The transition uses like an "alpha" channel, so images are mounted over the last one.

## Setup
To setup the environment for this script is needed that you have ImageMagick installed in your system and have to modify the file default_config.py in the moviepy python folder and specify the location of the ImageMagick executable file.

## Configuration
The different configuration variables are on the top side of the script. Here's an example:

- video_width = 1080
- video_height = 1920
- video_fps = 60
- duration_per_image = 2
- duration_of_transition = 0.25
- video_title = "Video Title"
- video_subtitle = "Video Subtitle"
 
## Watermark
You can use a watermark in the root dir named as "watermark.png". Check the code to optimize its size and position.

## Future works
Among my plans are:
- Create new transitions.
- Animated watermark.
- More flexible input/output (folder names, video name, etc)