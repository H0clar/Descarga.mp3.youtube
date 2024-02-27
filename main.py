import argparse
import string  # Importar el módulo string
from pytube import YouTube
from moviepy.editor import *
import os
import re


def descargar_y_convertir_a_mp3(urls):
    try:
        # Asegúrate de que la carpeta "/Canciones_Listas/" exista antes de ejecutar el script
        if not os.path.exists('Canciones_Listas'):
            os.makedirs('Canciones_Listas')

        with open(urls, 'r') as file:
            for url in file:
                url = url.strip()  # Elimina cualquier espacio en blanco al principio o al final de la URL
                # Extraer el ID del video de YouTube de la URL
                video_id_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11})', url)
                if video_id_match:
                    video_id = video_id_match.group(1)
                    # Descargar el video de YouTube
                    yt = YouTube('https://www.youtube.com/watch?v=' + video_id)
                    video = yt.streams.filter(only_audio=True).first()

                    # Obtener un nombre de archivo válido basado en el título del video
                    title = yt.title
                    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
                    filename = ''.join(c for c in title if c in valid_chars)
                    filename = filename.replace(' ', '_')  # Reemplazar espacios en blanco con guiones bajos

                    # Especifica la ruta completa para guardar el archivo de audio
                    audio_path = os.path.join('Canciones_Listas', 'temp_audio.mp3')  # Cambiado a .mp3
                    video.download(output_path='Canciones_Listas', filename='temp_audio.mp3')  # Cambiado a .mp3

                    # Convertir el video a MP3
                    clip = AudioFileClip(audio_path)

                    # Verificar si el archivo ya existe y eliminarlo si es necesario
                    if os.path.exists(f'Canciones_Listas/{filename}.mp3'):
                        os.remove(f'Canciones_Listas/{filename}.mp3')

                    clip.write_audiofile(f'Canciones_Listas/{filename}.mp3')  # Utilizar un nombre de archivo válido

                    # Eliminar el archivo temporal
                    clip.close()  # Cerrar el archivo de audio
                    os.remove(audio_path)

                    print(f'Archivo MP3 guardado en /Canciones_Listas/ como {filename}.mp3')
                else:
                    print(f'La URL "{url}" no es una URL válida de YouTube')
    except Exception as e:
        print(f'Error al descargar, convertir o mover el archivo: {e}')


def main():
    print("Leyendo las URLs de las canciones desde el archivo canciones_url.txt...")
    urls_file = 'canciones_url.txt'

    descargar_y_convertir_a_mp3(urls_file)


if __name__ == "__main__":
    main()
