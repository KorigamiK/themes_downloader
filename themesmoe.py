import requests
import json
import eyed3
import subprocess
import os


class themes:
    def __init__(self, keyword, choice=None):
        self.keyword = keyword
        self.choice = choice

    @staticmethod
    def get_mal_ids(search) -> 'malids list':
        return requests.get(f"https://themes.moe/api/anime/search/{search.replace(' ', '%20')}").json()
    # @staticmethod

    def get_info_from_ids(self, ids, get_input=False):
        animeInfo = requests.post(
            "https://themes.moe/api/themes/search", json=ids).json()
        data_dict = {}
        info_dict = {}
        for index, i in enumerate(animeInfo):
            info = {}
            if get_input == True:
                print(index)
            for j, k in i.items():
                if type(k) != list:
                    if get_input == True:
                        print(j, k)
                    else:
                        pass
                    info[j] = k

                else:
                    print(j)
                    data = []
                    for l in k:
                        data.append(
                            [l['themeType'], f"{l['themeType']} {l['themeName']}.mp3", l['mirror']['mirrorURL']])
                    data_dict[index] = data
            info_dict[index] = info
            print()
        if self.choice != None:
            pass
        else:
            choice = int(input("Enter anime choice: "))
            setattr(self, 'choice', choice)
        return themes_wrapper(info_dict[self.choice], data_dict[self.choice])

    def get_and_print(self):
        return themes.get_info_from_ids(self, themes.get_mal_ids(self.keyword), get_input=True)

    def initiate_downloads(self):
        var = self.get_and_print()
        var.change_video_to_audio()
        print("Downloading please wait...")
        # print(var.links)
        self.final_embed(var.name, var.links)

    @staticmethod
    def final_embed(name, dow_urls_with_options):
        if not os.path.exists("./"+name):
            os.mkdir("./"+name)
            os.chdir("./"+name)
        else:
            os.chdir("./"+name)
        for i, j in dow_urls_with_options:
            themes.download(j, i)
            if '.jpg' in i:
                themes.embeder()

    @staticmethod
    def download(link, options_name=""):
        query = f"""wget "{link}" -q --show-progress --no-check-certificate -O "{options_name}" """
        subprocess.run(query, shell=True)

    @staticmethod
    def embeder():
        for j in os.listdir():
            if '.jpg' in j:
                image = j
        for j in os.listdir():
            if '.mp3' in j:
                themes.embed_art(j, image)
        os.remove(image)

    @staticmethod
    def embed_art(mp3, photo):
        audiofile = eyed3.load(mp3)
        if (audiofile.tag == None):
            audiofile.initTag()
        audiofile.tag.images.set(3, open(photo, 'rb').read(), 'image/jpeg')
        audiofile.tag.save()

# testinfo = {'malID': 37521, 'name': 'Vinland Saga', 'year': 2019, 'season': 'summer'}
# testdata = [['OP1', 'OP1 MUKANJYO', 'https://animethemes.moe/video/VinlandSaga-OP1-NCBD1080.webm'], ['OP2', 'OP2 Dark Crow', 'https://animethemes.moe/video/VinlandSaga-OP2-NCBD1080.webm'], ['ED1', 'ED1 Torches', 'https://animethemes.moe/video/VinlandSaga-ED1-NCBD1080.webm'], ['ED2', 'ED2 Drown', 'https://animethemes.moe/video/VinlandSaga-ED2-NCBD1080.webm']]


class themes_wrapper:
    def __init__(self, info, links):
        self.name = info['name']
        self.info = info
        self.links = links
        self.malID = info['malID']

    @property
    def cover(self):
        return requests.get(f"https://animethemes-api.herokuapp.com/api/v1/anime/{self.malID}").json()['cover']

    def change_video_to_audio(self):
        for j, i in enumerate(self.links):
            self.links[j][2] = themes_wrapper.get_music_from_video(
                self, i[0], i[2])
            self.links[j].pop(0)
        self.links.append(["cover.jpg", self.cover])

    def get_music_from_video(self, themetype, video):
        response = requests.post(
            f"https://themes.moe/api/themes/{self.malID}/{themetype}/audio", json=[video])
        return response.text
# https://themes.moe/api/themes/24405/OP3/audio


test = themes(input('Enter anime name: '))
test.initiate_downloads()
# themes_wrapper.get_music_from_video("https://animethemes.moe/video/VinlandSaga-OP1-NCBD1080.webm")
# testwrap = themes_wrapper(testinfo, testdata)
# testwrap.change_video_to_audio()
