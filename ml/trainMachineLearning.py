import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import tree
import pickle

df = pd.read_csv('Salary_Data.csv') 
input_columns = ["YearsExperience","Age"]
output_columns = ["Salary"] 
X = df.loc[:,input_columns] 
y = df.loc[:,output_columns] 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = .20, random_state = 1,)


df.dropna(inplace = True)

clf = tree.DecisionTreeRegressor(random_state = 0) 

y_p = clf.predict(X_test)

print(np.sqrt(metrics.mean_squared_error(y_test, y_p)))

pickle.dump(clf, open('decisiontree.pickle', 'wb'))