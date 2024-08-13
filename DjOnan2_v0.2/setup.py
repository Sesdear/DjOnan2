from setuptools import setup
from Cython.Build import cythonize
import os

# Указываем пути к файлам .pyx, включая файлы в папке commands
extensions = [
    "DjOnanMainFile.pyx",
    "run.pyx",
    os.path.join("commands", "__init__.pyx"),
    os.path.join("commands", "music.pyx"),
    os.path.join("commands", "yt_downloader.pyx"),
    os.path.join("commands", "fun.pyx"),
]

setup(
    ext_modules = cythonize(extensions),
)
