__author__ = 'nfx'

import os
import fnmatch

from mutagen.id3 import ID3, APIC
from mutagen.mp3 import MP3

def get_all_mp3_files(folder):
    for root, dirnames, filenames in os.walk(folder):
        for filename in fnmatch.filter(filenames, '*.mp3'):
            full_path = os.path.join(root, filename)
            audio = MP3(full_path)
            yield full_path, audio

def get_all_files_without_cover(mp3_files):
    for full_path in mp3_files:
        audio = MP3(full_path)
        if 'APIC:' not in audio.tags:
#            print audio.tags.pprint()
            yield full_path, audio

itunes = '/Users/nfx/Music/iTunes'
#itunes = '/Users/nfx/Music/iTunes/iTunes Media/Music/Abnormyndeffect/Betwin' # has image
#itunes = '/Users/nfx/Music/iTunes/iTunes Media/Music/Behemoth'

def get_info_for_duplicate_songs():
    prev_song = None
    for file, audio in get_all_mp3_files(itunes):
        try:
            song_name = '{} - {} - {}'.format(audio['TPE1'], audio['TALB'], audio['TIT2']).lower()
            #    print "DUP: ", song_name
            if prev_song == song_name:
                yield audio['TPE1'], audio['TALB'], audio['TIT2']
            else:
                prev_song = song_name
        except KeyError, e:
            pass
            #print audio.pprint()

prev_album = (None, None)
for artist, album, so in get_info_for_duplicate_songs():
    if prev_album != (artist, album):
        prev_album = (artist, album)
        print artist, "\t", album