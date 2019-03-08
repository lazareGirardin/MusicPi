import vlc
import pafy
import time
import sys
import os
import shutil
from threading import Thread
#from flask_socketio import SocketIO, emit

# ideas:
# add exception catch: write next songs in playlist.txt.
# in the beginning, check if file exists and load songs then erase

class PlaylistLooper(Thread):
    def __init__(self, pi_player):
        Thread.__init__(self)
        self.pi_player = pi_player

    def run(self):
        while (True):
            try:
                state = self.pi_player.get_state()
                if state == vlc.State.Ended or not self.pi_player.get_play_state():
                    song = self.pi_player.get_next_song()
                    if song:
                        self.pi_player.start(song)
                        self.pi_player.set_play_state(True)
                        data = {}
                        data['now'] = self.pi_player.now_playing
                        songs = self.pi_player.get_next_song_list(5)
                        for i in range(5):
                            data[str(i)] = songs[i]
                    else:
                        self.pi_player.is_playing = False
                time.sleep(5)
            except Exception as e:
                print(str(e))


class PiPlayer:
    def __init__(self, history, playlist):
        self.HISTORY = history
        self.PATH = playlist
        self.to_play = []
        self.now_playing = []
        self.is_playing = False

        self.PLAYURL = 0
        self.TITLE = 1
        self.URL = 2

        self.vlc_instance = vlc.Instance()
        self.player = self.vlc_instance.media_player_new()

        self.Media = None

        #self.load_playlist('playlist_test.txt')

    def get_state(self):
        return self.player.get_state()
    def get_play_state(self):
        return self.is_playing
    def set_play_state(self, _bool):
        self.is_playing = _bool

    def get_current_song(self):
        song = None
        if self.is_playing:
            song = self.now_playing[self.TITLE]
        return song

    def load_playlist(self, path):
        self.to_play = []
        with open(path, 'r') as file:
            data = file.read().splitlines()
        self.to_play = [self._get_play_url(s.split(',')[1]) for s in data]

    def get_next_song_list(self, N):
        result=[]
        for i in range(N):
            if len(self.to_play)>i:
                result.append(self.to_play[i][self.TITLE])
            else:
                result.append('')
        return result

    def get_all_songs(self):
        result=[]
        for entry in self.to_play:
            result.append(entry[self.TITLE])
        return result

    def get_next_song(self):
        if len(self.to_play) > 0:
            self.now_playing = self.to_play.pop(0)
            return self.now_playing[self.PLAYURL]
        else:
            return None

    def start(self, url):
        self.Media = self.vlc_instance.media_new(url)
        self.Media.get_mrl()
        self.player.set_media(self.Media)
        self.player.play()

    def _get_play_url(self, url):
        try:
            video=pafy.new(url)
            best=video.getbestaudio()

            return best.url, best.title, url
        except Exception as e:
            print(e)
            return None

    def add_entry(self, url):
        try:
            play_url, title, _url = self._get_play_url(url)
            if play_url is not None:
                self.to_play.append([play_url, title, _url])
                with open(self.HISTORY, 'a') as file:
                    # add play url to load playlist faster r in another file maybe?
                    file.write(title + ',' + url + '\n')
            return True
        except Exception as e:
            return False

    def set_pause(self):
        self.player.pause()
        # leave is_playing True so that the loop does not re-start
    def set_next(self):
        song = self.get_next_song()
        if song:
            self.start(song)
            self.is_playing = True
