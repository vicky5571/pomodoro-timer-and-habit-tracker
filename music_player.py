import pygame
import os
import sys

class MusicPlayer:
    def __init__(self, music_folder="music"):
        pygame.mixer.init()
        self.music_folder = self.resource_path(music_folder)

        if not os.path.exists(self.music_folder):
            print(f"❌ Folder musik '{self.music_folder}' tidak ditemukan.")
            self.playlist = []
            return

        self.playlist = [
            os.path.join(self.music_folder, file)
            for file in os.listdir(self.music_folder)
            if file.endswith(".mp3") or file.endswith(".wav")
        ]
        self.current_index = 0

    def resource_path(self, relative_path):
        """Dapatkan path absolut, bekerja di .exe dan mode normal."""
        try:
            base_path = sys._MEIPASS  # Temp folder dari PyInstaller
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def play(self):
        if not self.playlist:
            print("🎵 No music files found in folder:", self.music_folder)
            return
        pygame.mixer.music.load(self.playlist[self.current_index])
        pygame.mixer.music.play(-1)
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
