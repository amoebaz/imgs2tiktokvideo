from moviepy.editor import ImageSequenceClip, TextClip, CompositeVideoClip, concatenate_videoclips, VideoClip, ImageClip, transfx, vfx
import os
import PIL.Image as Image, PIL.ImageEnhance as ImageEnhance
import random
import numpy as np
import sys
import shutil

os.environ["FFMPEG_BINARY"] = "ffmpeg"

import subprocess

def get_ffmpeg_version():
    result = subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout.split('\n')[0]

print("Versión de ffmpeg:", get_ffmpeg_version())


video_width = 1080
video_height = 1920
video_fps = 60
duration_per_image = 2
duration_of_transition = 0.25
titulo_video = "Battle Beast"
subtitulo_video = "Marenostrum Fuengirola"


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

def zoom_transition(clip1, clip2, duration=duration_of_transition):
    def milambda(t, duration):
#        print("t/Duration: " + str(t) + "/" + str(duration))
        if (t<2*duration):
            return 1.5 - ((2*t-2*duration))
        else:
            return 1
        
    clip2_zoomed = clip2.fx(vfx.resize, lambda t: milambda(t,duration)).set_position("center", "center")
    return CompositeVideoClip([
        clip1,
        clip2_zoomed.set_start(clip1.duration - duration)
    ], use_bgclip=True)

def rotate_transition(clip1, clip2, duration=duration_of_transition, direction='left'):
    def milambda(t, duration, direction):
        if (t<duration and direction == 'left'):
            return 720*(1 - 4*t)/3*duration
        elif (t<duration and direction):
            return 720*(4*t - 1)/3*duration
        else:
            return 0

    clip2_rotated = clip2.add_mask().fx(vfx.rotate, lambda t: milambda(t, duration, direction)).set_position("center", "center").crossfadein(duration)
    return CompositeVideoClip([
        clip1,
        clip2_rotated.set_start(clip1.duration - duration)
    ], use_bgclip=True)

def fade_transition(clip1, clip2, duration=duration_of_transition):
    clip2_faded = clip2.fx(vfx.fadeout, duration)
    return CompositeVideoClip([
        clip1,
        clip2_faded.set_start(clip1.duration - duration)
    ], use_bgclip=True)

def create_vertical_image(img1_path, img2_path, img3_path):
    img1 = Image.open(img1_path)
    img2 = Image.open(img2_path)
    img3 = Image.open(img3_path)
    
    # Calcular las dimensiones finales
    final_width = video_width
    final_height = video_height
    
    # Altura de cada imagen en la composición final
    img_height = final_height // 3
    
    def crop_and_resize(img):
        # Calcular el recorte necesario
        aspect_ratio = final_width / img_height
        if img.width / img.height > aspect_ratio:
            # La imagen es más ancha de lo necesario
            new_width = int(img.height * aspect_ratio)
            left = (img.width - new_width) // 2
            img = img.crop((left, 0, left + new_width, img.height))
        else:
            # La imagen es más alta de lo necesario
            new_height = int(img.width / aspect_ratio)
            top = (img.height - new_height) // 2
            img = img.crop((0, top, img.width, top + new_height))
        
        return img.resize((final_width, img_height), Image.LANCZOS)
    
    img1_resized = crop_and_resize(img1)
    img2_resized = crop_and_resize(img2)
    img3_resized = crop_and_resize(img3)
    
    # Crear la imagen final
    new_img = Image.new('RGB', (final_width, final_height))
    new_img.paste(img1_resized, (0, 0))
    new_img.paste(img2_resized, (0, img_height))
    new_img.paste(img3_resized, (0, 2 * img_height))
    
    return new_img

def create_slideshow(image_folder, output_video, duration_per_image=2, video_size=(video_width, video_height), fps=video_fps):
    # Obtén la lista de imágenes en el directorio especificado
    images = [os.path.join(image_folder, img) for img in os.listdir(image_folder) if img.endswith(('.png', '.jpg', '.jpeg'))]
    images.sort()
    
    processed_images = []
    horizontal_images = []
    
    for img_path in images:
        img = Image.open(img_path)
        if img.width > img.height:  # Imagen horizontal
            horizontal_images.append(img_path)
            if len(horizontal_images) == 3:
                vertical_img = create_vertical_image(*horizontal_images)
                temp_path = f"{image_folder}/temp_vertical_{len(processed_images)}.jpg"
                vertical_img.save(temp_path)
                processed_images.append(temp_path)
                horizontal_images = []
        else:
            # Imagen vertical, procesar normalmente
            processed_images.append(img_path)
    
    # Procesar las imágenes horizontales restantes
    for img_path in horizontal_images:
        processed_images.append(img_path)
    
    # Recortar y redimensionar las imágenes
    for img_path in processed_images:
        im = Image.open(img_path)
        width, height = im.size
        left = (width - video_width)/2
        top = (height - video_height)/2
        right = (width + video_width)/2
        bottom = (height + video_height)/2
        im = im.crop((left, top, right, bottom))
        enhancer = ImageEnhance.Sharpness(im)
        im = enhancer.enhance(2)
        im.save(img_path)

    # Crea clips de video a partir de las imágenes procesadas
    clips = [ImageSequenceClip([img], durations=[duration_per_image]).resize(newsize=video_size) for img in processed_images]
    print("CANTIDAD: " + str(len(clips)))
    
    if len(clips) == 0:
        print("No se encontraron imágenes en el directorio especificado.")
        return

    # Añadir transiciones aleatorias entre clips
    transition_types = ['crossfade', 'slide_left', 'slide_right', 'slide_top', 'slide_bottom', 'zoom', 'rotate_left', 'rotate_right', 'fade']
    final_clips = [clips[0]]
    for i in range(1, len(clips)):
#    for i in range(1, 3):
        transition_type = random.choice(transition_types)
#        transition_type = 'slide_left'
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
        elif transition_type == 'zoom':
            final_clips.append(zoom_transition(final_clips[-1], clips[i]))
        elif transition_type == 'rotate':
            final_clips.append(rotate_transition(final_clips[-1], clips[i]))
        elif transition_type == 'rotate_left':
            final_clips.append(rotate_transition(final_clips[-1], clips[i], duration_of_transition, direction='left'))
        elif transition_type == 'rotate_right':
            final_clips.append(rotate_transition(final_clips[-1], clips[i], duration_of_transition, direction='right'))
        elif transition_type == 'fade':
            final_clips.append(fade_transition(final_clips[-1], clips[i]))
        else:
            print("ERROR!!!")
            exit()

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


def copiar_imagenes(origen, destino='images'):
    # Limpiar la ruta de entrada
    origen = origen.strip().strip('"\'').replace('\\', '/')
    
    if not os.path.exists(origen):
        print(f"El directorio '{origen}' no existe.")
        return

    # Borrar contenido actual de la carpeta destino
    for archivo in os.listdir(destino):
        ruta_archivo = os.path.join(destino, archivo)
        if os.path.isfile(ruta_archivo):
            os.unlink(ruta_archivo)
    
    # Copiar imágenes del origen al destino
    for archivo in os.listdir(origen):
        if archivo.lower().endswith(('.png', '.jpg', '.jpeg')):
            shutil.copy2(os.path.join(origen, archivo), destino)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        directorio_origen = sys.argv[1]
        copiar_imagenes(directorio_origen)
        print(f"Imágenes copiadas de {directorio_origen} a la carpeta 'images'")
    
    create_slideshow('images', 'output_video.mp4')
