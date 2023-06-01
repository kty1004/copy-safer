import requests
from urllib.parse import quote # 한글 url 인코딩을 할 수 있도록 도움을 줌
import time

def speed_checking_for_naver_dict():
    word='심심하다'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
        'Referer': 'https://ko.dict.naver.com/'
    }

    url_encoded_word = quote(word) # 단어 인코딩

    url = f"https://ko.dict.naver.com/api3/koko/search?query={url_encoded_word}&m=pc&range=all&lang=ko&"
    start_time = time.time()
    response = requests.get(url, headers=headers)
    end_time=time.time()
    times=end_time-start_time
    
    if response.status_code==200:
        return times
    else:
        print(response.status_code, 'fail to checking DICT ping.')