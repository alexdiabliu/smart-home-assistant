
import os
import pygame
class MusicPlayer:
    """
    A class to represent a music player that can play songs by artist and title.
    """

    def __init__(self):
        pygame.mixer.init(buffer=512)
        self.is_playing = False

    def play(self, artist: str, title: str) -> None:
        """
        Play the music using the specified artist and title in the background.
        """
        music_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../music"))
        print(f"Checking music folder for {artist} - {title}...")

        for file in os.listdir(music_dir):
            if artist in file.lower() and title in file.lower():
                full_path = os.path.join(music_dir, file)
                print(f"Found {file}, Playing Now...")
                self.is_playing = True
                pygame.mixer.music.load(full_path)
                pygame.mixer.music.play()
                return

        print(f"Song {artist} - {title} not found in music folder.")
        print("Please check the artist and title, or add the song to the music folder.")


    def pause(self) -> None:
        """
        Pause the currently playing music.
        """
        print("Pausing Music...")
        pygame.mixer.music.pause()
        self.is_playing = False
        return


    def resume(self) -> None:
        """
        Resume the previously paused music.
        """
        print("Resuming Music...")
        pygame.mixer.music.unpause()
        self.is_playing = True
        return


    def stop(self) -> None:
        """
        Stop the currently playing music entirely.
        """
        print("Stopping Music...")
        pygame.mixer.music.stop()
        self.is_playing = False
        return


    def change_volume(self, volume = 0.3) -> None:
        print(f"Adjusting to {volume}...")
        pygame.mixer.music.set_volume(volume)
        return