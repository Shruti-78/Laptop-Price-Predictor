# -*- coding: utf-8 -*-
"""Miniproject.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1grYsocl9oZKSS-Va-Y9oc0dmjXCmCFlz

# **DATA CLEANING**
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

laptops = pd.read_csv("laptops_test.csv")
laptops["RAM"] = laptops["RAM"].str.replace('GB', '')
laptops["Weight"] = laptops["Weight"].str.replace('kg', '')
laptops["Screen Size"] = laptops["Screen Size"].str.replace('"', '')
df = pd.DataFrame()
laptops["Storage"] = laptops["Storage"].str.replace('GB', '')
laptops["Storage"] = laptops["Storage"].str.replace('TB', '000')
new=laptops["Storage"].str.split("+", n = 1, expand = True)
df["first"]= new[0]
df["first"]=df["first"].str.strip()
df["second"]= new[1]
df["Layer1HDD"] = df["first"].apply(lambda x: 1 if "HDD" in x else 0)
df["Layer1SSD"] = df["first"].apply(lambda x: 1 if "SSD" in x else 0)
# df['first'].str.split().apply(lambda x:x[0])
df['first']=df['first'].str.split().apply(lambda x:x[0])

df["second"].fillna("0", inplace = True)    # filling none with 0
df["Layer2HDD"] = df["second"].apply(lambda x: 1 if "HDD" in x else 0)
df["Layer2SSD"] = df["second"].apply(lambda x: 1 if "SSD" in x else 0)
df['second']=df['second'].str.split().apply(lambda x:x[0])

df["first"] = df["first"].astype(int)
df["second"] = df["second"].astype(int)
df["HDD"]=(df["first"]*df["Layer1HDD"]+df["second"]*df["Layer2HDD"])
df["SSD"]=(df["first"]*df["Layer1SSD"]+df["second"]*df["Layer2SSD"])

df.drop(columns=['first', 'second', 'Layer1HDD', 'Layer1SSD',
        'Layer2HDD', 'Layer2SSD'
       ],inplace=True)
new_df=laptops['Screen'].str.split('x',n=1,expand=True)    #splitting screen resolution
df['X_res'] = new_df[0]
df['Y_res'] = new_df[1]
df['X_res']=df['X_res'].str.split().apply(lambda x:x[-1])
df['X_res'] = df['X_res'].astype('int')
df['Y_res'] = df['Y_res'].astype('int')

df['Cpu'] = laptops['CPU'].apply(lambda x:" ".join(x.split()[0:3]))
def fetch(y):
    if y == 'Intel Core i7' or y == 'Intel Core i5' or y == 'Intel Core i3':
        return y
    else:
        if y.split()[0] == 'Intel':
            return 'Other Intel Processor'
        else:
            return 'AMD Processor'

df['CPU'] = df['Cpu'].apply(fetch)
df.drop(columns=['Cpu'],inplace = True)
df['GPU'] = laptops['GPU'].apply(lambda x : x.split()[0])

"""# **ENCODING ATTRIBUTES**"""

le = LabelEncoder()

df['enManufacturer'] = le.fit_transform(laptops['Manufacturer'])
df['enRAM'] = (laptops['RAM']).astype(int)
df['enWeight'] = (laptops['Weight']).astype(float)
df['enScreen_Size'] = (laptops['Screen Size']).astype(float)
df['enCategory'] = le.fit_transform(laptops['Category'])
df['enModel'] = le.fit_transform(laptops['Model Name'])
df['enOS'] = le.fit_transform(laptops['Operating System'])
df['enGPU'] = le.fit_transform(df['GPU'])
df['enCPU'] = le.fit_transform(df['CPU'])
df['enOSV'] = (laptops['Operating System Version']).astype(int)
df['PPI'] = (((df['X_res']**2) + (df['Y_res']**2))**0.5/df['enScreen_Size']).astype('float')
df['price'] = laptops['Price'].astype(float)
df['price'] = df['price']/100
print(df['price'])

"""# **COMPARING EACH ATTRIBUTE WITH PRICE**"""

df1 = pd.DataFrame()
df1["HDD"]=df["HDD"]
df1["SSD"]=df["SSD"]
df1['Manufacturer']=laptops['Manufacturer']
df1['RAM'] = laptops['RAM'].astype(int)
df1['Weight'] = (laptops['Weight']).astype(float)
df1['Screen Size']=laptops['Screen Size'].astype(float)
df1['Category'] = laptops['Category']
df1['CPU'] = df['CPU']
df1['GPU'] = df['GPU']
df1['OSV'] = laptops['Operating System Version']
df1['PPI'] = (((df['X_res']**2) + (df['Y_res']**2))**0.5/df['enScreen_Size']).astype('float')
df1['price'] = df['price']

"""**PLOTTING STUDY OF PRICE RANGE**"""

import seaborn as sns
#target column distribution
sns.distplot(df1['price'],color='purple')
plt.title("study of price range")
plt.xlabel("Price in lakhs(Rs)")
plt.show()
print("This plot shows that the price of laptop ranges between 30 thousand to 3.5 lakh Rs")

# comparing average price based on attributes
def avgprice_attribute(a) :
  attribute =sorted(df1[a].unique())
  attribute_avgprice =df1.groupby([a])['price'].mean()
  print("Average price(in lakhs) comparing based on",a)
  print(attribute_avgprice)
  sns.barplot(x=attribute,y=attribute_avgprice).set_xticklabels(attribute, rotation=90)
  plt.xlabel(a,fontsize=12)
  plt.ylabel("Average price(in lakhs)",fontsize=12)
  plt.xticks(fontsize=10)
  plt.yticks(fontsize=10)
  avg_price=df['price'].mean()
  print("Average price of laptop : Rs.",avg_price)
  plt.axhline(y = avg_price, color ="green", linestyle ="--")
  plt.show()

"""**PLOTTING HDD VS PRICE**"""

print("HDD in GB")
avgprice_attribute('HDD')

"""**PLOTTING SSD VS PRICE**"""

print("SSD in GB")
avgprice_attribute('SSD')

"""**PLOTTING MANUFACTURER VS PRICE**"""

avgprice_attribute('Manufacturer')

"""**PLOTTING RAM VS PRICE**"""

print("RAM in GB")
avgprice_attribute('RAM')

"""**PLOTTING SCREEN SIZE VS PRICE**"""

print("Screen Size in inches")
avgprice_attribute('Screen Size')

"""**PLOTTING CATEGORY VS PRICE**"""

avgprice_attribute('Category')

"""**PLOTTING GPU VS PRICE**"""

avgprice_attribute('GPU')

"""**PLOTTING CPU VS PRICE**"""

avgprice_attribute('CPU')

"""**PLOTTING PPI VS PRICE**"""

avgprice_attribute('PPI')

"""**PLOTTING SCATTER PLOTS FOR ALL ATTRIBUTES VS PRICE**"""

def compare(att,color):
  attribute =df1[att]
  price=df1['price']
  plt.scatter(attribute,price,color=color)
  plt.xticks(attribute, rotation=90)
  plt.title("Scatter plot")
  plt.xticks(fontsize=10)
  plt.xlabel(att)
  plt.ylabel("Price(in lakhs)")
  plt.show()

compare('HDD','pink')
compare('SSD','yellow')
compare('CPU','red')
compare('GPU','purple')
compare('Manufacturer','blue')
compare('RAM','orange')
compare('Screen Size','cyan')
compare('Category','brown')
compare('OSV','green')
compare('PPI','violet')

"""# **PLOTTING HEATMAP**"""

df.drop(columns=['X_res', 'Y_res','CPU','GPU'],inplace=True)
plt.figure(figsize=(17,17))
dataplot = sb.heatmap(df.corr(), cmap="YlGnBu", annot=True)  # plotting correlation heatmap
sns.set(font_scale = 1.7)

plt.show()# displaying heatmap

"""# **MULTIPLE REGRESSION**"""

from sklearn import linear_model
# from sklearn.metrics import classification_report
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.metrics import accuracy_score
from sklearn.metrics import r2_score

x = df[['SSD', 'PPI','enGPU','enRAM','enOSV']]
y = df['price']
x_train,x_test = train_test_split(x,test_size = 0.2,random_state = 0)
y_train,y_test = train_test_split(y,test_size = 0.2 , random_state =0)

regr = linear_model.LinearRegression()
regr.fit(x_train, y_train)

score = r2_score(y_test,regr.predict(x_test))
print("The accuracy of our model is {}%".format(round(score, 2) *100),"\n")

#predicting price based on user inputs
ram = int(input("Enter size of RAM in GBs: "))
ssd = int(input("Enter size of SSD in GBs: "))
ppi = float(input("Enter PPI: "))
gpu = int(input("Enter GPU(0 for 'AMD', 1 for 'Intel', 2 for 'Nvidia'): "))
osv = int(input("Enter OS version: "))

print("\nPredicted price is: Rs. ",regr.predict([[ssd,ppi,gpu,ram,osv]]))

"""# **DECISION TREE REGRESSION**"""

from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score

tree_reg = DecisionTreeRegressor(max_depth=5)

# Train the model on the training set
tree_reg.fit(x_train, y_train)

# Make predictions on the testing set
y_pred = tree_reg.predict(x_test)

# Evaluate the model using mean squared error and R-squared score
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
# print("Mean Squared Error:", mse)
print("The accuracy of our model is {}%".format(round(r2, 2) *100),"\n")

#predicting price based on user inputs
ram = int(input("Enter size of RAM in GBs: "))
ssd = int(input("Enter size of SSD in GBs: "))
ppi = float(input("Enter PPI: "))
gpu = int(input("Enter GPU(0 for 'AMD', 1 for 'Intel', 2 for 'Nvidia'): "))
osv = int(input("Enter OS version: "))

print("\nPredicted price is: Rs. ",tree_reg.predict([[ssd,ppi,gpu,ram,osv]]))

"""As the accuracy of decision tree regression is more than the accuracy of multiple regression, thus we can say that decision tree regression is more suitable algorithm to use for this model."""