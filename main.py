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
import random
from make_data.make_sentence_data import random_split_senctence


if __name__=='__main__': # 이걸 왜 해야 하는 거지??? 일단 하라니깐 한다.
            
    text='한때 먼 옛날, 한 마을에 사는 소녀가 있었습니다. 그녀의 이름은 에밀리였습니다. 에밀리는 작은 집에서 어머니와 함께 살고 있었는데, 그녀는 어머니를 너무나 사랑했습니다. 어머니는 에밀리가 태어나자마자 아버지와 이별한 후 혼자서 에밀리를 키워왔던 강한 여성이었습니다. 에밀리는 어머니로부터 사랑과 관용, 인내심을 배웠습니다. 그녀는 어머니가 자신에게 이야기해주는 많은 이야기에 감명을 받아 세상을 탐험하는 상상력을 길러갔습니다. 에밀리는 또한 읽기와 쓰기를 좋아했습니다. 그녀는 작은 도서관에서 독서를 하며 다양한 이야기의 세계로 빠져들곤 했습니다. 어느 날, 에밀리는 작은 마을에 엄청난 신비한 이야기가 돌고 있다는 것을 듣게 되었습니다. 이 마을에는 노래하는 샘물이 있다는 소문이었습니다. 그 노래를 듣게 되면 소원을 이룰 수 있다는 것이었습니다. 에밀리는 믿을 수 없는 소리에 흥분하여 그 샘물을 찾아 나섰습니다. 마을 밖으로 나선 에밀리는 숲을 헤치며 샘물을 찾아갔습니다. 그녀는 잠시 멈추어 숨을 고르고 샘물의 노래를 듣기 시작했습니다. 그 노래는 환상적이었습니다. 바람과 샘물의 소리, 새들의 지저귐까지가 유려한 음악으로 어우러져 마음을 편안하게 만들었습니다. 에밀리는 소원을 하나 만들었습니다. 그녀는 세상을 여행하며 모든 사람들에게 사랑과 희망을 전해주는 작은 별이 되고 싶었습니다. 그녀는 마음을 다잡고 소원을 샘물에 담아 보냈습니다. 그리고 마을로 돌아왔습니다. 하지만 에밀리는 자신의 소원이 이루어질지 모른다는 걱정에 잠이 오지 않았습니다. 한동안 도시의 밀집된 거리를 달리던 남자가 있었습니다. 그의 이름은 엘리엇이었습니다. 엘리엇은 어릴 적부터 도시의 소음과 분주한 생활에 익숙해져 있었습니다. 그는 긴 근무 시간과 끊임없는 사회적 압박으로 인해 지쳐 있었습니다. 그러나 어느 날, 엘리엇은 자신의 일상에 변화를 주기로 결심했습니다. 엘리엇은 친구의 추천으로 작은 시골 마을에 머물기로 결정했습니다. 이 마을은 자연의 아름다움으로 유명했습니다. 엘리엇은 기대와 두려움을 안고 마을로 향했습니다. 도착한 순간부터 엘리엇은 마을의 매력에 사로잡혔습니다. 신선한 공기와 푸른 잔디밭, 작은 강이 흐르는 풍경은 그의 마음을 진정시켜주었습니다. 엘리엇은 마을 사람들과 어울리며 그들의 따뜻한 환영을 느낄 수 있었습니다. 마을 사람들은 서로를 돕고 존중하는 문화를 가지고 있었습니다. 엘리엇은 이 마을에서 조용하고 평온한 생활을 즐기면서도 새로운 친구들을 사귀었습니다. 그는 마을 주민들과 함께 일하고 식사하며 자연과 조화를 이루는 삶을 경험했습니다. 엘리엇은 시간이 지남에 따라 자신의 욕망과 가치에 대해 깊이 생각하게 되었습니다. 그는 도시에서의 번잡한 삶에 집착했던 자신을 되돌아보며, 더욱 의미있는 삶을 추구하고자 마음먹었습니다. 한편으로는 엘리엇은 도시에서의 경험과 기술을 마을에 기여할 수 있는 방법을 찾기도 했습니다. 그는 마을 사람들과 함께 지역 사회를 발전시키기 위한 프로젝트를 시작했습니다. 이를 통해 엘리엇은 자신의 역량을 발휘하면서도 마을의 문화와 가치를 보존하고 향상시키는 데 기여할 수 있었습니다. 시간이 흐르면서, 엘리엇은 마을이 자신을 변화시키는 동시에 그 또한 마을에 변화를 주는 존재가 되었습니다. 그의 열정과 영감은 다른 사람들에게도 전해져 마을은 더욱 번영하게 되었습니다. 엘리엇의 이야기는 우리에게 마을과 도시의 차이, 자연과 사회의 대립과 조화를 생각해보게 합니다. 그는 우리에게 삶의 진정한 가치와 의미를 되새기며, 조용한 곳에서도 큰 꿈을 이룰 수 있다는 희망을 주는 주인공입니다. 한동안 어수선한 도시에서 살던 여자가 있었습니다. 그녀의 이름은 루시이며, 일상적인 회사 생활에 지친 상태였습니다. 하지만 그녀는 꿈을 가지고 있었습니다. 그 꿈은 모험과 자유가 있는 삶을 즐기는 것이었습니다. 어느 날, 루시는 신기한 책을 발견했습니다. 이 책은 어릴 적에 들었던 동화처럼 보였지만, 루시는 그 안에 특별한 힘이 있다는 예감을 느꼈습니다. 그녀는 호기심에 휩싸여 책을 열어 읽기 시작했습니다. 읽는 순간, 루시는 놀라운 일이 벌어지기 시작했습니다. 그녀는 책 안으로 빨려들어가 마법의 세계로 들어온 것을 알게 되었습니다. 그곳에서 루시는 말하는 동물들과 마법사, 요정들과 만나며 신나는 모험을 시작했습니다. 루시는 용감하게 여행을 떠났습니다. 함께하는 친구들과 함께 알 수 없는 대륙을 넘어 다양한 도시와 마을을 탐험했습니다. 그녀는 마법의 능력을 갖게 되었고, 이를 통해 어려운 상황을 극복하며 자신의 역량을 발견해갔습니다.  루시는 그 세계에서 배운 지혜와 용기를 현실 세계로 가져왔습니다. 그녀는 일상의 어려움을 극복하며 새로운 가능성을 탐색하고 자신의 꿈을 이루기 위해 노력했습니다. 루시는 돌아온 후에도 도전적인 정신을 잃지 않았습니다. 그녀는 일상을 새롭게 바라보고, 창의적인 삶을 추구하며 세상을 변화시키는 데 기여했습니다. 그녀의 이야기는 우리에게 단순한 현실에 안주하지 않고 꿈과 모험을 향해 나아갈 용기를 줍니다. 루시의 모험은 우리에게 상상력의 힘과 현실을 넘어선 가능성을 상기시킵니다. 그녀는 자유와 창의력을 통해 인생을 더욱 완벽하게 만들 수 있다는 놀라운 메시지를 전달합니다.'

    def coy_safer_(user_text, mc):
        console=Console()
        install(show_locals=True)
        
        ping_check=speed_checking_for_naver_dict()
        
        start = time.time()
        randomness=3 # randomness must be bigger than 0.
        #user_text='화학 반응에서 열은 그 반응의 시작과 끝 상태만으로 결정되며, 도중의 경로에는 관계하지 않는다는 법칙이다. 물리적, 화학적 변화가 일어날 때 어떤 경로를 거쳐 변화가 일어나든지 관계없이 반음에 관여한 총 열량은 보존된다.'
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


        multiprocessing_core=mc # 병럴 처리 몇 개로 할 건지 결정
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
        
    def collecting_data(long_text: str, random_mc_range: int, re_collecting_num:int):
        for num in range(re_collecting_num):
            random_sentences_list=random_split_senctence(long_text)
            
            for random_sentences in random_sentences_list:
                random_mc=random.randint(1, random_mc_range)
                coy_safer_(random_sentences, random_mc)
    
    collecting_data(text, 10, re_collecting_num=25)
        
 
        
        