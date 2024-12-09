# -*- coding: utf-8 -*-
"""ML_E4_Code.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/134eITWMctLlPlSaWYOnhTFMJoQz415YA

**SVM math**
"""

# code for building and plotting SVM calculation

import numpy as np
import matplotlib.pyplot as plt

# coordinates and their labels
x = [2, 1, 5]
y = [2, 5, 3]
labels = ["(2,2) -1", "(1,5) +1", "(5,3) +1"]

dot_styles = ['x', 'o', 'o']
colors = ['red', 'blue', 'blue']

# add in calculated line
slope = 7 / 3
intercept = 17 / 3

# plot points and calculated SVM
plt.figure(figsize = (6, 6))

for i in range(len(x)):
  plt.scatter(x[i], y[i], color = colors[i], marker = dot_styles[i], s=100)
  plt.text(x[i] + 0.1, y[i] + 0.1, labels[i])

x_vals = np.linspace(0, 6, 400)
y_vals = slope * x_vals + intercept
plt.plot(x_vals, y_vals, label = r'$x_2 = \frac{7}{3}x_1 + \frac{17}{3}$', color = 'green')

plt.xlim(0, 6)
plt.ylim(0, 6)

plt.legend()

"""**Doing Data Science**"""

# import libraries and read in CSV
import pandas as pd

amazon = pd.read_csv("amazon.csv")
amazon.head()

# one hot encode top purchase category
amazon = pd.get_dummies(amazon, columns=["Top Purchase Category"])

# import libraries for DT
from sklearn.model_selection import train_test_split
from sklearn import tree
import graphviz

# split data up into train and test sets
DT_train, DT_test = train_test_split(amazon, test_size = .3, random_state = 0000)

# set label for train and test sets
DT_train_label = DT_train["Credit Card Offer"]
DT_test_label = DT_test["Credit Card Offer"]

# drop label
DT_train = DT_train.drop(["Credit Card Offer"], axis=1)
DT_test = DT_test.drop(["Credit Card Offer"], axis=1)

# instantiate decision tree
myTree = tree.DecisionTreeClassifier(criterion = 'entropy', max_depth = 4)

# fit DT model
myTree.fit(DT_train, DT_train_label)

# define feature names
FeatureNames = DT_train.columns.values

# define class names
ClassNames = myTree.classes_

# visualize decision tree

# import library
import matplotlib.pyplot as plt

# plot decision tree
plt.figure(figsize = (20, 10))
ClassNames_str = [str(x) for x in ClassNames]
MyPlot = tree.plot_tree(myTree, feature_names = FeatureNames, class_names = ClassNames_str)
plt.show()

# create confusion matrix for DT

# import library
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# use decision tree to make predictions
DT_test_pred = myTree.predict(DT_test)

# build confusion matrix
conf_matrix = confusion_matrix(DT_test_label, DT_test_pred)

# display confusion matrix
disp = ConfusionMatrixDisplay(confusion_matrix = conf_matrix, display_labels = ClassNames)
disp.plot(cmap = 'Blues')
plt.show()

# split data up into train and test sets
Reg_train, Reg_test = train_test_split(amazon, test_size = .3, random_state = 1996)

# set label for train and test sets
Reg_train_label = Reg_train["Credit Card Offer"]
Reg_test_label = Reg_test["Credit Card Offer"]

# drop label
Reg_train = Reg_train.drop(["Credit Card Offer"], axis=1)
Reg_test = Reg_test.drop(["Credit Card Offer"], axis=1)

# import libraries for logistic regression
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# instantiate logistic regression
my_log_reg = LogisticRegression()

# fit model
my_log_reg.fit(Reg_train, Reg_train_label)

# make predictions from fitted model
Reg_test_pred = my_log_reg.predict(Reg_test)

# calculate and print accuracy score (logreg)
accuracy = accuracy_score(Reg_test_label, Reg_test_pred)
print(f"Accuracy: {accuracy:.2f}")

# create confusion matrix for logreg

# import library
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# construct confusion matrix
conf_matrix = confusion_matrix(Reg_test_label, Reg_test_pred)

# display confusion matrix
disp = ConfusionMatrixDisplay(confusion_matrix=conf_matrix, display_labels=my_log_reg.classes_)
disp.plot(cmap='Blues')

# print coefficients

coefficients = my_log_reg.coef_[0]
feature_names = Reg_train.columns

for feature, coef in zip(feature_names, coefficients):
  print(f"{feature}: {coef}")

amazon = pd.read_csv("amazon.csv")

# build product catalog

products = pd.DataFrame({
    'Product Name': ['Product A', 'Product B', 'Product C', 'Product D', 'Product E', 'Product F', 'Product G', 'Product H'],
    'Category': ['Cosmetics', 'Books', 'Technology', 'Housewares', 'Cosmetics', 'Technology', 'Outdoor Gear', 'Cosmetics'],
    'Price': [22, 10, 105, 58, 37, 330, 60, 350]
})


# build recommendation function

def recommend_products(amazon, products):
  recommendations = []

  for i, user in amazon.iterrows():
    category = user['Top Purchase Category']
    avg_spending = user['Avg Monthly Spending']

    recommended_products = products[(products['Category'] == category) &
                                (products['Price'] >= avg_spending * 0.5) &
                                (products['Price'] <= avg_spending * 1.5)]

    recommendation = {
        'User': i + 1,
        'Category': category,
        'Recommended Products': recommended_products['Product Name'].tolist()
        }

    recommendations.append(pd.DataFrame([recommendation]))

  return pd.concat(recommendations, ignore_index=True)

recommendations = recommend_products(amazon, products)

print(recommendations)