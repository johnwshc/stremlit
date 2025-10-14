import datetime
import os.path
from pathlib import Path
import requests
from requests.auth import HTTPBasicAuth
import json
from config import Config
from pprint import pprint


#   curl url:   >curl https://api.podbean.com/v1/files/uploadAuthorize
#       -G -d 'access_token='e9768f8a7302d94bac8083efcad68b938aab6a4f'
#       -d 'filename=e:/recorded shows/fanny/fanny.3.13.23.mp3'
#       -d 'filesize=83075273'
#       -d 'content_type=audio/mpeg'


class Podbean:
    client_id = '68f96298e13e6c3e5ba24'
    client_secret = 'd205a18c78c93abedc142'
    pb_auth_url = 'https://api.podbean.com/v1/oauth/token'
    pb_episodes_url = f"https://api.podbean.com/v1/episodes"
    test_publish_props = {

        'title': f"Women's History Month, part II",
        'content': 'Enlighten Radio Storytelling for 3.13.23',
        # 'media_key': "e:\\recorded shows\\fanny\\fanny3.13.23.mp3",
        # 'logo_key': "e:\\recorded shows\\wnl\\shows\\unity.jpg",
        'season_number': 10,
        'episode_number': 1,
        'content_explicit': 'clean',
        'filename': "e:/recorded_shows/fanny/fanny.3.13.23.mp3",
    }

    embedded_player = """
    <iframe 
        title="Enlighten Radio: The Storytelling Hour: January 23: Reunions- Memorable Persons and Food Experiences" 
        allowtransparency="true" 
        height="300" 
        width="100%" 
        style="border: none; min-width: min(100%, 430px);" 
        scrolling="no" 
        data-name="pb-iframe-player" 
        src="https://www.podbean.com/player-v2/?from=embed&i=s3btx-136ef8a-pb&square=1&share=1&download=1&fonts=Arial&skin=8bbb4e&font-color=&rtl=0&logo_link=&btn-skin=3267a3&size=300" 
        allowfullscreen="">
    </iframe>"""

    sample_eps_response = {
        'id': 'S3BTX136EF8A',
        'podcast_id': 'DaMzrilOukR',
        'title': 'Enlighten Radio: The Storytelling Hour: January 23: Reunions- Memorable Persons and Food Experiences',
        'content': '',
        'logo': 'https://deow9bq0xqvbj.cloudfront.net/ep-logo/pbblog350764/TSHlogo.jpg',
        'media_url': 'https://mcdn.podbean.com/mf/web/besd8r/fanny123237dn7y.mp3',
        'player_url': 'https://www.podbean.com/player-v2/?share=1&download=1&rtl=0&fonts=Arial&skin=8bbb4e&btn-skin=3267a3&multiple_size=315&square_size=300&order=episodic&filter=all&limit=10&season=all&tag=all&i=s3btx-136ef8a-pb',
        'permalink_url': 'https://democracyroad.podbean.com/e/enlighten-radio-the-storytelling-hour-january-23-reunions-memorable-persons-and-food-experiences/',
        'publish_time': 1674498617,
        'status': 'publish',
        'type': 'public',
        'duration': 3584,
        'season_number': 0,
        'episode_number': 494,
        'apple_episode_type': 'full',
        'transcripts_url': None,
        'object': 'Episode'}

    @staticmethod
    def PB_getFileUploadAuth(access_token, fn):

        up_file = fn
        url = 'https://api.podbean.com/v1/files/uploadAuthorize'
        data = {'access_token': access_token,
                'filename': up_file,
                'filesize': os.path.getsize(up_file),
                'content_type': 'audio/mpeg'
                }
        r = requests.get(url, params=data)

        return r.json()

        #   curl url:   >curl https://api.podbean.com/v1/files/uploadAuthorize
        #       -G
        #       -d 'access_token='e9768f8a7302d94bac8083efcad68b938aab6a4f'
        #       -d 'filename=e:/recorded shows/fanny/fanny.3.13.23.mp3'
        #       -d 'filesize=83075273'
        #       -d 'content_type=audio/mpeg'

    #     curl cmd

    @staticmethod
    def get_podcast_by_title(title='The Poetry Show -- A Celebration of Jane Hirschfield', max=7):
        matches = []
        pb = Podbean()
        epss, msg = pb.getEpisodes(max=max)
        eps = epss['episodes']
        for e in eps:
            id = e['id']
            etitle = e['title']
            if title == etitle:
                matches.append((id, title, e))
                break
        if len(matches) > 0:
            return matches[0]
        else:
            return None

    # ##############  Instance Methods    ################

    def __init__(self):
        self.basic = HTTPBasicAuth(Podbean.client_id, Podbean.client_secret)
        self.payload = {'grant_type': 'client_credentials'}

    def getToken(self):
        r = requests.post(Podbean.pb_auth_url, auth=self.basic, data=self.payload)
        d = json.loads(r.text)
        access_token = d.get('access_token', None)
        return access_token

    def getEpisodes(self, max: int = 10):
        t = self.getToken()
        if t:
            payload = {'access_token': t, 'offset': 0, 'limit': max}
            r = requests.get(Podbean.pb_episodes_url, params=payload)
            d = json.loads(r.text)
            return d, "success"
        else:
            return None, "fail"
        # curl
        # url = https: // api.podbean.com / v1 / episodes \
        #           - G - d
        # 'access_token={access_token}' - d
        # 'offset=0' - d
        # 'limit=10'

    def getPodcast_by_id(self, id=sample_eps_response['id']):
        url = f"{Podbean.pb_episodes_url}/{id}"
        payload = {'access_token': self.getToken()}
        r = requests.get(url, params=payload)
        return r

    # def get_pub_auth(self, fn, tok):
    #     get_auth_url = 'https://api.podbean.com/v1/files/uploadAuthorize'
    #
    #     auth_dic = {
    #         'access_token': tok,
    #         'filename': fn,
    #         'filesize': os.path.getsize(fn),
    #         'content_type': 'audio/mpeg',
    #     }
    #     pprint(auth_dic)
    #     res = requests.get(url=get_auth_url, params=auth_dic).json()
    #     res['fn'] = auth_dic['filename']
    #     return res

    @staticmethod
    def upload_audio_file(auth_props):

        #  ########################## Curl publish cmd string ############################

        #
        # Request Put example:
        # headers = {'Content-type': 'image/jpeg', 'Slug': fileName}
        # r = requests.put(ps_url, data=open(path, 'rb'), headers=headers, auth=('username', 'pass'))
        #
        #  ################################################################################
        # sample_upload_auth_props = {
        #     'presigned_url': str,  # url
        #     'expire_at': int,   # The lifetime of presigned url, in seconds.
        #     'file_key':  str,  # Use this to create / update episode
        #     'filename': str
        # }
        headers = {'Content-Type': 'audio/mpeg'}
        up_file = f"{auth_props['filename']}"

        print(f"uploading audio file to podbean: {up_file}")
        r = requests.put(url=auth_props['presigned_url'],
                         data=open(up_file, 'rb'),
                         headers=headers)
        return r

    # def publishEpisode(self, props:dict, adata):
    #
    #
    #     # sample_pub_auth = {
    #     #     'presigned_url': 'https://s3.amazonaws.com/a1.podbean.com/tmp6/350764/wnl_3_14_23.mp3?X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAYBAB55VCLOBZX454%2F20230325%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20230325T130203Z&X-Amz-SignedHeaders=host&X-Amz-Expires=600&X-Amz-Signature=dfb8b836d24b47aa6e9d6dba1735fec4fadb3db05cf2d1bce8dd264c9a809e79',
    #     #     'expire_at': 600,
    #     #     'file_key': 'tmp6/350764/wnl_3_14_23.mp3'}
    #
    #
    #     token = self.getToken()
    #     # res = self.get_pub_auth(props['filename'], token)
    #     # adata =  res.json()
    #     self.presigned_url = adata['presigned_url']
    #     expire_at = adata['expire_at']
    #     media_key = adata['file_key']
    #     pub_url = f"https://api.podbean.com/v1/episodes"
    #
    #     pdata = {
    #         'access_token': token,
    #         'title': props['title'],
    #         'content': props['content'],
    #         'status': 'draft',
    #         'type': 'public',
    #         'media_key': media_key,
    #         # 'logo_key': props['logo_key'],
    #         'apple_episode_type': 'full',
    #         # 'publish_timestamp': str(datetime.datetime.now()),
    #         'content_explicit': props['content_explicit']
    #     }
    #     res = requests.post(url=pub_url, data=pdata)
    #     return res.json()


class PBPoetry(Podbean):
    poetry_show_default_hosts = 'Janet Harrison and John Case'
    default_poetry_template = "pb_poetry_upload.html"
    default_broadcast = f"Broadcasts LIVE: Wednesdays, 10 AM Eastern Time."
    default_audio_dir = f"f:/recorded_shows/wnl/shows"

    @staticmethod
    def test():
        props = {}
        fn = f"poetry_09202023_wildflower_in_crannie.mp3"

        props['filename'] = fn
        props['guests'] = []
        props['title'] = "The Poetry Show: Infinity in Your Hand"
        props['hosts'] = "Janet Harrison and John Case"
        props['poem'] = "poem_crannie.txt"
        props['poem_title'] = "Flower in a Crannied Wall"
        props['poet'] = "Alfred, Lord of Tennyson"
        props['hosts'] = PBPoetry.poetry_show_default_hosts
        props['broadcast'] = PBPoetry.default_broadcast
        props['rec_date'] = "September 20, 2023"
        props['image_url'] = "https://images.fineartamerica.com/images/artworkimages/mediumlarge/2/flower-in-the-crannied-wall-tennyson-harold-burdekin.jpg"
        props['headline'] = """If You Understood All in All <br >of 
        the flower in a wall crannie, then you would also get <br />the relationship 
        of 'God' to 'man'."""
        props['description'] = "I think that i shall never see, a thing as lovely as a tree"
        return props

    def __init__(self, props):
        super().__init__()
        from app import ju
        self.ju = ju
        self.fn = os.path.join(PBPoetry.default_audio_dir,props.get("filename", "NONE"))
        self.pth_fn = Path(self.fn)
        # self.fn = self.pth_fn.name
        self.dir = self.pth_fn.parents[0].as_posix()
        self.guests = props.get('guests', None)
        self.title = props['title']
        self.hosts = props.get('hosts', PBPoetry.poetry_show_default_hosts)
        plines = []
        poemfile = f"d:/python_apps/flaskER/show_resources/poetry/{props['poem']}"
        with open(poemfile) as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if line:
                    plines.append(line)

            self.poem = plines
        self.poem_title = props.get('poem_title', "Not Available")
        self.poet = props.get('poet', "Not Available")
        self.broadcast = props.get('broadcast', None)
        self.template = props.get('template', PBPoetry.default_poetry_template)
        self.pub_url = f"https://api.podbean.com/v1/episodes"
        self.access_token = self.getToken()

        self.headline = props['headline']
        self.rec_date = props.get('rec_date', datetime.datetime.now().strftime("%d/%m/%Y"))
        self.image_url = props.get('image_url', None)
        self.img_alt = self.poem_title if self.poem_title else None
        self.description = props.get('description', None)
        self.content = self.ju.getPoetryShowPostTemplate(self).strip('\n')
        self.auth_resp = None

    def get_auth_resp(self):
        return Podbean.PB_getFileUploadAuth(self.access_token, self.fn)

    def upload_Poetry_audio(self, fn):
        self.auth_resp = Podbean.PB_getFileUploadAuth(self.access_token, fn)
        self.auth_resp['filename'] = fn
        res = self.upload_audio_file(self.auth_resp)
        return res

    def publish_episode(self, pdata=None):
        self.pdata = pdata
        if not self.pdata:
            self.pdata = {
                'access_token': self.access_token,
                'title': self.title,
                'content': self.content,
                'status': 'draft',
                'type': 'public',
                'media_key': self.auth_resp['file_key'],
            }
        res = requests.post(url=self.pub_url, data=self.pdata)

        return res

    @staticmethod
    def test_poetry():
        props = PBPoetry.test()
        pbp = PBPoetry(props)
        upfile_res = pbp.upload_Poetry_audio(pbp.fn)
        return pbp, upfile_res


class PBLabor(Podbean):
    labor_default_hosts = 'John Case, Scott Marshall, JB Christensen'
    default_labor_template = "pb_labor_upload.html"
    default_broadcast = f"Broadcasts LIVE: Tuesdays, 10 AM Eastern Time."
    default_audio_dir = f"{Config.WNL_DIR}"

    @staticmethod
    def test():
        props = {}
        fn = f"labor_09262023.mp3"

        props['filename'] = fn
        props['guests'] = []
        props['title'] = "Stand UP For the UAW"
        props['description'] = """Find a picket line to help. 
        Ask your neighbor too. John, Scott and JB review the latest UAW updates."""

        props['hosts'] = PBLabor.labor_default_hosts
        props['broadcast'] = PBLabor.default_broadcast
        props['rec_date'] = "September 26, 2023"
        props['image_url'] = "https://uaw.org/wp-content/uploads/2023/09/stand-up-header-image-tp-v3.png"
        props['headline'] = """If The Auto Workers Don't Win, neither You Nor I will Either.<br /> 
        If so-called progress leaves working families behind, then it will not be progress."""
        return props

    def __init__(self, props):
        super().__init__()
        from app import ju
        self.ju = ju
        self.fn = None
        try:
            self.fn = Path(os.path.join(PBLabor.default_audio_dir, props.get("filename", None))).as_posix()
            if not self.fn or not os.path.exists(self.fn):
                raise Exception("No Labor Show without valid file name")
        except Exception as inst:
            print(inst)
            raise inst


        self.guests = props.get('guests', None)
        self.title = props['title']
        self.hosts = props.get('hosts', PBLabor.labor_default_hosts)
        self.broadcast = props.get('broadcast', None)
        self.template = props.get('template', PBLabor.default_labor_template)
        self.pub_url = f"https://api.podbean.com/v1/episodes"
        self.access_token = self.getToken()
        self.headline = props['headline']
        self.rec_date = props.get('rec_date', datetime.datetime.now().strftime("%d/%m/%Y"))
        self.image_url = props.get('image_url', None)
        self.img_alt = self.title
        self.description = props.get('description', None)

        self.content = self.ju.getLaborShowPostTemplate(self).strip('\n')
        self.auth_resp = None

    def get_auth_resp(self):
        return Podbean.PB_getFileUploadAuth(self.access_token, self.fn)

    def upload_Labor_audio(self, fn):
        self.auth_resp = Podbean.PB_getFileUploadAuth(self.access_token, fn)
        self.auth_resp['filename'] = fn
        res = self.upload_audio_file(self.auth_resp)
        return res

    def publish_episode(self, pdata=None):
        self.pdata = pdata
        if not self.pdata:
            self.pdata = {
                'access_token': self.access_token,
                'title': self.title,
                'content': self.content,
                'status': 'draft',
                'type': 'public',
                'media_key': self.auth_resp['file_key'],
            }
        res = requests.post(url=self.pub_url, data=self.pdata)

        return res

    @staticmethod
    def test_labor():
        props = PBLabor.test()
        pbl = PBLabor(props)
        return pbl


class PBRecovery(Podbean):
    default_recovery_hosts = 'James Boyd, John Case'
    default_recovery_template = "pb_recovery_upload.html"
    default_broadcast = f"Broadcasts LIVE: Thursdays, 5:00 PM Eastern Time."
    default_recovery_audio_dir = Config.WNL_DIR

    @staticmethod
    def test():
        props = {}
        # rec_dir = f"E:/recorded_shows/wnl/shows"
        tst_fn = "recovery_09212023_eliz_from_elevate.mp3"

        props['filename'] = tst_fn
        props['guests'] = ["Special Guest: Elizabeth McGowan"]
        props['title'] = "The Recovery Cafe"
        props['description'] = """The Story of Elevate"""

        props['hosts'] = PBRecovery.default_recovery_hosts
        props['broadcast'] = PBRecovery.default_broadcast
        props['rec_date'] = "September 21, 2023"
        props['image_url'] = "https://pbs.twimg.com/profile_images/2170941511/recovery_cafe_logo_square_400x400.jpg"
        props['headline'] = """Walking the Walk."""
        return props

    def __init__(self, props):
        super().__init__()
        from app import ju
        self.ju = ju
        self.fn = None
        try:
            self.fn = os.path.join(Config.WNL_DIR, props.get("filename", None))
            if not self.fn or not os.path.exists(self.fn):
                raise Exception("No Recovery Show without valid file name")
        except Exception as inst:
            print(inst)
            raise inst
        self.pth_fn = Path(self.fn)
        # self.fn = self.pth_fn.name
        self.dir = self.pth_fn.parents[0].as_posix()
        self.guests = props.get('guests', None)
        self.title = props['title']
        self.hosts = props.get('hosts', PBRecovery.default_recovery_hosts)
        self.broadcast = props.get('broadcast', None)
        self.template = props.get('template', PBRecovery.default_recovery_template)
        self.pub_url = f"https://api.podbean.com/v1/episodes"
        self.access_token = self.getToken()
        self.headline = props['headline']
        self.rec_date = props.get('rec_date', datetime.datetime.now().strftime("%d/%m/%Y"))
        self.image_url = props.get('image_url', None)
        self.img_alt = self.title
        self.description = props.get('description', None)

        self.content = self.ju.getRecoveryShowPostTemplate(self).strip('\n')
        self.auth_resp = None

    def get_auth_resp(self):
        return Podbean.PB_getFileUploadAuth(self.access_token, self.fn)

    def upload_recovery_audio(self, fn):
        self.auth_resp = Podbean.PB_getFileUploadAuth(self.access_token, fn)
        self.auth_resp['filename'] = fn
        res = self.upload_audio_file(self.auth_resp)
        return res

    def publish_episode(self, pdata=None):
        self.pdata = pdata
        if not self.pdata:
            self.pdata = {
                'access_token': self.access_token,
                'title': self.title,
                'content': self.content,
                'status': 'draft',
                'type': 'public',
                'media_key': self.auth_resp['file_key'],
            }
        res = requests.post(url=self.pub_url, data=self.pdata)

        return res

    @staticmethod
    def test_recovery():
        props = PBRecovery.test()
        pbr = PBRecovery(props)
        return pbr

class PBWNL(Podbean):

    default_wnl_hosts = 'Karen Valentine, John Case'
    default_wnl_template = "pb_wnl_upload.html"
    default_broadcast = f"Broadcasts LIVE: Fridays, 7:00 AM Eastern Time."
    default_wnl_audio_dir = Config.WNL_DIR


    @staticmethod
    def test():
        props = {}

        tst_fn = "wnl__mitts_mind_09152023.mp3"

        props['filename'] = tst_fn
        props['guests'] = ["Special Guest: Michelle Obama"]
        props['title'] = "The First Lady Visits Shepherdstown"
        props['description'] = """ \"Who's Michelle? Our Michelle!\", chirps Mayor Auxer"""

        props['hosts'] = PBWNL.default_wnl_hosts
        props['broadcast'] = PBWNL.default_broadcast
        props['rec_date'] = "September 21, 2023"
        props['image_url'] = "https://play-lh.googleusercontent.com/Z_jkLpEMt5OkWanl9Mfe8ZvsUrzLmsMIjK4naUA1EYh4zIs-td1EKt3FZuSONBKOmrk"
        props['headline'] = """ \"Beautiful -- but a little too white.\" """
        return props

    def __init__(self, props):
        super().__init__()
        from app import ju
        self.ju = ju
        self.fn = None
        try:
            self.fn = os.path.join(PBWNL.default_wnl_audio_dir, props.get("filename", None))
            if not self.fn or not os.path.exists(self.fn):
                raise Exception("No Sports and comedy attack without valid file name")
        except Exception as inst:
            print(inst)
            raise inst

        self.guests = props.get('guests', None)
        self.title = props['title']
        self.hosts = props.get('hosts', PBWNL.default_wnl_hosts)
        self.broadcast = props.get('broadcast', None)
        self.template = props.get('template', PBWNL.default_wnl_template)
        self.pub_url = f"https://api.podbean.com/v1/episodes"
        self.access_token = self.getToken()
        self.headline = props['headline']
        self.rec_date = props.get('rec_date', datetime.datetime.now().strftime("%d/%m/%Y"))
        self.image_url = props.get('image_url', None)
        self.img_alt = self.title
        self.description = props.get('description', None)

        self.content = self.ju.getWNLShowPostTemplate(self).strip('\n')
        self.auth_resp = None

    def get_auth_resp(self):
        return Podbean.PB_getFileUploadAuth(self.access_token, self.fn)

    def upload_wnl_audio(self, fn):
        self.auth_resp = Podbean.PB_getFileUploadAuth(self.access_token, fn)
        self.auth_resp['filename'] = fn
        res = self.upload_audio_file(self.auth_resp)
        return res

    def publish_episode(self, pdata=None):
        self.pdata = pdata
        if not self.pdata:
            self.pdata = {
                'access_token': self.access_token,
                'title': self.title,
                'content': self.content,
                'status': 'draft',
                'type': 'public',
                'media_key': self.auth_resp['file_key'],
            }
        res = requests.post(url=self.pub_url, data=self.pdata)

        return res

    @staticmethod
    def test_wnl():
        props = PBWNL.test()
        pbw = PBWNL(props)
        return pbw


class PBSports(Podbean):

    default_sports_hosts = 'Mike Diesel, John Case'
    default_sports_template = "pb_sports_upload.html"
    default_broadcast = f"Broadcasts LIVE: Mondays, 12:00 Noon Eastern Time."
    default_sports_audio_dir = Config.WNL_DIR


    @staticmethod

    def test():
        props = {}

        tst_fn = "sports_09252023.mp3"
        props['filename'] = tst_fn
        props['guests'] = ["Special Guests:, Mickey Mantle, Henry Aaron, Babe Ruth"]
        props['title'] = "Dead Baseball Players Declare for the Presidency..."
        props['description'] = """ Mr Bill says kill em all. Let God sort it out. """

        props['hosts'] = PBSports.default_sports_hosts
        props['broadcast'] = PBSports.default_broadcast
        props['rec_date'] = "September 21, 2023"
        props['image_url'] = "https://cdn.britannica.com/83/5283-050-20357D2B/Hank-Aaron.jpg?w=400&h=300&c=crop"
        props['headline'] = """ "Dead Presidents seen Fleeing with Fremason 
        Treasures buried neath the White House" """
        return props

    def __init__(self, props):
        super().__init__()
        from app import ju
        self.ju = ju
        self.fn = None
        try:
            self.fn = os.path.join(PBSports.default_sports_audio_dir,props.get("filename", None))
            if not self.fn or not os.path.exists(self.fn):
                raise Exception("No Winners and Losers Show without valid file name")
        except Exception as inst:
            print(inst)
            raise inst
        # self.pth_fn = Path(self.fn)
        # # self.fn = self.pth_fn.name
        # self.dir = self.pth_fn.parents[0].as_posix()
        self.guests = props.get('guests', None)
        self.title = props['title']
        self.hosts = props.get('hosts', PBSports.default_sports_hosts)
        self.broadcast = props.get('broadcast', None)
        self.template = props.get('template', PBSports.default_sports_template)
        self.pub_url = f"https://api.podbean.com/v1/episodes"
        self.access_token = self.getToken()
        self.headline = props['headline']
        self.rec_date = props.get('rec_date', datetime.datetime.now().strftime("%d/%m/%Y"))
        self.image_url = props.get('image_url', None)
        self.img_alt = self.title
        self.description = props.get('description', None)

        self.content = self.ju.getSportsShowPostTemplate(self).strip('\n')
        self.auth_resp = None

    def get_auth_resp(self):
        return Podbean.PB_getFileUploadAuth(self.access_token, self.fn)

    def upload_sports_audio(self, fn):
        self.auth_resp = Podbean.PB_getFileUploadAuth(self.access_token, fn)
        self.auth_resp['filename'] = fn
        res = self.upload_audio_file(self.auth_resp)
        return res

    def publish_episode(self, pdata=None):
        self.pdata = pdata
        if not self.pdata:
            self.pdata = {
                'access_token': self.access_token,
                'title': self.title,
                'content': self.content,
                'status': 'draft',
                'type': 'public',
                'media_key': self.auth_resp['file_key'],
            }
        res = requests.post(url=self.pub_url, data=self.pdata)

        return res

    @staticmethod
    def test_sports():
        props = PBSports.test()
        pbs = PBSports(props)
        return pbs



