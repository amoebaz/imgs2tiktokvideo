<<<<<<< HEAD
from moviepy.editor import ImageSequenceClip, TextClip, CompositeVideoClip, concatenate_videoclips, VideoClip, ImageClip, transfx
import os
import PIL.Image as Image
import random


video_width = 1080
video_height = 1920
video_fps = 60
duration_per_image = 2
duration_of_transition = 0.25
titulo_video = "Judas Priest"
subtitulo_video = "Rock Imperium 2024"


def crossfade_transition(clip1, clip2, duration=duration_of_transition):
    clip3 = clip2.crossfadein(duration)
    return CompositeVideoClip([
        clip1, clip3.set_start(clip1.duration - duration)
    ], use_bgclip=True)

def slide_transition(clip1, clip2, duration=duration_of_transition, direction='left'):
    clip3 = clip2.fx(transfx.slide_in, duration, side=direction)
    return CompositeVideoClip([
        clip1, clip3.set_start(clip1.duration - duration)
    ], use_bgclip=True)

def create_slideshow(image_folder, output_video, duration_per_image=2, video_size=(video_width, video_height), fps=video_fps):
    # Obtén la lista de imágenes en el directorio especificado
    images = [os.path.join(image_folder, img) for img in os.listdir(image_folder) if img.endswith(('.png', '.jpg', '.jpeg'))]
    
    for img in os.listdir(image_folder):
        print(img)
        im = Image.open(image_folder + "/" + img)
        width, height = im.size
        left = (width - 1080)/2
        top = (height - 1920)/2
        right = (width + 1080)/2
        bottom = (height + 1920)/2

        # Crop the center of the image
        im = im.crop((left, top, right, bottom))
        im.save(image_folder + "/" + img)

    # Volvemos a coger las imágenes ya recortadas y las ordenamos por nombre
    images = [os.path.join(image_folder, img) for img in os.listdir(image_folder) if img.endswith(('.png', '.jpg', '.jpeg'))]
    images.sort()
    
    # Crea un clip de video a partir de la secuencia de imágenes
    clips = [ImageSequenceClip([img], durations=[duration_per_image]).resize(newsize=video_size) for img in images]
    print("CANTIDAD: " + str(len(clips)))
    
    # Añadir transiciones aleatorias entre clips
    transition_types = ['crossfade', 'crossfade' ,'slide_left', 'slide_right', 'slide_top', 'slide_bottom']
    final_clips = [clips[0]]
    for i in range(1, len(clips)):
        transition_type = random.choice(transition_types)
        if transition_type == 'crossfade':
            final_clips.append(crossfade_transition(final_clips[-1], clips[i]))
        elif transition_type == 'slide_left':
            final_clips.append(slide_transition(final_clips[-1], clips[i], duration_of_transition, direction='left'))
        elif transition_type == 'slide_right':
            final_clips.append(slide_transition(final_clips[-1], clips[i], duration_of_transition, direction='right'))
        elif transition_type == 'slide_top':
            final_clips.append(slide_transition(final_clips[-1], clips[i], duration_of_transition, direction='top'))
        elif transition_type == 'slide_bottom':
            final_clips.append(slide_transition(final_clips[-1], clips[i], duration_of_transition, direction='bottom'))
   
    final_clip = final_clips[len(final_clips)-1]

    # Añadir un título al inicio del video (opcional)
    try:
        title_1 = TextClip(titulo_video, fontsize=100, color='white')
        title_1 = title_1.set_position((20, video_height - 2 *(video_height/10))).set_duration(final_clip.duration)
        title_2 = TextClip(subtitulo_video, fontsize=70, color='white')
        title_2 = title_2.set_position((20, video_height - 2 *(video_height/10) + 110)).set_duration(final_clip.duration)
    except Exception as e:
        print(f"Error creating TextClip: {e}")

    # Marca de agua
    lado_marca_agua = video_height / 10
    logo = (ImageClip("watermark.png")
            .set_duration(final_clip.duration)
            .resize(height=(lado_marca_agua), width=(lado_marca_agua))
            .margin(right=20, top=20, opacity=0)
            .set_pos(("right", "top")))

    # Montamos el video con el título, el subtítulo y el logo.
    final_clip = CompositeVideoClip([final_clip, title_1, title_2, logo], use_bgclip=True)


    # Escribe el resultado en un archivo de video
    final_clip.write_videofile(output_video, threads=64, fps=video_fps, codec='libx264')


# Ejemplo de uso
create_slideshow('images', 'output_video.mp4')
=======
from moviepy.editor import ImageSequenceClip, TextClip, CompositeVideoClip, concatenate_videoclips, VideoClip, ImageClip, transfx
import os
import PIL.Image as Image
import random


video_width = 1080
video_height = 1920
video_fps = 60
duration_per_image = 2
duration_of_transition = 0.25
titulo_video = "Judas Priest"
subtitulo_video = "Rock Imperium 2024"


def crossfade_transition(clip1, clip2, duration=duration_of_transition):
    clip3 = clip2.crossfadein(duration)
    return CompositeVideoClip([
        clip1, clip3.set_start(clip1.duration - duration)
    ], use_bgclip=True)

def slide_transition(clip1, clip2, duration=duration_of_transition, direction='left'):
    clip3 = clip2.fx(transfx.slide_in, duration, side=direction)
    return CompositeVideoClip([
        clip1, clip3.set_start(clip1.duration - duration)
    ], use_bgclip=True)

def create_slideshow(image_folder, output_video, duration_per_image=2, video_size=(video_width, video_height), fps=video_fps):
    # Obtén la lista de imágenes en el directorio especificado
    images = [os.path.join(image_folder, img) for img in os.listdir(image_folder) if img.endswith(('.png', '.jpg', '.jpeg'))]
    
    for img in os.listdir(image_folder):
        print(img)
        im = Image.open(image_folder + "/" + img)
        width, height = im.size
        left = (width - 1080)/2
        top = (height - 1920)/2
        right = (width + 1080)/2
        bottom = (height + 1920)/2

        # Crop the center of the image
        im = im.crop((left, top, right, bottom))
        im.save(image_folder + "/" + img)

    # Volvemos a coger las imágenes ya recortadas y las ordenamos por nombre
    images = [os.path.join(image_folder, img) for img in os.listdir(image_folder) if img.endswith(('.png', '.jpg', '.jpeg'))]
    images.sort()
    
    # Crea un clip de video a partir de la secuencia de imágenes
    clips = [ImageSequenceClip([img], durations=[duration_per_image]).resize(newsize=video_size) for img in images]
    print("CANTIDAD: " + str(len(clips)))
    
    # Añadir transiciones aleatorias entre clips
    transition_types = ['crossfade', 'crossfade' ,'slide_left', 'slide_right', 'slide_top', 'slide_bottom']
    final_clips = [clips[0]]
    for i in range(1, len(clips)):
        transition_type = random.choice(transition_types)
        if transition_type == 'crossfade':
            final_clips.append(crossfade_transition(final_clips[-1], clips[i]))
        elif transition_type == 'slide_left':
            final_clips.append(slide_transition(final_clips[-1], clips[i], duration_of_transition, direction='left'))
        elif transition_type == 'slide_right':
            final_clips.append(slide_transition(final_clips[-1], clips[i], duration_of_transition, direction='right'))
        elif transition_type == 'slide_top':
            final_clips.append(slide_transition(final_clips[-1], clips[i], duration_of_transition, direction='top'))
        elif transition_type == 'slide_bottom':
            final_clips.append(slide_transition(final_clips[-1], clips[i], duration_of_transition, direction='bottom'))
   
    final_clip = final_clips[len(final_clips)-1]

    # Añadir un título al inicio del video (opcional)
    try:
        title_1 = TextClip(titulo_video, fontsize=100, color='white')
        title_1 = title_1.set_position((20, video_height - 2 *(video_height/10))).set_duration(final_clip.duration)
        title_2 = TextClip(subtitulo_video, fontsize=70, color='white')
        title_2 = title_2.set_position((20, video_height - 2 *(video_height/10) + 110)).set_duration(final_clip.duration)
    except Exception as e:
        print(f"Error creating TextClip: {e}")

    # Marca de agua
    lado_marca_agua = video_height / 10
    logo = (ImageClip("watermark.png")
            .set_duration(final_clip.duration)
            .resize(height=(lado_marca_agua), width=(lado_marca_agua))
            .margin(right=20, top=20, opacity=0)
            .set_pos(("right", "top")))

    # Montamos el video con el título, el subtítulo y el logo.
    final_clip = CompositeVideoClip([final_clip, title_1, title_2, logo], use_bgclip=True)


    # Escribe el resultado en un archivo de video
    final_clip.write_videofile(output_video, threads=64, fps=video_fps, codec='libx264')


# Ejemplo de uso
create_slideshow('images', 'output_video.mp4')
>>>>>>> eb03450defb1e1cc2b7d4fc9156bea336d17e813
