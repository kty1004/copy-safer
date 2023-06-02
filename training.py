# MC is Multiprocessing Core.
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pandas as pd

'''sklearn'''
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split,KFold # dataset에서 †raining값과 †esting 값을 분류해줌.
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import PolynomialFeatures
import joblib


name=['text-length', 'number-of-words-to-process', 'naver-DICT-ping', 'MC', 'time']
df = pd.read_csv("data.csv", names=name)
df.head()

x = df.iloc[:, :-1].values 
y = df.iloc[:, -1].values


x_list=[]
for num in range(4):
    x_list.append(df.iloc[:,num].values)

for x_index in range(len(x_list)): # x값들을 순차적으로 가져옴
    x_element=x_list[x_index]
    sorted_indices = np.argsort(x_element) # x를 오름차순으로 정렬한 인덱스를 가져옴

    # x와 y를 정렬된 인덱스에 맞게 정렬
    sorted_x = np.array(x_element)[sorted_indices]
    sorted_y = np.array(y)[sorted_indices]
    sns.scatterplot(x=sorted_x, y=sorted_y, data=df)
    plt.xlabel(name[x_index])
    #plt.show() # 이중에서 mc와 times(y에 해당)의 간의 관계가 눈에 띈다.


# 회귀 모델을 결정하기 위해 y의 형태를 봄
sorted_data = sorted(y) # 단순히 y를 오름차순으로 정렬.
plt.plot(sorted_data)
plt.xlabel('Index')
plt.ylabel('Value')
plt.title('Sorted Data')
#plt.show()

'''k-fold'''
def k_fold(k_value):
    k=5
    kflod=KFold(n_splits=k,shuffle=True)
    accuracy_score=[]

    for train_index, test_index in kflod.split(x):
        x_train, x_test=x.iloc[train_index, :], x.iloc[test_index, :]
        y_train, y_test=y.iloc[train_index], y.iloc[test_index]



'''Validation data'''
Validation_data = [214,30,0.07352614402770996,2,6.861304759979248]
Validation_data__x_array=np.array(Validation_data[:-1]) # list--> array형태로 해야 reshape사용 가능.
Validation_data__x=Validation_data__x_array.reshape(1,-1) #단일 샘플이므로 reshape가 필요. 단일 샘플은 한 번의 관측 결과를 말함. 이 때 reshape(1,-1)을 사용해야 함.

'''다중 선형 회귀'''
def mulit_linnear(x,y):
    mlr_1=LinearRegression()

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20)
    mlr_1.fit(x_train, y_train)

    print('다중 선형 회귀 train score', mlr_1.score(x_train, y_train))
    print('다중 선형 회귀 test score', mlr_1.score(x_test, y_test))
    predict_y=mlr_1.predict(Validation_data__x)
    print('다항 회귀 모델을 사용한 예측값 : ',predict_y)
    


'''다항 회귀'''
def poly_linear(x,y, degree):
    mlr = LinearRegression() #  다항 회귀 모델 생성
    poly_features = PolynomialFeatures(degree=degree)  # n차 다항식 사용
    X_poly = poly_features.fit_transform(x)

    x_train, x_test, y_train, y_test = train_test_split(X_poly, y, test_size=0.20)

    mlr.fit(x_train, y_train)
    print('train set score: ',mlr.score(x_train, y_train)) # R^2=0.9437972402466835

    test_score=mlr.score(x_test, y_test)
    if test_score<0: # 음수
        print('model overfitting, test set score: ',mlr.score(x_test, y_test))
    else:
        print('test set score: ',mlr.score(x_test, y_test))
    '''모델 예측 평가'''
    

    
    validation_x__poly=poly_features.fit_transform(Validation_data__x)
    predict_y=mlr.predict(validation_x__poly)
    print('다항 회귀 모델을 사용한 예측값 : ',predict_y)
    

mulit_linnear(x,y)
poly_linear(x,y,3)


'''차수에 따른 score
> 과적합은 뻄.

왜 돌릴 떄 마다 score가 달라지지..? 너무 크게 달라지네... 너무 학습하는 자료가 없어서 그런가?? k-fold 사용하자.
- 2차
train set score:  0.6749956082635031
test set score:  0.8380652556933682
- 3차
train set score:  0.8008305711759697
test set score:  0.8018319761441871
'''

'''
# 모델 저장
joblib.dump(mlr, 'model.joblib')

# 모델 불러오기
model = joblib.load('model.joblib')

# 모델 예측
predictions = model.predict(X_test)

print(predictions)
'''



'''

from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense
names = ['text length', 'number of words to process', 'naver DICT ping', 'MC', 'time']
dataset = pd.read_csv('data.csv', names=names)
df = pd.read_csv('data.csv')

# 속성을 X, 클래스를 y로 저장합니다.
X = df.iloc[:,0:4]
y = df.iloc[:,4]

# 그래프로 확인해 봅시다.


# 모델 설정
model = Sequential()
model.add(Dense(12,  input_dim=4, activation='relu'))
model.add(Dense(8,  activation='relu'))
model.add(Dense(3, activation='relu'))
model.summary()

# 모델 컴파일
model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['accuracy'])

# 모델 실행
history=model.fit(X, y, epochs=100, batch_size=3)'''