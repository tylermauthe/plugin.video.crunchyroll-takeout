"""
    CrunchyRollTakeout
"""
import sys
import xbmcaddon

#plugin constants
__plugin__ = "CrunchyRollTakeout"
__version__ = "0.6.5"
__settings__ = xbmcaddon.Addon(id='plugin.video.crunchyroll-takeout')

print "[PLUGIN] '%s: version %s' initialized!" % (__plugin__, __version__)

if __name__ == "__main__":
    from resources.lib import crunchy_main as crunchyrolltakeout
    if not sys.argv[2]:
        crunchyrolltakeout.Main()
    else:
        crunchyrolltakeout.Main()

sys.modules.clear()
