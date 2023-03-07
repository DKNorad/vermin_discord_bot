import asyncio
import concurrent.futures
import yt_dlp
import discord
from discord.ext import commands
from config import config
from modules.music import linkutils, utils
from modules.music.playlist import Playlist
from modules.music.song import Song


class MusicCog(commands.Cog, name="Music Player"):
    """
    Controls the playback of audio and the sequential playing of the songs.
    Attributes:
        bot: The instance of the bot that will be playing the music.
        playlist: A Playlist object that stores the history and queue of songs.
        current_song: A Song object that stores details of the current song.
    """
    COG_EMOJI = "🎧"

    def __init__(self, bot):
        self.bot = bot
        self.playlist = Playlist()

        self.is_playing = False
        self.is_paused = False
        self.current_song = None

        self.volume = 100
        self.timer = utils.Timer(self.timeout_handler)
        self.vc = None

        self.YT_DLP = {'title': True, "cookiefile": config.COOKIE_PATH}
        self.YT_DLP_BEST = {'format': 'bestaudio', 'title': True, "cookiefile": config.COOKIE_PATH}

    def track_history(self):
        history_string = config.INFO_HISTORY_TITLE
        for trackname in self.playlist.trackname_history:
            history_string += "\n" + trackname
        return history_string

    def next_song(self):
        """Invoked after a song is finished. Plays the next song if there is one."""

        next_song = self.playlist.next(self.current_song)

        self.current_song = None
        if next_song is None:
            return

        coro = self.play_song(next_song)
        self.bot.loop.create_task(coro)

    async def play_song(self, song):
        """Plays a song object"""
        track_url = song.info.webpage_url
        try:
            downloader = yt_dlp.YoutubeDL(self.YT_DLP)
            r = downloader.extract_info(track_url, download=False)
        except:
            downloader = yt_dlp.YoutubeDL(self.YT_DLP)
            r = downloader.extract_info(track_url, download=False)

        song.base_url = r.get('url')
        song.info.uploader = r.get('uploader')
        song.info.title = r.get('title')
        song.info.duration = r.get('duration')
        song.info.webpage_url = r.get('webpage_url')
        song.info.thumbnail = r.get('thumbnails')[0]['url']

        self.playlist.add_name(song.info.title)
        self.current_song = song

        self.playlist.playhistory.append(self.current_song)

        self.vc.voice_client.play(discord.FFmpegPCMAudio(
            song.base_url, before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'),
            after=lambda e: self.next_song())

        self.vc.voice_client.source = discord.PCMVolumeTransformer(self.vc.voice_client.source)
        self.vc.voice_client.source.volume = float(self.volume) / 100.0

        self.playlist.playque.popleft()

        for song in list(self.playlist.playque)[:config.MAX_SONG_PRELOAD]:
            asyncio.ensure_future(self.preload(song))

    async def process_song(self, track_url):
        """Adds the track to the playlist instance and plays it, if it is the first song"""

        host = linkutils.identify_url(track_url)
        playlist_type = linkutils.identify_playlist(track_url)

        if playlist_type != linkutils.PlaylistTypes.Unknown:
            await self.process_playlist(playlist_type, track_url)

            if self.current_song is None:
                await self.play_song(self.playlist.playque[0])
                print("Playing {}".format(track_url))

            song = Song(linkutils.Origins.Playlist, linkutils.Sites.Unknown)
            return song

        if host == linkutils.Sites.Unknown:
            if linkutils.get_url(track_url) is not None:
                return None

            track = self.search_youtube(track_url)

        if host == linkutils.Sites.YouTube:
            track = track_url.split("&list=")[0]

        try:
            downloader = yt_dlp.YoutubeDL(self.YT_DLP)
            try:
                r = downloader.extract_info(track_url, download=False)
            except Exception as e:
                if "ERROR: Sign in to confirm your age" in str(e):
                    return None
        except:
            downloader = yt_dlp.YoutubeDL(self.YT_DLP)
            r = downloader.extract_info(track_url, download=False)

        if r.get('thumbnails') is not None:
            thumbnail = r.get('thumbnails')[len(r.get('thumbnails')) - 1]['url']
        else:
            thumbnail = None

        song = Song(linkutils.Origins.Default, host, base_url=r.get('url'),
                    uploader=r.get('uploader'), title=r.get('title'), duration=r.get('duration'),
                    webpage_url=r.get('webpage_url'), thumbnail=thumbnail)

        self.playlist.add(song)
        if self.current_song is None:
            print(f"Playing {track}")
            await self.play_song(song)

        return song

    async def process_playlist(self, playlist_type, url):
        if playlist_type == linkutils.PlaylistTypes.YouTube_Playlist:
            if "playlist?list=" in url:
                listid = url.split('=')[1]
            else:
                video = url.split('&')[0]
                await self.process_song(video)
                return

            with yt_dlp.YoutubeDL(self.YT_DLP_BEST) as ydl:
                r = ydl.extract_info(url, download=False)

                for entry in r['entries']:
                    link = f"https://www.youtube.com/watch?v={entry['id']}"
                    song = Song(linkutils.Origins.Playlist, linkutils.Sites.YouTube, webpage_url=link)
                    self.playlist.add(song)

        for song in list(self.playlist.playque)[:config.MAX_SONG_PRELOAD]:
            asyncio.ensure_future(self.preload(song))

    async def preload(self, song):
        if song.info.title is not None:
            return

        def down(song):
            if song.info.webpage_url is None:
                return None

            downloader = yt_dlp.YoutubeDL(self.YT_DLP_BEST)
            r = downloader.extract_info(song.info.webpage_url, download=False)
            song.base_url = r.get('url')
            song.info.uploader = r.get('uploader')
            song.info.title = r.get('title')
            song.info.duration = r.get('duration')
            song.info.webpage_url = r.get('webpage_url')
            song.info.thumbnail = r.get('thumbnails')[0]['url']

        loop = asyncio.get_event_loop()
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=config.MAX_SONG_PRELOAD)
        await asyncio.wait(fs={loop.run_in_executor(executor, down, song)}, return_when=asyncio.ALL_COMPLETED)

    def search_youtube(self, title):
        """Searches YouTube for the video title and returns the first results video link"""

        # if title is already a link
        if linkutils.get_url(title) is not None:
            return title

        with yt_dlp.YoutubeDL(self.YT_DLP_BEST) as ydl:
            r = ydl.extract_info(title, download=False)

        if r is None:
            return None

        videocode = r['entries'][0]['id']

        return f"https://www.youtube.com/watch?v={videocode}"

    async def stop_player(self):
        """Stops the player and removes all songs from the queue"""
        if not self.vc.voice_client or (not self.vc.voice_client.is_paused() and not self.vc.voice_client.is_playing()):
            return

        self.playlist.loop = False
        self.playlist.next(self.current_song)
        self.clear_queue()
        self.vc.voice_client.stop()

    async def prev_song(self):
        """Loads the last song from the history into the queue and starts it"""

        self.timer.cancel()

        if len(self.playlist.playhistory) == 0:
            return

        prev_song = self.playlist.prev(self.current_song)

        if not self.vc.voice_client.is_playing() and not self.vc.voice_client.is_paused():

            if prev_song == "Dummy":
                self.playlist.next(self.current_song)
                return None
            await self.play_song(prev_song)
        else:
            self.vc.voice_client.stop()

    async def timeout_handler(self):
        if len(self.vc.voice_client.channel.voice_states) == 1:
            await self.udisconnect()
            return

        sett = utils.guild_to_settings[self.vc]

        if not sett.get('vc_timeout'):
            self.timer = utils.Timer(self.timeout_handler)  # restart timer
            return

        if self.vc.voice_client.is_playing():
            self.timer = utils.Timer(self.timeout_handler)  # restart timer
            return

        self.timer = utils.Timer(self.timeout_handler)
        await self.udisconnect()

    async def uconnect(self, ctx):
        self.vc = discord.utils.get(ctx.guild.voice_channels, name=config.VC_CHANNEL_NAME, bitrate=64000)
        try:
            await self.vc.connect(reconnect=True, timeout=None)
        except Exception as e:
            print(e)

    async def udisconnect(self):
        await self.stop_player()
        await self.vc.voice_client.disconnect(force=True)

    def clear_queue(self):
        self.playlist.playque.clear()


async def setup(bot: commands.Bot):
    await bot.add_cog(MusicCog(bot))
