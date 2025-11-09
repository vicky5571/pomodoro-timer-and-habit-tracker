import pygame
import os

class MusicPlayer:
    def __init__(self, music_folder="music"):
        pygame.mixer.init()
        self.music_folder = music_folder
        self.playlist = [
            os.path.join(music_folder, file)
            for file in os.listdir(music_folder)
            if file.endswith(".mp3") or file.endswith(".wav")
        ]
        self.current_index = 0

    def play(self):
        if not self.playlist:
            print("🎵 No music files found in folder:", self.music_folder)
            return
        pygame.mixer.music.load(self.playlist[self.current_index])
        pygame.mixer.music.play(-1)  # -1 untuk loop terus-menerus
        print(f"▶️ Now playing: {os.path.basename(self.playlist[self.current_index])}")

    def stop(self):
        pygame.mixer.music.stop()
        print("⏹️ Music stopped.")

    def next_track(self):
        if not self.playlist:
            return
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.play()

    def previous_track(self):
        if not self.playlist:
            return
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.play()
