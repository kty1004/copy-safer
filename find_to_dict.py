from word_crawling import find_word

def find_word_many(user_word_list,user_word_part_of_list,return_list, processing_num):
    result_dicts=[]
    for num in range(len(user_word_list)):
        user_word=user_word_list[num]
        user_word_part_of=user_word_part_of_list[num]
        res_find_word= find_word(word=user_word, word_part_of_speech_code=user_word_part_of)

        if not res_find_word: # find_word에 아무것도 안 들어 있으면 처리한 단어로 치지 않음.
            pass
        else: # processing_num은 멀티코어 번호다. 이를 알아야 나중에 결과물이 뒤섞이지 않은체, result_dicts에 보관된다.
            result_dict={user_word:res_find_word} # result_dict 형태 == [{'단어': {'품사':'~', '유의어':[~,~,~]}}, 딕셔너리가 동음이의어 만큼 있음.]
            result_dicts.append(result_dict)
        

    
    return_list.append({processing_num:result_dicts}) # 딕서녀리들을 모아둔 리스트