import random
from kss import split_sentences


def extract_random_elements(lst: list, num_elements : int):
    if num_elements > len(lst):
        #print("Error: Number of elements to extract exceeds the length of the list.")
        return {'random_elements':list, 'lst' :lst}

    random_elements = random.sample(lst, num_elements)
    for random_element in random_elements:
        lst.remove(random_element)
    return {'random_elements':random_elements, 'lst' :lst}


def random_split_senctence(long_text):
    # 문장별로 나누고 렌덤하게 합치자. 그냥 정해진 문장 수로만 하면 안되나??
    sentence_list=[]
    random_num_elements_range=6
    random_num_elements=int(random.randint(3,random_num_elements_range))
    for sentence in split_sentences(long_text):
        sentence_list.append(sentence)
    new_sentences_list=[]
    while sentence_list:
        random_sentences=extract_random_elements(sentence_list, num_elements=random_num_elements)['random_elements']
        
        sentence_list=extract_random_elements(sentence_list, num_elements=random_num_elements)['lst']
        try: 
            random_sentences=' '.join(random_sentences)
            new_sentences_list.append(random_sentences)
        except TypeError:
            # 뜬금없이 random_sentences의 type이 type이 되버려서 에러가 난다...
            break
        
    
    #print(new_sentences_list)
    
    
    return new_sentences_list
    
