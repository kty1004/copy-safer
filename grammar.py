from jamo import h2j, j2hcj
from unicode import join_jamos
from other_tools import find_key_by_value

'''rich'''
from rich import print
from rich.console import Console

console=Console()

def grammatical_elements__jossa(jamo_without_random_synonym,jamo_random_synonym,new_texts, jamo_split_user_text):
    vowels = ['ㅏ', 'ㅑ', 'ㅓ', 'ㅕ', 'ㅗ', 'ㅛ', 'ㅜ', 'ㅠ', 'ㅡ', 'ㅣ', 'ㅐ', 'ㅔ', 'ㅒ', 'ㅖ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅢ']
    target={'이':'가','을':'를','은':'는'} # target의 키가 받침이 있을 때 쓰이는 것이다.
    if jamo_random_synonym[-1] in vowels: # random synonym이 모음으로 끝날 때
        '''받침유무에 따라 달라지는 조사 처리.'''
        if join_jamos(jamo_without_random_synonym) in list(target.keys()): # target에 있을 때
            modified_split_with_random_synonym=j2hcj(h2j(target[join_jamos(jamo_without_random_synonym)])).strip()#target의 value를 자모 분리 시킴.
            jamo_split_user_text=jamo_random_synonym+modified_split_with_random_synonym
            new_texts.append(join_jamos(jamo_split_user_text))
            #print(jamo_split_user_text)
            #raise
        else: # target에 없을 때
            #print(f'{join_jamos(jamo_random_synonym)}가 모음으로 끝나나, {join_jamos(jamo_without_random_synonym)} 에 해당하는 게 target에 적절한 게 없음. 현 위치 : {split_user_text}')
            new_texts.append(join_jamos(jamo_split_user_text))
    else: # random synonym이 자음으로 끝날 때
        if join_jamos(jamo_without_random_synonym) in list(target.values()): # target에 있을 때
            
            try:
                target_key=find_key_by_value(target, join_jamos(jamo_without_random_synonym)) # 자음으로 끝날 때는 target의 value로 key를 찾고, 이 key를 사용해야 한다.
                modified_split_with_random_synonym=j2hcj(h2j(target_key))
                jamo_split_user_text=jamo_random_synonym+modified_split_with_random_synonym
                new_texts.append(join_jamos(jamo_split_user_text))
            except TypeError:
                print(join_jamos(jamo_without_random_synonym), '\n', list(target.values()))

                raise
            
        else: # target에 없을 때
            #print(f'{jamo_random_synonym}가 자음으로 끝나나, {jamo_without_random_synonym} 에 해당하는 게 target에 적절한 게 없음. 현 위치 : {split_user_text}')
            new_texts.append(join_jamos(jamo_split_user_text))



