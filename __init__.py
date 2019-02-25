import os
import time
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_file_handler, intent_handler
from mycroft.util.log import LOG

__author__ = 'colla69'


def play_player():
    os.system('cmus-remote -C "add -p"')
    os.system("cmus-remote -p")


def pause_player():
    os.system("cmus-remote -u")


def next_player():
    os.system("cmus-remote -n")


def prev_player():
    os.system("cmus-remote -N")


def search_player(text):
    os.system('cmus-remote -C "/' + text+'"')
    os.system('cmus-remote -C "win-activate"')


def refresh_library(path):
    os.system('cmus-remote -C clear')
    LOG.info('reloading music files from: '+path)
    os.system('cmus-remote -C "add '+path+'"')


def show_player():
    os.system('x-terminal-emulator -e "screen -r " ')


def getrunning():
    check = os.popen('cmus-remote -Q | grep "shuffle" |  tail -c 5').readlines()
    if len(check) == 0:
        return False
    else:
        return True


def shufflin():
    check = os.popen('ps ax | grep cmus | grep -v " grep"').readlines()
    LOG.info(check)
    if len(check) == 0:
        return False
    else:
        return True


class Localmusicplayer(MycroftSkill):

    def __init__(self):
        super(Localmusicplayer, self).__init__(name="TemplateSkill")
        # Initialize working variables used within the skill.
        self.music_source = self.settings.get("musicsource", "")
        # init cmus player
        self.activate_player()

    @intent_file_handler('play.music.intent')
    def handle_play_music_ntent(self, message):
        self.activate_player()
        play_player()

    @intent_file_handler('pause.music.intent')
    def handle_pause_music_intent(self, message):
        self.activate_player()
        pause_player()

    @intent_file_handler('reload.library.intent')
    def handle_reload_library_intent(self, message):
        refresh_library(self.music_source)
        self.speak_dialog("refresh.library")

    @intent_file_handler('shuffling.library.intent')
    def handle_shuffling_library_intent(self, message):
        if shufflin():
            self.speak("yes")
        else:
            self.speak("no")

    @intent_file_handler('next.music.intent')
    def handle_next_music_intent(self, message):
        self.activate_player()
        next_player()

    @intent_file_handler('prev.music.intent')
    def handle_prev_music_intent(self, message):
        self.activate_player()
        prev_player()

    @intent_file_handler('show.music.intent')
    def handle_show_music_intent(self, message):
        self.activate_player()
        show_player()

    @intent_handler(IntentBuilder("search.music.intent").require("search.music").require("SongToPlay").build())
    def handle_search_music_intent(self, message):
        songtoplay = message.data.get("SongToPlay")
        self.activate_player()
        search_player(songtoplay)

    def start_player(self):
        os.system("screen -d -m -S cmus cmus &")
        os.system("screen -d -m -S cmus cmus &")
        # config player for usage
        os.system('cmus-remote -C "set softvol_state=70 70"')
        os.system('cmus-remote -C "set continue=true"')
        time.sleep(1)

    def stop_player(self):
        os.system("cmus-remote -C quit")

    def activate_player(self):
        if not getrunning():
            self.start_player()
            refresh_library(self.music_source)

    def converse(self, utterances, lang="en-us"):
        return False

    def stop(self):
        if getrunning():
            self.stop_player()


def create_skill():
    return Localmusicplayer()
