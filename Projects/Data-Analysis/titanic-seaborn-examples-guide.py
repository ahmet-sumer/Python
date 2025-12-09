import pandas as pd
pd.plotting.register_matplotlib_converters()
import matplotlib.pyplot as plt
import seaborn as sns


titanic = "archive/train_and_test2.csv"

try:
    #* Reads DataFrame
    df = pd.read_csv(titanic) 

    #* Renames Sex distirbution with Gender
    df = df.rename(columns={"Sex":"Gender"}) 

    #* Replaces NaN values with Unknown 
    df["Embarked"] = df["Embarked"].fillna("Unknown") 

    #* Sets Gender Values as 1 and 0 
    df["Gender"] = df["Gender"].map({0: "F", 1: "M"}) 

    #* Makes a new column (age_sort) categorizing age 
    df["age_sort"] = df["Age"].apply(lambda x : "Child" if x < 20 else "Adult" )

    #* Makes a new column (qcut_fare) "qcut_fare" dividing "Fare" into 4 equal-frequency bins
    #* with labels: "low", "middle", "high", "very-high"
    df["qcut_fare"] = pd.qcut(df["Fare"],4 ,labels=["low","middle","high","very-high"])
 
    
#! =========== Visualization Templates ============


#^ Histogram: Visualize the distribution of Age Variable
    """plt.figure(figsize=(9,6))
    sns.histplot(df["Age"])
    plt.title("Age analyze with Histogram")"""       


#^ Bar Plot: Shows Survival rate across different passenger Classes
    """plt.figure(figsize=(9,6))
    sns.barplot(y=df["2urvived"],x=df["Pclass"])
    plt.title("Class Distribution for Survived")"""


#^ Scatter Plot: Show Relationship between Fare and Age
    """plt.figure(figsize=(9,6))
    sns.scatterplot(x=df["Fare"],y=df["Age"])
    plt.title("Fare distribution for Age ")"""       


#^ Linear Regression Plot: Show trend line Between Age and Fare 
    """sns.lmplot(data=df, x="Age", y="Fare")
    plt.title("Age distribution for Fare ")"""       
    

#^ Strip Plot: Show individual points of Age distribution across Passenger Classes
    """sns.stripplot(data=df, x="Pclass", y="Age")
    plt.title("Pclass distribution for Age ")"""      


#^ Regression Plot: Show Scatter points with regression line between Fare vs Age
    """sns.regplot(data=df, x="Fare", y="Age")
    plt.title("Fare distribution for Age ")"""


#^ KDE Plot: Kernel Density Estimation showing Fare distribution by Gender
#? fill=True makes a colored area under the curve
    """plt.figure(figsize=(9,6))
    sns.kdeplot(data=df, x="Fare",hue="Gender",fill=True)
    plt.title("Fare Analyze for Gender")"""       


#^ Joint Plot: Show bivariate relationships with different plot types
#? kind=hex makes a hexbin plot, kind=scatter shows dots, kind=kde shows density  
    """sns.jointplot(data=df, x="Age",y="Passengerid",kind="hex", color="#4CB391")
    sns.jointplot(data=df, x="Age", y="Fare", kind="scatter", color="#4CB391")
    sns.jointplot(data=df, x="Age", y="Fare", kind="kde", color="#4CB391")"""


#^ Box Plot: Show Age distribution across passenger Classes with customizations
    """plt.figure(figsize=(9,6))
    sns.boxplot(data=df, x="Pclass", y="Age",                      
                notch=True, showcaps=False,                        #? notch=True Adds confidence intervals, showcaps=False removes whisker caps
                flierprops={"marker": "^"},                        #? flierprops={"marker":"^"} customizes outlier markers
                boxprops={"facecolor": (.3, .5, .7, .5)},          #? boxprops={"facecolor":(.3, .5, .7, .5)} sets box color and transparency
                medianprops={"color": "r", "linewidth": 2})"""     #? medianprops={"color": "r", "linewidth": 2} sets middle lines color and width
    

#^ Count Plot: Show frequency of each Gender category, further divided by Passenger Class
    """plt.figure(figsize=(9,6))
    sns.countplot(data=df, x="Gender", hue="Pclass")"""
    

#^ Heatmap
    #? Select only numerical columns from DataFrame
    numeric_df = df.select_dtypes(include=("number"))

    #? Calculate correlation matrix using Pearson Correlation coefficent
    #? Each cell shows the correlation strength between two variables (-1 to +1)
    corr = numeric_df.corr()    

    #^ Visualize correlation matrix as heatmap
    plt.figure(figsize=(16,9))
    sns.heatmap(
                corr,
                annot=True,             #* Display correlation values inside each cells
                fmt=".2f",              #* Format values to 2 decimal places
                cmap="coolwarm",        #* Color Palette: cool (blue/negative) to warm (red/positive)
                center=0,               #* Centers the color scale at 0 
                square=True             #* Make cells square-shaped instead of rectangular
                )
    plt.title("Correlation Matrix Heatmap")
    plt.tight_layout()


#^ Violin Plot: Detailed Distribution about Age by Embarked Port and Gender
#? split=True places to violins side by side for comparision 
#? inner="quart" shows quartile lines inside of violins
#? fill=False Doesn't colorise violin areas
#? palette={"F": "gray", "M": "lightblue"} sets palette of Age distribution with colors 
    """sns.violinplot(data=df, x="Embarked", y="Age", hue="Gender",
                fill=False,                 #* split=True places to violins side by side for comparision 
                split=True,                 #* inner="quart" shows quartile lines inside of violins
                inner="quart",              #* fill=False Doesn't colorise violin areas
                palette={"F": "gray",       #* palette={"F": "gray", "M": "lightblue"} sets palette of Age distribution with colors 
                  "M": "lightblue"})      
    plt.title("Age Analyze for Gender")"""

#& Displays all plots
    plt.show()

#* Prints first 5 rows of the DataFrame
    print(
        
        df.head(),"\n",
    )

#! If cannot read the file outputs this Error
except FileNotFoundError:
    print("Couldn't read csv")