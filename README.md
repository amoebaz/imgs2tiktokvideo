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

## Configuration
The different configuration variables are on the top side of the script. Here's an example:

- video_width = 1080
- video_height = 1920
- video_fps = 60
- duration_per_image = 2
- duration_of_transition = 0.25
- titulo_video = "Video Title"
- subtitulo_video = "Video Subtitle"

## Watermark
You can use a watermark in the root dir named as "watermark.png". Check the code to optimize its size and position.

## Future works
Among my plans are:
- Check for horizontal photos and generate sets of three to create a vertical slide.
- Create new transitions.
- Animated watermark.