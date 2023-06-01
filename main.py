from multiprocessing import Process,Manager
import crawling.find_to_dict as find_to_dict
import parlanceGPT
from stemmers import stemmer
import time


'''rich'''
from rich.progress import track
from rich import print
from rich.console import Console
from rich.traceback import install


'''머신러닝을 위해 필요한 데이터 수집하는 함수 불러옴.'''
from targeting import targeting_with_result_list
from make_data.speed_checking import speed_checking_for_naver_dict
from make_data.saving_csv import saving_data



if __name__=='__main__': # 이걸 왜 해야 하는 거지??? 일단 하라니깐 한다.
    console=Console()
    install(show_locals=True)
    
    ping_check=speed_checking_for_naver_dict()
    
    start = time.time()
    randomness=3 # randomness must be bigger than 0.
    user_text='화학 반응에서 열은 그 반응의 시작과 끝 상태만으로 결정되며, 도중의 경로에는 관계하지 않는다는 법칙이다. 물리적, 화학적 변화가 일어날 때 어떤 경로를 거쳐 변화가 일어나든지 관계없이 반음에 관여한 총 열량은 보존된다.'
    console.rule('[bold blue]입력받은 텍스트')
    console.print(f'[bold]{user_text}')
    console.rule('[bold red]유의어 대치 프로그램 시작')
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

    number_of_words_to_process=len(stemmer(modified_text))
    print('\n',f'처리할 단어 수 : [bold red]{number_of_words_to_process}[/bold red]')
    
    manager = Manager()
    return_list=manager.list()


    multiprocessing_core=5 # 병럴 처리 몇 개로 할 건지 결정
    processing=[] # join함수를 쓰기 위함.
    
    '''유의어 대치'''
    with console.status("[bold blue]multiprocessing...") as status:
        for i in range(multiprocessing_core): # 문장 별로 쪼개서 넣는게 낫지 않을까????
            future_bundle=((len(user_word_list)//multiprocessing_core))*(i+1)
            current_bundle=((len(user_word_list)//multiprocessing_core))*(i) # current_bundle은 현재 bundle의 시작점을 말함.

            if i==0:
                print(f'{user_word_list[: future_bundle]} : 첫 번째 코어')
                th=Process(target=find_to_dict.find_word_many, args=((user_word_list[: future_bundle]),(user_word_part_of_list[: future_bundle]),return_list, i))
                
            elif type(len(user_word_list)/multiprocessing_core)!= 'int' and i==multiprocessing_core-1: # muliti core 수랑 user word list 수를 나눌 때 딱 안 떨어지면 마지막 인덱스를 처리 못해서 이 코드를 작성함.
                print(f'{(user_word_list[current_bundle: ])} : {i+1}번째 코어')
                th=Process(target=find_to_dict.find_word_many, args=((user_word_list[current_bundle: ]),(user_word_part_of_list[current_bundle: ]),return_list, i))
            else:
                print(f'{user_word_list[current_bundle : future_bundle]} : {i+1}번째 코어')
                th=Process(target=find_to_dict.find_word_many, args=((user_word_list[current_bundle : future_bundle]),(user_word_part_of_list[current_bundle : future_bundle]),return_list, i))
            processing.append(th)
            th.start()

        
        for num in range(len(processing)):
            processing[num].join() # 멀티 프로세싱 종료
    
    '''-----with 문 끝------'''
    
    '''동음이의어 처리'''
    
    
    '''return list 정리'''
    result_list=[] # 멀티 프로세싱을 사용할 때 return list안의 자료들이 뒤죽박죽 셖여서 제대로 작동을 하지 않는다.
    
    used_index=[]
    where_return_list__element__index=[]
     # return list에서 현재 처리까지 처리한 요소 인덱스
    
    #print('\nreturn list 요소 정리 시작\n')
    
    for processing_index in range(multiprocessing_core): 
        # list(return_list__element.keys())[0]  현재 몇 코어에서 온 결과값인지 알 수 있음.
        return_list_index=0
        while return_list_index <= multiprocessing_core-1:
            return_list__element=return_list[return_list_index]
            return_list__element__index=list(return_list__element.keys())[0]
            if  processing_index == return_list__element__index and return_list__element__index not in used_index: # 제대로 찾았을 때
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
            
    
    #print(used_index) # used_index가 오름차순으로 있어야 제대로 정렬이 된 것이다.
    # print(where_return_list__element__index)
    
    #print(result_list)
    
    '''문법 교정으로 새로운 글 만들기'''
    new_texts=targeting_with_result_list(user_text=user_text, result_list=result_list, randomness=randomness, used_index=used_index)
    end = time.time() # 프로그램 끝나는 시간 계산.

    '''머신 러닝을 위한 데이터 수집'''
    saving_data(MC=multiprocessing_core, text_length=len(user_text), number_of_words_to_process=number_of_words_to_process, naver_dict_ping=ping_check, time=end-start)
    # 처리할 단어수, 유저 텍스트 길이, 네이버 사전 핑 그리고 멀티코어 수, 총 작동 시간을 csv에 저장할 것이다.
    
    
    print(f"단어 처리 수 : {len(result_list)} \n 작동 시간:{end - start} sec")