import random
from collections import deque
from config.config import MAX_TRACKNAME_HISTORY_LENGTH, MAX_HISTORY_LENGTH
from modules.music.song import Song


class Playlist:
    """Stores the YouTube links of songs to be played and already played and offers basic operation on the queues"""

    def __init__(self):
        # Stores the links of the songs in queue and the ones already played.
        self.playque = deque()
        self.playhistory = deque()

        # A separate history that remembers the names of the tracks that were played
        self.trackname_history = deque()

        self.loop = False

    def __len__(self):
        return len(self.playque)

    def add_name(self, trackname):
        self.trackname_history.append(trackname)
        if len(self.trackname_history) > MAX_TRACKNAME_HISTORY_LENGTH:
            self.trackname_history.popleft()

    def add(self, track: Song):
        self.playque.append(track)

    def next(self, song_played):
        if self.loop:
            self.playque.appendleft(self.playhistory[-1])

        if len(self.playque) == 0:
            return None

        if song_played != "Dummy":
            if len(self.playhistory) > MAX_HISTORY_LENGTH:
                self.playhistory.popleft()

        return self.playque[0]

    def prev(self, current_song):
        if current_song is None:
            self.playque.appendleft(self.playhistory[-1])
            return self.playque[0]

        ind = self.playhistory.index(current_song)
        self.playque.appendleft(self.playhistory[ind - 1])
        if current_song is not None:
            self.playque.insert(1, current_song)

    def shuffle(self):
        random.shuffle(self.playque)

    def move(self, oldindex: int, newindex: int):
        temp = self.playque[oldindex]
        del self.playque[oldindex]
        self.playque.insert(newindex, temp)

    def empty(self):
        self.playque.clear()
        self.playhistory.clear()
