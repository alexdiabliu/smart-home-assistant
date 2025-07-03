
from setuptools import setup, find_packages

setup(
    name="voice_assistant",
    version="0.1",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
)

setup(
    name="music_player",
    version="0.1",  
    package_dir={"": "src"},
    packages=find_packages(where="src"),
)
