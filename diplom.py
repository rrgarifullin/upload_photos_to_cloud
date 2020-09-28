import requests
from pprint import pprint
import json


class YaDisk:
    def __init__(self, name, token, photos):
        self.name = name
        self.token = token
        self.photos = photos

    def create_folder(self):
        URL = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = {
            'Accept': 'application/json',
            'Authorization': 'OAuth ' + self.token
        }
        params = {
            'path': self.name
        }
        response = requests.put(URL, headers=headers, params=params)
        if response.status_code == 200 or response.status_code == 201:
            print('Создана папка на Яндекс Диске')
        return response

    def upload_photos(self):
        info = {
            'user_name': self.name,
            'photos': [
            ]
        }
        for photo in self.photos:
            url_get = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
            headers = {
                'Accept': 'application/json',
                'Authorization': 'OAuth' + ' ' + self.token
            }
            params = {
                'path': self.name + '/' + str(photo['likes']) + '_' + str(photo['date']) + '.png'
            }
            response_get = requests.get(url_get, headers=headers, params=params)

            url_put = response_get.json()['href']
            photo_get = requests.get(photo['url'])
            ph = photo_get.content
            response_put = requests.put(url_put, files={'file': ph})
            if response_put.status_code == 200 or response_put.status_code == 201:
                print('Фото загружено')
                info['photos'].append(
                    {
                        'file_name': str(photo['likes']) + '_' + str(photo['date']) + '.png',
                        'size': 'z'
                    }
                )
        with open('result.json', 'w') as f:
            json.dump(info, f, ensure_ascii=False, indent=2)


class VK_user:
    photos = []
    TOKEN = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'

    def __init__(self, id):
        self.id = id

    def get_vk_photos(self):
        params = {
            'access_token': self.TOKEN,
            'owner_id': self.id,
            'album_id': 'profile',
            'rev': 0,
            'extended': 1,
            'photo_sizes': 1,
            'v': 5.124
        }

        response = requests.get('https://api.vk.com/method/photos.get', params=params)
        for photo in response.json()['response']['items']:
            likes = photo['likes']['count']
            date = photo['date']
            url_photo = photo['sizes'][-1]['url']
            self.photos.append({'url': url_photo, 'likes': likes, 'date': date})
        return self.photos

    def get_user_name(self):
        params = {
            'access_token': self.TOKEN,
            'user_ids': self.id,
            'v': 5.124
        }

        response = requests.get('https://api.vk.com/method/users.get', params=params)
        user_name = response.json()['response'][0]['first_name'] + ' ' + response.json()['response'][0]['last_name']
        return user_name


def user_input():
    user_id = input('Введите id пользователя Вконтакте: ')
    token_yadisk = input('Введите токен с Полигона Яндекс.Диска: ')
    return user_id, token_yadisk


def main():
    user_id, token_yadisk = user_input()
    user = VK_user(user_id)
    photos = user.get_vk_photos()
    name = user.get_user_name()
    disk = YaDisk(name, token_yadisk, photos)
    result = disk.create_folder()
    up = disk.upload_photos()


main()