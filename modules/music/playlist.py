import random
from collections import deque
from config.config import MAX_TRACKNAME_HISTORY_LENGTH, MAX_HISTORY_LENGTH
from modules.music.song import Song


class Playlist:
    """Stores the YouTube links of songs to be played and already played and offers basic operation on the queues"""

    def __init__(self):
        # Stores the links of the songs in queue and the ones already played.
        self.playqueue = deque()
        self.playhistory = deque()

        # A separate history that remembers the names of the tracks that were played
        self.trackname_history = deque()

        self.loop = False

    def __len__(self):
        return len(self.playqueue)

    def add_name(self, trackname):
        self.trackname_history.append(trackname)
        if len(self.trackname_history) > MAX_TRACKNAME_HISTORY_LENGTH:
            self.trackname_history.popleft()

    def add(self, track: Song):
        self.playqueue.append(track)

    def next(self, song_played):
        if self.loop:
            self.playqueue.appendleft(self.playhistory[-1])

        if len(self.playqueue) == 0:
            return None

        if song_played != "Dummy":
            if len(self.playhistory) > MAX_HISTORY_LENGTH:
                self.playhistory.popleft()

        return self.playqueue[0]

    def prev(self, current_song):
        if current_song is None:
            self.playqueue.appendleft(self.playhistory[-1])
            return self.playqueue[0]

        ind = self.playhistory.index(current_song)
        self.playqueue.appendleft(self.playhistory[ind - 1])
        if current_song is not None:
            self.playqueue.insert(1, current_song)

    def shuffle(self):
        random.shuffle(self.playqueue)

    def move(self, oldindex: int, newindex: int):
        temp = self.playqueue[oldindex]
        del self.playqueue[oldindex]
        self.playqueue.insert(newindex, temp)

    def empty(self):
        self.playqueue.clear()
        self.playhistory.clear()
