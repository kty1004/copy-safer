from selenium import webdriver
from bs4 import BeautifulSoup
import re

def find_part_of_speech(soup, user_word, url, resiving_part_of):
    '''품사 찾기'''
    try:
        mean_lists=soup.find_all(class_='mean_list') # mean_list안에 또 여러 개의 mean_items가 있음.
        for mean_list in mean_lists:
            mean_items=mean_list.find_all(class_='mean_item')
            for mean_item in mean_items:
                
                if resiving_part_of==mean_item.find('p', class_='mean').find('span',class_='word_class').text.strip():
                    part_of_speech=resiving_part_of
                    
                    return part_of_speech
                else:
                    pass
        
    except AttributeError:
        print(f'{user_word}의 품사를 찾는데 실패하였음.', '\n', url)
        part_of_speech=None
        return part_of_speech

def find_synonym(soup, user_word,index):
    synonym_list=[]
    '''유의어 찾기'''
    try: # 유의어가 없을 시를 대처하기 위함.
        synonym_results=soup.find(class_='synonym_info').find(class_='cont').find_all('a')
        
        for synonym_result in synonym_results:
            synonym=synonym_result.contents[0].text.strip()
            if synonym==user_word: # 유의어 중에 user_word랑 간혹 같은 게 있다. 이걸 제거하려고 한다.
                pass
            else:
                synonym_list.append(synonym)

    except AttributeError:
            #print(f'{user_word+str(index)} 유의어 없음.')
            pass

    return synonym_list


def find_word(user_word, resiving_part_of): # 이 함수는 한 단어만을 찾는 함수다. 이 때resiving_part_of는 단어의 품사이다.
    synonym_list=[]

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    
    browser=webdriver.Chrome(options=options)
    url=f'https://ko.dict.naver.com/#/search?query={user_word}'
    browser.get(url)
    browser.implicitly_wait(20) # 암묵적 대기 --> 동적 페이지일 떄 로딩 까지 기다린다.
    
    html_source=browser.page_source


    '''bs4 start'''
    soup= BeautifulSoup(html_source, 'html.parser')

    '''동음이의어 개수 찾기'''
    homophone_boxs=[]
    try:
        homophone_boxs=soup.find('div',class_='component_keyword has-saving-function').find_all(class_='row')
        
    except AttributeError: # 왜 에러가 발생하지??? 일단 옳바른 url로 접속은 한다 리다이렉트 없다. 다른 종류의 대기를 해야 하나?
        
        #print(soup.find('body'))
        print('에러 발생')
        print(user_word)


    homophone_boxs_to_use=[]
    
    for num in range(len(homophone_boxs)):
        '''엣말 찾기'''
        try:
            mark=homophone_boxs[num].find(class_='mean_list').find(class_='mark').text.replace(" ",'') # class가 mark인게 옛말 말고도, 단어를 한자로 표현하는 div의 class도 mark임.
            if mark=='옛말':
                pass
            else:
                raise # 강제로 에러 발생시킴.
        except:
            # 이상한 단어들을 찾지 않도록 하기
            word_target= re.sub(r'[0-9]','',homophone_boxs[num].find(class_='origin').find('a').text.replace("\n",'')) # 단어에서 숫자가 있을 경우 숫자 제외.
            
            if word_target ==user_word:# 찾은 단어가 정확히 user word랑 일치하는지 확인
                
                part_of_speech=find_part_of_speech(soup=homophone_boxs[num], url=url, user_word=user_word, resiving_part_of=resiving_part_of)
                synonym_list=find_synonym(soup=homophone_boxs[num], user_word=user_word, index=num)
                if part_of_speech==None: # 품사가 없으면 재낀다.
                    pass
                elif not synonym_list: # 유의어가 없으면 재낀다.
                    pass
                else:
                    result={'품사': part_of_speech, '유의어':synonym_list}
                    homophone_boxs_to_use.append(result)
            else:
                pass

    
    browser.close()
    '''if not homophone_boxs_to_use:
        print(f'{user_word}, {resiving_part_of}:  homophone_boxs_to_use is empty. check url plz.')
        print(f'{url}')'''
    return homophone_boxs_to_use

'''
res=find_word('달리다', 'verb')
print(res)'''