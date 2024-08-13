from yt_dlp import YoutubeDL
import os


def download_yt_mp3(url: str, save_folder: str) -> str:
    """
    Скачивает аудио из YouTube в формате MP3 и сохраняет его в указанной папке.

    :param url: URL видео на YouTube.
    :param save_folder: Папка, в которую будет сохранён MP3 файл.
    :return: Путь к сохранённому MP3 файлу.
    """
    print(f"Start processing music from {url}")

    # Убедитесь, что папка для сохранения существует
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    # Опции для YoutubeDL
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'ffmpeg_location': 'ffmpeg.exe',  # Укажите путь к папке с ffmpeg, если не в PATH
        'outtmpl': os.path.join(save_folder, '%(title)s.%(ext)s'),  # Путь для сохранения файлов
    }

    # Получаем информацию о видео
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)

    title = info_dict.get('title', 'untitled')  # Используем 'untitled', если title не найден
    filename = f"{title}.mp3"
    file_path = os.path.join(save_folder, filename)

    # Проверяем, существует ли файл
    if os.path.isfile(file_path):
        print(f"File {file_path} already exists. Skipping download.")
        return file_path

    # Загружаем файл, если его нет
    print(f"File {file_path} does not exist. Downloading now.")
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return file_path
