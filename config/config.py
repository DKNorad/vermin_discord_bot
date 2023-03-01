PREFIX = "!"
VC_CHANNEL_NAME = "GENERAL"


# Music Player
INFO_HISTORY_TITLE = "Songs Played:"
MAX_HISTORY_LENGTH = 20
MAX_TRACKNAME_HISTORY_LENGTH = 20

MAX_SONG_PRELOAD = 5

VC_TIMEOUT = 600  # seconds
VC_TIMEOUT_DEFAULT = True  # default template setting for VC timeout true= yes, timeout false= no timeout
ALLOW_VC_TIMEOUT_EDIT = True  # allow or disallow editing the vc_timeout guild setting


# Songs
SONGINFO_UPLOADER = "Uploader: "
SONGINFO_DURATION = "Duration: "
SONGINFO_SECONDS = "s"
SONGINFO_LIKES = "Likes: "
SONGINFO_DISLIKES = "Dislikes: "
SONGINFO_NOW_PLAYING = "Now Playing"
SONGINFO_QUEUE_ADDED = "Added to queue"
SONGINFO_SONGINFO = "Song info"
SONGINFO_ERROR = "Error: Unsupported site or age restricted content. To enable age restricted content check the documentation/wiki."
SONGINFO_PLAYLIST_QUEUED = "Queued playlist :page_with_curl:"
SONGINFO_UNKNOWN_DURATION = "Unknown"

# General
COOKIE_PATH = "./cookies.txt"
EMBED_COLOR = 0x4dd4d0


# Help
HELP_CONNECT_SHORT = "Connect bot to voice channel"
HELP_CONNECT_LONG = "Connects the bot to the voice channel you are currently in"
HELP_DISCONNECT_SHORT = "Disconnect bot from voice channel"
HELP_DISCONNECT_LONG = "Disconnect the bot from the voice channel and stop audio."

HELP_SETTINGS_SHORT = "View and set bot settings"
HELP_SETTINGS_LONG = f"View and set bot settings in the server. Usage: {PREFIX}settings setting_name value"

HELP_HISTORY_SHORT = "Show history of songs"
HELP_HISTORY_LONG = "Shows the " + str(MAX_TRACKNAME_HISTORY_LENGTH) + " last played songs."
HELP_PAUSE_SHORT = "Pause Music"
HELP_PAUSE_LONG = "Pauses the Music Player. Playback can be continued with the resume command."
HELP_VOL_SHORT = "Change volume %"
HELP_VOL_LONG = "Changes the volume of the Music Player. Argument specifies the % to which the volume should be set."
HELP_PREV_SHORT = "Go back one Song"
HELP_PREV_LONG = "Plays the previous song again."
HELP_RESUME_SHORT = "Resume Music"
HELP_RESUME_LONG = "Resumes the Music Player."
HELP_SKIP_SHORT = "Skip a song"
HELP_SKIP_LONG = "Skips the currently playing song and goes to the next item in the queue."
HELP_SONGINFO_SHORT = "Info about current Song"
HELP_SONGINFO_LONG = "Shows details about the song currently being played and posts a link to the song."
HELP_STOP_SHORT = "Stop Music"
HELP_STOP_LONG = "Stops the Music Player and clears the song queue"
HELP_MOVE_LONG = f"{PREFIX}move [position] [new position]"
HELP_MOVE_SHORT = 'Moves a track in the queue'
HELP_YT_SHORT = "Play a supported link or search on youtube"
HELP_YT_LONG = ("$p [link/video title]")
HELP_PING_SHORT = "Pong"
HELP_PING_LONG = "Test bot response status"
HELP_CLEAR_SHORT = "Clear the queue."
HELP_CLEAR_LONG = "Clears the queue and skips the current song."
HELP_LOOP_SHORT = "Loops the currently playing song, toggle on/off."
HELP_LOOP_LONG = "Loops the currently playing song and locks the queue. Use the command again to disable loop."
HELP_QUEUE_SHORT = "Shows the songs in queue."
HELP_QUEUE_LONG = "Shows the number of songs in queue, up to 10."
HELP_SHUFFLE_SHORT = "Shuffle the queue"
HELP_SHUFFLE_LONG = "Randomly sort the songs in the current queue"
HELP_CHANGECHANNEL_SHORT = "Change the bot channel"
HELP_CHANGECHANNEL_LONG = "Change the bot channel to the VC you are in"

ABSOLUTE_PATH = ''  # do not modify
