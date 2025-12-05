import pandas as pd
pd.plotting.register_matplotlib_converters()
import matplotlib.pyplot as plt
import seaborn as sns


titanic = "archive/train_and_test2.csv"

try:
    df = pd.read_csv(titanic)
    df = df.rename(columns={"Sex":"Gender"})
    df["Embarked"] = df["Embarked"].fillna("Unknown")
    """df = df.astype({"Embarked": int})"""
    df["Gender"] = df["Gender"].map({0: "F", 1: "M"})
    df["age_sort"] = df["Age"].apply(lambda x : "Child" if x < 20 else "Adult" ) 
    df["qcut_fare"] = pd.qcut(df["Fare"],4 ,labels=["low","middle","high","very-high"])
    

    """plt.figure(figsize=(9,6))
    sns.histplot(df["Age"])
    plt.title("Age analyze with Histogram")"""       

    """plt.figure(figsize=(9,6))
    sns.barplot(y=df["2urvived"],x=df["Pclass"])
    plt.title("Class Distribution for Survived")"""
    
    """plt.figure(figsize=(9,6))
    sns.scatterplot(x=df["Fare"],y=df["Age"])
    plt.title("Fare distribution for Age ")"""       
    
       
    """plt.figure(figsize=(9,6))
    sns.kdeplot(data=df, x="Fare",hue="Gender",fill=True)
    plt.title("Fare Analyze for Gender")  """     

   
    """sns.jointplot(data=df, x="Age",y="Passengerid",kind="hex", color="#4CB391")
    sns.jointplot(data=df, x="Age", y="Fare", kind="scatter", color="#4CB391")
    sns.jointplot(data=df, x="Age", y="Fare", kind="kde", color="#4CB391")"""



    plt.figure(figsize=(9,6))
    sns.boxplot(data=df, x="Pclass", y="Age")
    plt.figure(figsize=(9,6))
    sns.countplot(data=df, x="Gender", hue="Pclass")
    
    plt.show()

    print(
        
        df.head(),"\n",
        df["Embarked"].value_counts(),"\n",
       
               
    )

except FileNotFoundError:
    print("Couldn't read csv")