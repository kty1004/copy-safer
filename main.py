from multiprocessing import Process,Manager
import find_to_dict
import parlanceGPT
from stemmers import stemmer
from jamo import h2j, j2hcj
import random
from unicode import join_jamos
# 프로그램 끝나는 시간 계산하려고 불러옴.
import time

'''multiprocessing''' 

if __name__=='__main__': # 이걸 왜 해야 하는 거지??? 일단 하라니깐 한다.
    
    start = time.time()

    user_text='크로마토그래피는 혼합물을 구성하는 성분을 분리하고 분석하는 기술로, 화학 물질의 정량 및 정성 분석에 사용됩니다. 크로마토그래피는 샘플을 이동시키는 이동 상으로부터 특정 성분을 분리하는 방식으로 작동합니다. 이를 위해 정지 상, 이동 상, 그리고 분석 대상인 샘플이 필요합니다. 주로 액체 크로마토그래피(LC)와 가스 크로마토그래피(GC)가 사용되며, 각각은 액체와 기체 상에서 분리가 이루어집니다. 크로마토그래피는 다양한 분야에서 활용되며, 정확하고 신속한 분석 결과를 제공합니다.'

    api_key=''
    #modified_text=parlanceGPT.change_parlance(user_text=user_text, api_key=api_key)
    modified_text=user_text
    

    user_word_list=[]
    user_word_part_of_list=[]

    stemmer_values=list(stemmer(user_text).values()) # {찾기 쉽게 가공된 단어}

    for num in range(len(stemmer_values)):
        user_word_part_of_list__part_of=list(stemmer_values[num].values()) # 품사
        user_word_part_of_list__word=list(stemmer_values[num].keys()) # 가공된 단어
        '''chaging list to str'''
        user_word_part_of_list__word=''.join(user_word_part_of_list__word)
        user_word_part_of_list__part_of=''.join(user_word_part_of_list__part_of)
        user_word_list.append(user_word_part_of_list__word)
        user_word_part_of_list.append(user_word_part_of_list__part_of)


    print(stemmer(modified_text),'\n',f'처리할 단어 수 : {len(stemmer(modified_text))}')
    
    manager = Manager()
    return_list=manager.list()


    multiprocessing_core=1 # 병럴 처리 몇 개로 할 건지 결정
    processing=[] # join함수를 쓰기 위함.

    '''유의어 대치'''
    for i in range(multiprocessing_core): # 문장 별로 쪼개서 넣는게 낫지 않을까????
        future_bundle=((len(user_word_list)//multiprocessing_core))*(i+1)
        current_bundle=((len(user_word_list)//multiprocessing_core))*(i) # current_bundle은 현재 bundle의 시작점을 말함.

        if i==0:
            print(user_word_list[: future_bundle], '첫 번째 코어')
            th=Process(target=find_to_dict.find_word_many, args=((user_word_list[: future_bundle]),(user_word_part_of_list[: future_bundle]),return_list, i))
            
        elif type(len(user_word_list)/multiprocessing_core)!= 'int' and i==multiprocessing_core-1: # muliti core 수랑 user word list 수를 나눌 때 딱 안 떨어지면 마지막 인덱스를 처리 못해서 이 코드를 작성함.
            print((user_word_list[current_bundle: ]),f'{i+1}번째 코어')
            th=Process(target=find_to_dict.find_word_many, args=((user_word_list[current_bundle: ]),(user_word_part_of_list[current_bundle: ]),return_list, i))
        else:
            print(user_word_list[current_bundle : future_bundle], f'{i+1}번째 코어')
            th=Process(target=find_to_dict.find_word_many, args=((user_word_list[current_bundle : future_bundle]),(user_word_part_of_list[current_bundle : future_bundle]),return_list, i))
        processing.append(th)
        th.start()


    for num in range(len(processing)):
        processing[num].join() # 멀티 프로세싱 종료
        print(f'process{num+1} is over.')
    
    '''동음이의어 처리'''

    
    result_list=[] # 멀티 프로세싱을 사용할 때 return list안의 자료들이 뒤죽박죽 셖여서 제대로 작동을 하지 않는다.
    
    used_index=[]
    where_return_list__element__index=[]
     # return list에서 현재 처리까지 처리한 요소 인덱스
    
    #print('\nreturn list 요소 정리 시작\n')

    for processing_index in range(multiprocessing_core): # for 문을 사용하면 안되겠네...
        # list(return_list__element.keys())[0]  현재 몇 코어에서 온 결과값인지 알 수 있음.
        return_list_index=0
        while return_list_index <= multiprocessing_core-1:
            return_list__element=return_list[return_list_index]
            return_list__element__index=list(return_list__element.keys())[0]
            if  processing_index == return_list__element__index and return_list_index not in used_index: # 제대로 찾았을 때
                used_index.append(return_list__element__index) # 이미 처리한 return_list_index이 무엇인지 알기 위함이다.
                where_return_list__element__index.append({processing_index: return_list_index}) # return_list_index는 return list안에 들어 있는 각 리스트들이 몇 번 째인지 나타낸 것이다. 고로, 읽는 방법은 processing_index에 해당하는 return_list__element__index을 가지고 있는 return list안의 리스트의 index값은 return_list_index라는 말이다.
                result_list.extend(list(return_list__element.values())[0])
                 # 이 의미는 정상적으로 찾았으니, 다음 while문에서는 return_list_index+1번째부터 찾으라는 말이다.
                #print('while statement must be break')
                break
                # break문 해버리면 for 문까지 깨져 버리는 듯 하다.
            else:
                #print('while statement still alive')
                return_list_index+=+1
        # break으로 while문이 깨졌을 때
        return_list_index+=+1 # return_list_num번째까지는 처리했으니, 그 다음부터 처리하라는 말이 된다.
            
    '''
    print(used_index) # used_index가 오름차순으로 있어야 성공한 것이다.
    print(where_return_list__element__index)
    '''

    '''새로운 글 만들기'''
    split_user_texts=user_text.split()
    new_texts=[]
    result_list_num=0
    for split_user_text in split_user_texts: # 띄어쓰기 단위로 user가 준 글을 자른다.
        list__value=result_list[result_list_num]
        list__value=list(list__value.values())[0][0] # list의 첫 번째 √alue를 뜻한다. 일단은 가장 유력한 동음이의어부터 사용해본다. 이를 의미하는 것이 마지막 인덱스다. 첫번쨰 인덱스는 list()로 생긴 리스트를 까려고 만든 것이다.
        # list__value는 dict이다. 
        
        processed_word= list(list__value.keys())
        processed_word="".join(processed_word)
        # back_to_stemmer에 의해 가공된 단어를 추출했다. processed_word의 타입은 str이다.
        processed_word__value=list__value[processed_word] # 이제 {'품사' :, '유의어': []} 까지 온 것이다. processed_word__value는 dict이다.
        synonyms=processed_word__value['유의어'] # 유의러 리스트를 뽑아왔다.

        '''자모 분리로 타겟팅하기'''
        jamo_split_user_text=j2hcj(h2j(split_user_text))
        jamo_processed_word=j2hcj(h2j(processed_word))
        if jamo_processed_word in jamo_split_user_text or jamo_processed_word[:-1] in jamo_split_user_text: # 제대로 targeting이 되었을 때. 자모 분리할 떄 jamo_processed_word 마지막 문자는 눈감아 줘야 할 떄가 있다.
            jamo_random_synonym=j2hcj(h2j(random.choice(synonyms))) # 무작위로 뽑은 유의어를 자모 분리 시켰다.
            jamo_split_user_text=jamo_split_user_text.replace(jamo_processed_word, jamo_random_synonym)
            new_texts.append(join_jamos(jamo_split_user_text))
            result_list_num=result_list_num+1
        else: # targeting이 안되었을 때
            #print('processed wod :',processed_word, 'user text: ', split_user_text)
            # 구지 자모 분리 할 필요 없이 바로 new_texts에 넣는다.
            if processed_word=='따르' and split_user_text=='따라':
                print(jamo_processed_word, jamo_split_user_text)
            new_texts.append(split_user_text)
    new_texts=' '.join(new_texts)
    print(new_texts)
    end = time.time() # 프로그램 끝나는 시간 계산.

    excuted_word_num=0
    for list in return_list:
        excuted_word_num+=len(list)
        '''for word in list:
            print(word, '\n')'''
    print(f"단어 처리 수 : {excuted_word_num} \n 작동 시간:{end - start} sec")