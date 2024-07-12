import streamlit as st
from yt_dlp import YoutubeDL
import os
import re
import string
import shutil
import urllib.request
import zipfile

def setup_ffmpeg():
    ffmpeg_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    ffmpeg_zip_path = "ffmpeg-release-essentials.zip"
    ffmpeg_extract_path = "ffmpeg"

    # Descargar ffmpeg
    if not os.path.exists(ffmpeg_extract_path):
        urllib.request.urlretrieve(ffmpeg_url, ffmpeg_zip_path)

        # Extraer ffmpeg
        with zipfile.ZipFile(ffmpeg_zip_path, 'r') as zip_ref:
            zip_ref.extractall(ffmpeg_extract_path)

        # Limpiar archivo zip
        os.remove(ffmpeg_zip_path)

    # Encontrar el ejecutable de ffmpeg
    for root, dirs, files in os.walk(ffmpeg_extract_path):
        for file in files:
            if file == "ffmpeg.exe":
                return os.path.join(root, file)

    raise FileNotFoundError("ffmpeg.exe no encontrado")

def descargar_y_convertir_a_mp3(url, ffmpeg_path):
    try:
        if not os.path.exists('Canciones_Listas'):
            os.makedirs('Canciones_Listas')

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'Canciones_Listas/%(title)s.%(ext)s',
            'ffmpeg_location': ffmpeg_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            title = info_dict.get('title', None)
            valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
            filename = ''.join(c for c in title if c in valid_chars)
            filename = filename.replace(' ', '_')

            # Asegúrate de que el archivo .mp3 existe
            original_path = f'Canciones_Listas/{filename}.mp3'
            if os.path.exists(original_path):
                return f'Archivo MP3 guardado en /Canciones_Listas/ como {filename}.mp3'
            else:
                return 'Error al encontrar el archivo descargado para renombrar'
    except Exception as e:
        return f'Error al descargar, convertir o mover el archivo: {e}'

def main():
    st.title('Descargador de Videos de YouTube a MP3')

    urls_input = st.text_area('Inserta las URL de los videos de YouTube (una por línea)')

    if st.button('Agregar URL a archivo y previsualizar'):
        urls = urls_input.split('\n')
        for url in urls:
            url = url.strip()
            if url:
                with open('canciones_url.txt', 'a') as file:
                    file.write(url + '\n')
                st.write(f'URL {url} agregada a canciones_url.txt')

                try:
                    yt = YoutubeDL().extract_info(url, download=False)
                    st.video(url)
                    st.write(f"Título: {yt['title']}")
                    st.write(f"Autor: {yt['uploader']}")
                    st.write(f"Duración: {yt['duration']} segundos")
                except Exception as e:
                    st.write(f'Error al cargar la previsualización de {url}: {e}')

    if st.button('Descargar y Convertir todas las URL a MP3'):
        ffmpeg_path = setup_ffmpeg()
        with open('canciones_url.txt', 'r') as file:
            urls = file.readlines()

        for url in urls:
            url = url.strip()
            if url:
                mensaje = descargar_y_convertir_a_mp3(url, ffmpeg_path)
                st.write(mensaje)

if __name__ == "__main__":
    main()
