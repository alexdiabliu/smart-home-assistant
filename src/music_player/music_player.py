
import os


class MusicPlayer:
    """
    A class to represent a music player that can play songs by artist and title.
    """

    def __init__(self, artist: str, title: str):
        self.artist = artist
        self.title = title

    def play(self) -> None:
        """
        Play the music using the specified artist and title.
        """

        params = {
            'artist': self.artist,
            'title': self.title
        }
        # checks music folder for the song
        print(f"Checking music folder for {self.artist} - {self.title}...")

        for file in os.listdir('../music'):
            print(f"Found file: {file}")
            if (self.artist and self.title) in file:
                print(f"Found {file}, playing now...")
                # Here you would typically call a music player API or library to play the song.
                break
        else:
            print(f"Song {self.artist} - {self.title} not found in music folder.")
            print("Please check the artist and title, or add the song to the music folder.")
        

    def pause(self) -> None:
        """
        Pause the currently playing music.
        """
        print("Pausing music...")

    def stop(self) -> None:
        """
        Stop the currently playing music.
        """
        print("Stopping music...")