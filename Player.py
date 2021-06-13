import Model
from pygame import mixer
from tkinter import filedialog
import os
from mutagen.mp3 import MP3

class Player:
    def __init__(self):
        mixer.init()
        self.my_model = Model.Model()

    def get_db_status(self):
        return self.my_model.get_db_status()

    def get_song_count(self):
        return self.my_model.get_song_count()

    def close_player(self):
        mixer.music.stop()
        self.my_model.close_db_connection()

    def set_volume(self, volume_level):
        mixer.music.set_volume(volume_level)   # accepts only float values ranging from 0.0 to 1.0

    def add_song(self):
        song_path = filedialog.askopenfilenames(title="Select a song", initialdir="C:/", filetypes=[("mp3 files","*.mp3")])
        if song_path == "":
            return
        song_name_list = []
        for single_song_path in song_path:
            song_name = os.path.basename(single_song_path)
            if song_name in self.my_model.song_dict:
                song_name = "song is already present"
            else:
                self.my_model.add_song(song_name, single_song_path)
            song_name_list.append(song_name)
        return song_name_list

    def remove_song(self, sname):
        self.my_model.remove_song(sname)

    def get_song_length(self, sname):
        self.spath = self.my_model.get_song_path(sname)
        self.audio_tag = MP3(self.spath)
        song_length = self.audio_tag.info.length
        return song_length

    def play_song(self):
        mixer.quit()
        mixer.init(frequency=self.audio_tag.info.sample_rate)
        mixer.music.load(self.spath)
        mixer.music.play()

    def stop_song(self):
        mixer.music.stop()

    def pause_song(self):
        mixer.music.pause()

    def unpause_song(self):
        mixer.music.unpause()

    def set_song_pos(self, pos):
        #pos = mixer.music.get_pos()
        #print("pos in sec",pos/1000)
        mixer.music.set_pos(pos)

    def add_song_to_favourites(self, sname):
        spath = self.my_model.get_song_path(sname)
        result = self.my_model.add_song_to_favourites(sname, spath)
        return result

    def load_songs_from_favourites(self):
        result = self.my_model.load_songs_from_favourites()
        return result, self.my_model.song_dict

    def remove_song_from_favourites(self, sname):
        result = self.my_model.remove_song_from_favourites(sname)
        return result

