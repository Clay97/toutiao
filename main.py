#coding:utf-8
import requests
import time
from urllib.parse import urlencode
import os
from hashlib import md5
from multiprocessing.pool import Pool
def get_page(offsetp):
    t = time.time()
    timestamp = int(t * 1000)
    params = {
        'aid': 24,
        'app_name': 'web_search',
        'offset': offsetp,
        'format': 'json',
        'keyword': '街拍',
        'autoload': 'true',
        'count': 20,
        'en_qc': 1,
        'cur_tab': 1,
        'from': 'search_tab',
        'timestamp': timestamp
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
        'Cookie': 'tt_webid=6698224417073694219; UM_distinctid=16b1c89b4891dc-07c5eab40102ac-4c312d7d-100200-16b1c89b48a400; csrftoken=f2f895fa787b16b95088a70f7de231c9; __tasessionId=v9ffxsrfd1559551950358; CNZZDATA1259612802=1433961361-1559551484-https%253A%252F%252Flanding.toutiao.com%252F%7C1559551484; s_v_web_id=72ad7620bc7eee5c573a2fe6966db22e'
    }
    #url = 'https://www.toutiao.com/api/search/content/?' + urlencode(params)
    try:
        r = requests.get('https://www.toutiao.com/api/search/content/?', headers=headers, params=params)
        if r.status_code == 200:
            return r.json()
    except requests.ConnectionError :
        return None



def get_images(json):
    if json.get('data'):
        for item in json.get('data'):
            title = item.get('title')
            if (title == None):
                continue
            images = item.get('image_list')
            for image in images:
                yield {
                    'image': image.get('url'),
                    'title': title
                }

def save_image(item):
    title = item.get('title')
    if not os.path.exists(title):
        try:
            os.mkdir(title)
        except Exception as e:
            print(e)
            return
    try:
        response = requests.get(item.get('image'))
        if response.status_code == 200:
            file_path = '{0}/{1}.{2}'.format(title,md5(response.content).hexdigest(),'jpg')
            if not os.path.exists(file_path):
                with open(file_path,'wb') as f:
                    f.write(response.content)
            else:
                print('Aready Download',file_path)
    except requests.ConnectionError :
        print("Failed to save image")

def main(offset):
    print(offset)
    json = get_page(offset)
    for item in get_images(json):
        print(item)
        save_image(item)
        time.sleep(1)

GROUP_START = 1
GROUP_END = 20

if  __name__ == "__main__":
    pool = Pool()
    pool.map(main, [i*20 for i in range(1)])
    pool.close()
    pool.join()
    print("OK")








