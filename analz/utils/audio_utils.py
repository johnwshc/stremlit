# from pydub import AudioSegment
# from pydub.playback import play
import eyed3
from pydantic import BaseModel
from typing import Optional
import pathlib
from pathlib import Path
# import mutagen
from mutagen.flac import FLAC


class ERAudioTag(BaseModel):
    file: str
    artist: str
    album: str
    title: str
    type: Optional[str] = "mp3"


    @classmethod
    def prep_audio_tag(cls, afile, artist, type='mp3'):
        d = {'artist': artist, 'file': afile,}
        p_afile = pathlib.Path(afile).with_suffix('')
        par = p_afile.parent
        d['title'] = p_afile.name
        d['album'] = par.name
        d['type'] = type
        return cls(**d)

    @classmethod
    def test_prep_audio_tag(cls):
        fname = "F:/ia_downloads/greensky/gsbg2024-05-24/16 Ain't No Bread In The Breadbox.mp3"
        er_aidio_tag = cls.prep_audio_tag(fname, 'Greensky')
        return er_aidio_tag

    def read_flac_audio_tags(self) -> ():
        audio = FLAC(self.file)
        title = ""
        artist = ""
        album = ""
        album_artist = ""

        title = audio.get("title", None)
        artist = audio.get("artist", None)
        album = audio.get("album", None)
        album_artist = audio.get("albumartist", None)

        return title, artist, album, album_artist


        # print(audio.tags)  # Access all tags
        # print(audio["title"])  # Access specific tag

        # # Write tags
        # audio["artist"] = "New Artist"
        # audio.save()

    def read_mp3_audio_tags(self, audiofile: eyed3.core.AudioFile) -> ():
        title = ""
        artist = ""
        album = ""
        album_artist = ""

        fartist = audiofile.tag.artist
        if fartist:
            print(f"fartist: {fartist}")
            artist = fartist
        else:
            artist = None

        falbum_artist = audiofile.tag.album_artist

        if falbum_artist:
            print(f"falbum_artist: {falbum_artist}")
            album_artist = falbum_artist
        else:
            album_artist = None


        falbum = audiofile.tag.album
        if falbum:
            print(f"falbum: {falbum}")
            album = falbum

        else:
            album = None

        ftitle = audiofile.tag.title
        if ftitle:
            print(f"ftitle: {ftitle}")
            title = ftitle

        else:
            title =  None

        return title, artist, album, album_artist


    def edit_audio_tags(self) -> bool:

        if self.type == "mp3":
            try:
                # Load the MP3 file
                audiofile = eyed3.load(self.file) #  eyed3.load("path/to/your/mp3/file.mp3")

                ftitle, fartist, falbum, falbum_artist = self.read_mp3_audio_tags(audiofile)
                if fartist:
                    print(f"fartist: {fartist}")
                    self.artist = fartist
                else:
                    if falbum_artist:
                        audiofile.tag.artist = self.artist
                    else:
                        audiofile.tag.artist = self.artist
                if falbum:
                    print(f"falbum: {falbum}")
                    self.album = falbum
                else:
                    audiofile.tag.album = self.album

                if ftitle:
                    print(f"ftitle: {ftitle}")
                    self.title = ftitle
                else:
                    audiofile.tag.title = self.title

                audiofile.tag.save()
                return True
            except Exception as e:
                print(e)
            return False


        elif self.type == "flac":
            try:
                audio = FLAC(self.file)
                ftitle, fartist, falbum, falbum_artist = self.read_flac_audio_tags()
                if fartist:
                    print(f"fartist: {fartist}")
                    self.artist = fartist
                else:
                    if falbum_artist:
                        audio['artist'] = falbum_artist
                    else:
                        audio['artist'] = self.artist
                if falbum:
                    print(f"falbum: {falbum}")
                    self.album = falbum
                else:
                    audio['album'] = self.album

                if ftitle:
                    print(f"ftitle: {ftitle}")
                    self.title = ftitle
                else:
                    audio['title'] = self.title

                audio.save()
                return True



            except Exception as e:
                print(e)
                return False



class IA_Downloads:
    artists = \
        {
            'gsbg':
                [
                    {'dir': 'F:\\ia_downloads\\greensky\\gsbg2024-05-2',
                     'album':'gsbg2024-05-24',
                      'type': 'mp3'
                    },
                    {'dir': "F:\\ia_downloads\\bluegrass_radio\\greensky bluegrass\\gsbg2024-02-09",
                    'album': 'gsbg2024-02-09',
                    'type': 'flac'
                    },
                    {'dir': "F:\\ia_downloads\\bluegrass_radio\\greensky_2023-02-23",
                      'album': 'greensky_2023-02-23',
                      'type': 'mp3'

                    },
                    {
                        'dir': "F:\\ia_downloads\\bluegrass_radio\\gsbg2022-10-09.flac16",
                        'album': 'gsbg2022-10-09.flac16',
                        'type': 'flac'
                    }
                ],
            'billy_strings':

                [
                    {'dir': '"F:\\ia_downloads\\billy strings\\billystrings2020-02-22"',
                    'album': 'billystrings2020-02-22',
                     'type': 'flac'
                    },
                    {'dir': "F:\\ia_downloads\\billy strings\\billystrings2023-12-16",
                    'album': 'billystrings2023-12-16',
                     'type': 'mp3'
                    },
                    {'dir': "F:\\ia_downloads\\billy strings\\billystrings2024-06-20",
                    'album': 'billystrings2024-06-20',
                     'type': 'mp3'
                    },
                ],
            'cadillacsky':
                [
                    {'dir': "F:\\ia_downloads\\bluegrass_radio\\cadillacsky2006-07-14",
                     'album': 'cadillacsky2006-07-14',
                     'type': 'mp3'
                     },
                ],
            'del_mccoury':
                [
                    {'dir': "F:\\ia_downloads\\bluegrass_radio\\del2024-01-18.sdmix\\Del McCoury Band 2024-01-18 mix",
                     'album': 'Del McCoury Band 2024-01-18 mix',
                     'type': 'mp3'
                     },
                ],
            'horseshoes_and_handgrenades':
            [],
            'handpicked bluegrass':
            [],
            'Infamous Stringdusters':
            [],
            'Jim Lauderdale and Della May':
            [],
            'kitchen dwellers':
            [],
            'Harold Shotgun Jackson':
            [],
            'Max Creek':
            [],
            'sam bush':
            [],
            'SCBB':
            [],
            'she-might-love-me-onece-again':
            [],
            'southpaw blues band':
            [],
            'ston3henge bluegrass':
            [],
            'theStrayBirds2016-07-15':
            [],
            'The WolfTones':
            [],
            'Uncle Earl':
            [],
            'ymsb':
            [],
            'jupiter coyote':
            [],
            'lil_smokies':
            [],

        }

    @classmethod
    def rename_file(cls, old_file: Path) -> Path or None:
        p_old_file = old_file
        if p_old_file.exists():

            fname = p_old_file.name
            pre = f"{fname.split(' ')[0]}__"
            all = f"{pre}hhg.mp3"
            new_file = p_old_file.with_name(all)
            p_old_file.rename(new_file)
            print(f"File renamed from {old_file} to {new_file}")
            return new_file
        else:
            print(f"file {p_old_file.as_posix()} does not exist")
            return None






    @classmethod
    def hhg_fix(cls):

        tags: list = []

        hhg_dir1 = "F:\\ia_downloads\\bluegrass_radio\\hhg\\hhg2019-03-28"
        hhg_dir2 = "F:\\ia_downloads\\bluegrass_radio\\hhg\\hhg2024-06-29"
        artist = "Horseshoes_and_HandGrenades"
        p_dir1 = pathlib.Path(hhg_dir1)
        p_dir2 = pathlib.Path(hhg_dir2)
        for f in list(p_dir1.glob('*.mp3')):
            if 'hhg.mp3' in f.name:
                continue
            print(f"file: {f}")
            new_file = cls.rename_file(f)
            if new_file:
                er_audio_tag = ERAudioTag.prep_audio_tag(str(new_file), artist)
                tags.append(er_audio_tag)
                # er_audio_tag.edit_audio_tags()
        return tags

    @classmethod
    def convert_mp4_2_mp3(cls, vin, aout):
        from moviepy import VideoFileClip

        # Load the video
        video = VideoFileClip(vin)

        # Extract audio
        audio = video.audio

        # Save the audio as a temporary file
        audio.write_audiofile(aout)
        print(f"saved mp4 file: {vin} as mp3: {aout}")

        # Convert the temporary MP3 file to WAV
        # AudioSegment.from_mp3("temp_audio.mp3").export("final_audio.wav", format="wav")

    def __init__(self, s_dir: str, artist: str = "Greensky"):
        self.s_dir = s_dir
        self.p_dir = pathlib.Path(s_dir)
        self.album = self.p_dir.name
        self.mp3s = [str(f.as_posix()) for f in list(self.p_dir.glob('*.mp3'))]
        self.er_audio_tags = [ERAudioTag.prep_audio_tag(str(f), artist) for f in self.mp3s]

    @classmethod
    def test_ia_downloads(cls):
        s_dir = "F:/ia_downloads/greensky/gsbg2024-05-24"
        ia_downloads = cls(s_dir, artist='Greensky')
        return ia_downloads

    def edit_audio_tags(self):
        res = []
        for er_audio_tag in self.er_audio_tags:
            res.append(er_audio_tag.edit_audio_tags())
        return res


