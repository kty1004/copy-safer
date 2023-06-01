from csv import writer

def saving_data(text_length, number_of_words_to_process, naver_dict_ping, MC, time):
    data_row=[text_length, number_of_words_to_process, naver_dict_ping, MC, time]

    #row_1 = ['text length', 'number of words to process', 'naver DICT ping', 'MC', 'time']
    with open('data.csv', 'a', newline='') as csvfile:  
        # Pass the CSV  file object to the writer() function
        writer_object = writer(csvfile)
        # Result - a writer object
        # Pass the data in the list as an argument into the writerow() function
        writer_object.writerow(data_row)  
        # Close the file object
        csvfile.close()
