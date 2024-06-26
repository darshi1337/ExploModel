# -*- coding: utf-8 -*-
"""ExploModel.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1VXkNF6qo-92JWCls40uU1ecDJ_OFOXVJ
"""

from google.colab import files
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore")

pd.set_option("display.max_columns",None)
pd.set_option("display.max_rows",None)

uploaded = files.upload()
df = pd.read_csv("predictive_maintenance.csv")
df = df.drop(["UDI", "Product ID"], axis=1)
df = df.replace({'L': 1, 'M': 2, 'H': 3})

print(df.sample(6))

display(df.shape)
display(df.size)

df.info()

df.describe()

df['Type'].value_counts()

df.apply(lambda x: x.nunique())

df['Failure Type'].value_counts()

mapping = {
    1: "No Failure",
    2: "Heat Dissipation Failure",
    3: "Power Failure",
    4: "Overstrain Failure",
    5: "Tool Wear Failure",
    6: "Random Failures"
}

df["Failure Type"] = df["Failure Type"].replace(mapping)

sns.pairplot(df, hue='Target')

colors = ['#E1728F', '#409E7D']
plt.pie(df['Target'].value_counts(),  explode=[0.1, 0.2], labels=['Not failure', 'Failure'],
        autopct='%1.1f%%', wedgeprops={'edgecolor': 'black'}, shadow=True, startangle=25,
        colors=colors)
plt.title('Failure vs not failure')
plt.tight_layout()
plt.show()

numeric_df = df.drop(columns=['Failure Type'])

plt.figure(figsize=(8, 8))
sns.heatmap(numeric_df.corr(), annot=True)
plt.show()

X = df.drop(columns=["Target", "Failure Type"], axis=1)
y = df[["Failure Type"]]

from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=69)

from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression

logistic_regression_model = LogisticRegression()
logistic_regression_model.fit(X_train, y_train)
y_pred_lr = logistic_regression_model.predict(X_test)
training_accuracy = round(logistic_regression_model.score(X_train, y_train) * 100, 2)
test_accuracy = round(accuracy_score(y_pred_lr, y_test) * 100, 2)

print("Training Accuracy: {}%".format(training_accuracy))
print("Test Accuracy: {}%".format(test_accuracy))

importance = logistic_regression_model.coef_[0]
imp_scores = pd.Series(importance, index=X_train.columns).sort_values(ascending=False)

imp_scores

f, ax = plt.subplots(figsize=(8,5))
ax = sns.barplot(x=imp_scores, y=imp_scores.index)
ax.set_title("Visualize feature scores of the features")
ax.set_yticklabels(imp_scores.index)
ax.set_xlabel("Feature importance score")
ax.set_ylabel("Features")
plt.show()

logistic_regression_model = LogisticRegression()
logistic_regression_model.fit(X_train, y_train)

def predict_logistic_regression(X):
    X = np.array(X).reshape(1, -1)
    return logistic_regression_model.predict(X)

def test_logistic_regression():
    type_of_material = float(input("Enter the type of material used: "))
    air_temperature = float(input("E30nter air temperature in Kelvin: "))
    process_temperature = float(input("Enter process temperature in Kelvin: "))
    rotational_speed = float(input("Enter rotational speed: "))
    torque = float(input("Enter torque: "))
    tool_wear = float(input("Enter tool wear: "))

    result = predict_logistic_regression([type_of_material, air_temperature, process_temperature, rotational_speed, torque, tool_wear])

    print("Predicted machine failure label: ", result)

test_logistic_regression()

from sklearn.ensemble import RandomForestClassifier

random_forest_model = RandomForestClassifier()
random_forest_model.fit(X_train, y_train)
y_pred_rf = random_forest_model.predict(X_test)
training_accuracy_rf = round(random_forest_model.score(X_train, y_train) * 100, 2)
test_accuracy_rf = round(accuracy_score(y_pred_rf, y_test) * 100, 2)

print("Training Accuracy (Random Forest): {}%".format(training_accuracy_rf))
print("Test Accuracy (Random Forest): {}%".format(test_accuracy_rf))

random_forest_model = RandomForestClassifier()
random_forest_model.fit(X_train, y_train)

def predict_rando1272m_forest(X):
    X = np.array(X).reshape(1, -1)
    return random_forest_model.predict(X)

def test_random_forest():
    type_of_material = float(input("Enter the type of material used: "))
    air_temperature = float(input("Enter air temperature in Kelvin: "))
    process_temperature = float(input("Enter process temperature in Kelvin: "))
    rotational_speed = float(input("Enter rotational speed: "))
    torque = float(input("Enter torque: "))
    tool_wear = float(input("Enter tool wear: "))

    result = predict_random_forest([type_of_material, air_temperature, process_temperature, rotational_speed, torque, tool_wear])

    print("Predicted machine failure label: ", result)

test_random_forest()

feature_scores = pd.Series(random_forest_model.feature_importances_, index=X_train.columns).sort_values(ascending=False)

feature_scores

f, ax = plt.subplots(figsize=(16, 10))
ax = sns.barplot(x=feature_scores, y=feature_scores.index)
ax.set_title("Visualize feature scores of the features")
ax.set_yticklabels(feature_scores.index)
ax.set_xlabel("Feature importance score")
ax.set_ylabel("Features")
plt.show()