from __future__ import print_function
from pydbus import SessionBus
from gi.repository import GObject, GLib
import subprocess
from time import sleep

loop = GObject.MainLoop()

subprocess.Popen("gnome-music")
sleep(5)
print("Waiting for GNOME Music to start...")

b = SessionBus()
m = b.get("org.mpris.MediaPlayer2.GnomeMusic", "/org/mpris/MediaPlayer2")

m.PropertiesChanged.connect(print)

m.ActivatePlaylist(m.GetPlaylists(0, 5, "Alphabetical", 0)[0][0])

m.Play()
sleep(1)
assert(m.PlaybackStatus == "Playing")

m.Pause()
assert(m.PlaybackStatus == "Paused")

m.Play()
assert(m.PlaybackStatus == "Playing")

t = m.Metadata["xesam:title"]

m.Next()

assert(m.Metadata["xesam:title"] != t)

m.Previous()

assert(m.Metadata["xesam:title"] == t)

oldLoopStatus = m.LoopStatus

m.LoopStatus = "None"
assert(m.LoopStatus == "None")

m.LoopStatus = "Track"
assert(m.LoopStatus == "Track")

m.LoopStatus = oldLoopStatus

GLib.timeout_add_seconds(2, lambda: loop.quit())
loop.run()
