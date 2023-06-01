import requests
import json
from urllib.parse import quote # 한글 url 인코딩을 할 수 있도록 도움을 줌
import re # 한글 정규식 찾기을 도와 줌.
from stemmers import back_to_stemmer

def find_word(word, word_part_of_speech_code):
        
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
        'Referer': 'https://ko.dict.naver.com/'
    }

    url_encoded_word = quote(word) # 단어 인코딩

    # https://ko.dict.naver.com/api3/koko/search?query=%EC%8B%AC%EC%8B%AC%ED%95%98%EB%8B%A4&m=pc&range=all&lang=ko&hid=168458996064396100 원래 url
    
    url = f"https://ko.dict.naver.com/api3/koko/search?query={url_encoded_word}&m=pc&range=all&lang=ko&"

    response = requests.get(url, headers=headers)
    '''hid값이 안 맞으면 데이터를 다 볼 수가 없다. 그러나, 필수적인 것은 볼 수 있으니, 크게 걱정할 필요는 없는 것 같다.'''
    if response.status_code == 200:
        try:
            search_result = response.json()
            meaning_items = search_result['searchResultMap']
            targets = meaning_items.get('searchResultListMap', {}).get('WORD').get('items')
            #print(len(targets)) # 동음이의어 가능성이 있는 단어의 개수
            # pretty_targets = json.dumps(targets, indent=2, ensure_ascii=False)


            homophones_box=[] # 동음이의어들 리스트. 최종적으로 return할 리스트임.
            except_subject_groups=('방언', '옛말', '북한어') # 품사를 찾을 때 방언이나, 옛말은 찾지 않게 하기 위함.
            for target in targets:
                
                rank=target['rank']
                '''유의어 찾기'''
                synonyms=target['expSynonym']
                if synonyms==None: #유의어가 없는 단어는 재낀다.
                    continue

                # homophones_list.append(homophone_dict)
                
                '''품사 찾기'''
                part_of_speech=None
                means_collector=target['meansCollector'][0] # 이상하게 meansCollector 안에는 하나의 리스트 요소밖에 없다. 왜 이렇게 했는지는 모르겠다.
                find_part_of_speech_code= means_collector['partOfSpeechCode']
                if find_part_of_speech_code==None: # 품사가 없는 경우 재낀다.
                    #print('there no part of speech code.')
                    continue
                else:
                    means_collectors__means=means_collector['means']
                    for means_collectors__mean in means_collectors__means:# 한 단어에 뜻이 여러 개 있는 게 있다. 동음이의어는 아니다. 근데 만약 모든 뜻에서 품사 같으면 means리스트의 languageGroupCode가 비어 있다.
                        
                        subject_group=means_collectors__mean['subjectGroup'] # 방언이나, 옛말 유무 확인.
                        # lang_group_code=means_collectors__mean['languageGroupCode']
                        if find_part_of_speech_code==word_part_of_speech_code and subject_group not in except_subject_groups:
                            
                            part_of_speech=word_part_of_speech_code
                            break
                if part_of_speech==None: # 이 if문이 실행되었다는 말은, 목표한 품사가 받지 못했다는 것이다.
                    continue

                '''유의어 찾기'''
                synonyms=synonyms.split('|') # url도 담겨있다.
                
                synonyms_result=[] # 유의어 리스트
                for synonym in synonyms:
                    synonym_text_and_url=synonym.split('^')
                    synonym_text=synonym_text_and_url[0]
                    synonym_text_only=re.findall(r'[\uac00-\ud7a3]+', synonym_text)
                    synonym_text_only=' '.join(synonym_text_only)
                    synonyms_result.append(back_to_stemmer(synonym_text_only, part_of_speech)) # 필수 형태소만 결과로 들어간다.

                # result_dict 형태 == [{'단어': {'품사':'~', '유의어':[~,~,~]}}, 딕셔너리가 동음이의어 만큼 있음.]
                
                word_value={'품사':part_of_speech,'유의어':synonyms_result}
                result_dict={back_to_stemmer(word, part_of_speech):word_value} # back_to_stemmer를 사용해서 필수 형태소만 남긴다.
                homophones_box.append(result_dict)
            '''for target in targets 끝''' 
            
            return homophones_box
        except requests.exceptions.JSONDecodeError as e:
            print(f"JSONDecodeError: {e}")
    else:
        print("Error:", response.status_code)