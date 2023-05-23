from konlpy.tag import Komoran

# 다운한 형태소 분석기, 은전한닢(mecab), okt


'''형용사 구별법
심심하다 같은 거 구별하기: XSA앞의 단어를 찾은다음 '-하다'를 붙이자.
예쁘다 같은 거 구별하기: 그냥 VA찾고 '-다'를 붙이자.
'''
tagger=Komoran()

def change_jongyeoi_eomi(text): # 반말로 바꿔야 하는데...
    text_taggers=tagger.pos(text)
    target=('EF') # EF는 종결어미다.
    modified_text=''
    return modified_text

def stemmer(text):  #  target의 단어들을 반환함.
    
    target={'MAJ':'adv','MAG':'adv', 'NNG':'noun', 'VV':'verb','VA':'adj','IC':'감탄사','XSA':'형용사파생접미사'} # 고쳐야 할 품사들. 차후 네이버 사전에 맞게 이름들을 고쳐야 함. ex) 일반 명사는 noun로, 의존 명사는 고칠 필요없음.


    text_taggers=tagger.pos(text) # 예시:{'예쁘':'VA'}
    #print(text_taggers)

    required_synonym_substitution={}
    

    for num in range(len(text_taggers)):
        
        if text_taggers[num][1] in target: # target에 있는 것들을 찾는다. 이는 key든 value든 다 찾는다.
            # 형용사 처리
            processed_words={}
            original_word=text_taggers[num][0]  # 0인덱스가 원 문자다.
            if text_taggers[num][1]=='XSA': # 형용사 파생 접미사
                processed_words[f'{text_taggers[num-1][0]}'+'하다']=target['VA'] # 파생접미사의 바로 앞의 놈을 가져온다. 이후 품사를 adj라고 명시한다.
            elif text_taggers[num][1]=='VA' or text_taggers[num][1]=='VV': # 형용사와 동사 처리
                processed_words[f'{text_taggers[num][0]}'+'다']=target[text_taggers[num][1]]
            elif text_taggers[num][0] in processed_words:
                # 이미 찾아서 넣은 단어는 넘기기.
                continue
            else: 
                '''형용사 같이 특별한 처리가 필요하지 않은 단어들 처리'''
                processed_words[f'{text_taggers[num][0]}']=target[text_taggers[num][1]]
            
            word_pair={original_word:processed_words}
            required_synonym_substitution[original_word]=processed_words
    
    return required_synonym_substitution # 구조 {가공되기 전 단어 : {찾기 쉽게 가공된 단어: 품사 코드}, ...}

def back_to_stemmer(word, word_part_of): # 네이버 사전에서 찾은 유의어나 그런 것들 모두 필수 형태소 단위로 분리
    
    if word_part_of=='adj' and word[-2:]=='하다' and word != '하다': # 형용사일 때 만약 하다가 있을 때
        proecssed_word=word[: -2]
        return proecssed_word
    elif word_part_of=='verb' or word_part_of=='adj': # 형용사와 동사 처리 얘들은 뒤가 다로 끝난다.
        proecssed_word=word[:-1]
        return proecssed_word
    else:
        '''형용사 같이 특별한 처리가 필요하지 않은 단어들 처리할 필요 없다. 즉 단어 자체로 찾을 수 있는 애들을 말한다.'''
        return word

#user_text='크로마토그래피는 물리적 및 화학적 특성에 따라 혼합물의 성분을 분리하고 분석하기 위해 화학에서 사용되는 기술입니다.'
    