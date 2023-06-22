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
from sklearn.model_selection import KFold

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

'''Validation data'''
Validation_data = [214,30,0.07352614402770996,2,6.861304759979248]
Validation_data__x_array=np.array(Validation_data[:-1]) # list--> array형태로 해야 reshape사용 가능.
Validation_data__x=Validation_data__x_array.reshape(1,-1) #단일 샘플이므로 reshape가 필요. 단일 샘플은 한 번의 관측 결과를 말함. 이 때 reshape(1,-1)을 사용해야 함.

'''다항 회귀'''
mlr = LinearRegression() #  다항 회귀 모델 생성
degree=4
poly_features = PolynomialFeatures(degree=degree)  # n차 다항식 사용
X_poly = poly_features.fit_transform(x)

#x_train, x_test, y_train, y_test = train_test_split(X_poly, y, test_size=0.20)

for k in range(2,31):
    # Create a KFold object with 'k' folds
    kf = KFold(n_splits=k)

    best_accuracy = 0.0  # Variable to store the best accuracy
    best_model = None   # Variable to store the best model

    # Iterate over the folds
    for train_index, test_index in kf.split(X_poly):
        # Get the training and testing data for this fold
        X_train, X_test = X_poly[train_index], X_poly[test_index]
        y_train, y_test = y[train_index], y[test_index]
        
        # Train the model on the training data
        mlr.fit(X_train, y_train)
        
        # Evaluate the mlr on the testing data
        accuracy = mlr.score(X_test, y_test)
        
        # Check if this mlr has better accuracy
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_model = mlr

    # Print the best accuracy
    print(f"Best_Accuracy: {best_accuracy}", f"k: {k}")