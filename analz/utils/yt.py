import json
import yt_dlp
from config import Config



URL = 'https://youtu.be/7zDXj0uXo40'
URL2 = 'https://youtu.be/4l_gUwdPrNY'
YT_DIR = Config.YT_DOWNLOADS
YT_INFO_FILE = f"{YT_DIR}/vid_yt.info.json"
YT_AUDIO_FILE = f"{YT_DIR}/yt_audio_dl.m4a"

git_docs = 'https://github.com/yt-dlp/yt-dlp'

def extract_info(url=URL):

    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

        # ?? ydl.sanitize_info makes the info json-serializable
        jinfo =  json.dumps(ydl.sanitize_info(info))
        with open(YT_INFO_FILE, 'w') as f:
            f.write(jinfo)
        return jinfo


def downlowadYT(ifile=YT_INFO_FILE):


    with yt_dlp.YoutubeDL() as ydl:
        error_code = ydl.download_with_info_file(ifile)

    print('Some videos failed to download' if error_code
          else 'All videos successfully downloaded')


URLS = ['https://www.youtube.com/watch?v=BaW_jenozKc']


def extract_audio(urls=URLS):


    ydl_opts = \
        {
        'format': 'm4a/bestaudio/best',
            # ?? See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
            'postprocessors': [{  # Extract audio using ffmpeg
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a',
            }]
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(urls)

    def longer_than_a_minute(info, *, incomplete):
        """Download only videos longer than a minute (or with unknown duration)"""
        duration = info.get('duration')
        if duration and duration < 60:
            return 'The video is too short'

    def filter_video(info):
        furls = ['https://www.youtube.com/watch?v=BaW_jenozKc']
        ydl_opts = { 'match_filter': longer_than_a_minute, }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            error_code = ydl.download(furls)


