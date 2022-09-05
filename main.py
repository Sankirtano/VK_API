import requests
import json
import os


#  First we need to create app in VK and get access_token with them. Make it with your hands, not with code.
token = 'your_token'
user_id = 'your_id'


def write_albums(data):
    with open('albums.json', 'w') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def write_photos(data, name):
    with open('photos.json', 'w') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def get_largest(size_dict):
    if size_dict['width'] >= size_dict['height']:
        return size_dict['width']
    else:
        return size_dict['height']


def download_photo(url, name):
    r = requests.get(url, stream=True)
    filename = str(name) + '.jpg'
    with open(filename, 'bw') as file:
        for chunk in r.iter_content(4096):
            file.write(chunk)


def download_photo_like(url, name):
    r = requests.get(url, stream=True)
    filename = 'like' + str(name) + '.jpg'
    with open(filename, 'bw') as file:
        for chunk in r.iter_content(4096):
            file.write(chunk)


def main():
    r = requests.get('https://api.vk.com/method/photos.getAlbums', params={'owner_id': user_id,
                                                                           'access_token': token, 'v': 5.131})
    write_albums(r.json())
    albums = json.load(open('albums.json'))
    root_root = os.getcwd()
    if not os.path.exists('photos'):
        os.makedirs('photos')
    os.chdir('photos')
    for thing in albums['response']['items']:
        path = thing['title']
        root_path = os.getcwd()
        isExist = os.path.exists(path)
        if not isExist:
            os.makedirs(path)
        r = requests.get('https://api.vk.com/method/photos.get', params={'owner_id': user_id, 'album_id': thing['id'],
                                                                         'photo_sizes': 1, 'extended': True,
                                                                         'rev': 0, 'count': 1000,
                                                                         'access_token': token, 'v': 5.131})
        write_photos(r.json(), path)
        photos = json.load(open('photos.json'))
        os.chdir(path)
        max_like, url = 0, ''
        for photo in photos['response']['items']:
            sizes = photo['sizes']
            max_size_url = max(sizes, key=get_largest)['url']
            download_photo(max_size_url, photo['id'])
            like = int(photo['likes']['count'])
            if like >= max_like:
                max_like = like
                url = max_size_url
        download_photo_like(url, max_like)
        os.chdir(root_path)
        os.remove('photos.json')
    os.chdir(root_root)
    os.remove('albums.json')


if __name__ == '__main__':
    main()
