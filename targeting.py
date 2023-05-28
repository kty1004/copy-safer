from jamo import h2j, j2hcj
import random

'''rich'''
from rich import print
from rich.console import Console
from grammar import grammatical_elements__jossa

console=Console()


def adjust_synonym_list_with_randomness(randomness:int, synonyms): # randomness에 따라 synonyms에서 유의어를 뽑아줌.
    if randomness==1:
        cut_synonym=synonyms[0]
        return cut_synonym
    else:
        cut_synonyms=synonyms[:randomness-1]
        jamo_random=j2hcj(h2j(random.choice(cut_synonyms))) # 무작위로 뽑은 유의어를 자모 분리 시켰다.
        jamo_random_synonym=''.join(jamo_random) # 이거 중요하다!!! 코딩 지식!! 이렇게 하는 이유는 random함수를 한 번만 실힝시키겠금 하기 위함이다. 이렇게 안 하고 jamo_random을 그대로 쓰면 해당 변수가 호출될 떄마다, random함수가 실행된다.
        return jamo_random_synonym

def targeting_with_result_list(user_text:str, result_list:list, randomness: int):
    
    '''새로운 글 만들기'''


    split_user_texts=user_text.split() # user_text는 맨 처음에 user에게서 입력받았던 texts
    new_texts=[]
    result_list_num=0

    for split_user_text in split_user_texts: # 띄어쓰기 단위로 user가 준 글을 자른다.
        
        list__value=result_list[result_list_num]
        #print(list__value)


        list__value=list(list__value.values())[0][0] # list의 첫 번째 √alue를 뜻한다. 일단은 가장 유력한 동음이의어부터 사용해본다. 이를 의미하는 것이 마지막 인덱스다. 첫번쨰 인덱스는 list()로 생긴 리스트를 까려고 만든 것이다.
        # list__value는 dict이다. 
        
        processed_word= list(list__value.keys())
        #print(processed_word)
        
        processed_word="".join(processed_word)
        # back_to_stemmer에 의해 가공된 단어를 추출했다. processed_word의 타입은 str이다.
        processed_word__value=list__value[processed_word] # 이제 {'품사' :, '유의어': []} 까지 온 것이다. processed_word__value는 dict이다.
        synonyms=processed_word__value['유의어'] # 유의어 리스트를 뽑아왔다.

        '''자모 분리로 타겟팅하기: 자모분리를 함으로써 맞춤법을 교정할 것이다.'''

        jamo_split_user_text=j2hcj(h2j(split_user_text))
        jamo_processed_word=j2hcj(h2j(processed_word))
        jamo_processed_word2=jamo_processed_word[:-1] # 자모 분리할 떄 jamo_processed_word 마지막 문자는 눈감아 줘야 할 떄가 있다.
        if jamo_processed_word in jamo_split_user_text or jamo_processed_word2 in jamo_split_user_text and result_list_num <= len(result_list): # 제대로 targeting이 되었을 때.
            
            jamo_random_synonym=adjust_synonym_list_with_randomness(randomness=randomness, synonyms=synonyms)
            '''if jamo_processed_word2 in jamo_split_user_text:
                jamo_processed_word=jamo_processed_word2'''
            jamo_split_user_text=jamo_split_user_text.replace(jamo_processed_word, jamo_random_synonym)
            jamo_without_random_synonym= jamo_split_user_text.replace(jamo_random_synonym, '') # jamo_random_synonym를 기준으로 jamo_split_user_text 분리
            
            '''문법 교정'''
            grammatical_elements__jossa(jamo_random_synonym=jamo_random_synonym, jamo_without_random_synonym=jamo_without_random_synonym, new_texts=new_texts, jamo_split_user_text=jamo_split_user_text)
            
            
            
            if result_list_num < len(result_list)-1: # result_list_num이 result_list의 크기를 넘어가지 않게 하기 위함.
                result_list_num=result_list_num+1

        else: # targeting이 안되었을 때
            print(f'processed word :[green]{processed_word}[/green], user text: [green]{split_user_text}[/green]')
            # 구지 자모 분리 할 필요 없이 바로 new_texts에 넣는다.
            
            new_texts.append(split_user_text)

    if result_list_num != len(result_list)-1:
        print('result list에 있는 모든 단어를 사용하지 못함. 사용한 result_list_num : ', result_list_num)

        raise
    new_texts=' '.join(new_texts)
    console.rule('[bold red] 바뀐 텍스트')
    console.print(f'[bold]{new_texts}')
    return new_texts
    