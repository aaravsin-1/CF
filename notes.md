```cpp title=cheat-command
pip install httpie
http -d https://github.com/aaravsin-1/CF/raw/main/AI.py

python AI.py "solve main.py and fill blanks" main.py > solved.py
cp solved.py main.py

```

# feature scaling
for **numerical** like values like **age** : 12,14,18 compared to **salary**:20k,30k, the model might think that salary is more important because values are bigger while both are **equally** **important**
### 2 ways:
1) Min max scaling ( **when we want values in the range 0-1**) 
- eg age = 40, min = 20;max = 60 ; thus range = 60-20 = 40 and scaled value = (age-min)/range
Algos that care about this:
- **K-Nearest Neighbors (KNN)**
- **K-Means**
- **Neural networks**
- Some optimization/gradient-descent problems

1) Standardization( **when data has different ranges / outliers(technically not but mentioned)**)
- changes values such that average = 0, and standard deviation/spread = 1
Algos
- **Linear regression**
- **Logistic regression**
- **SVM**
- **PCA**
- **KNN / K-Means**
- Neural networks

**for stuff like random forests/ gradient boosting XGBoost u dont need scaling**

eg:
```python title=scaling.py
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler
// {} means creating a dictionary ( key:value)
//[] means list
//dataframe is a table(rows and colums)

data = 
{
	"Age":[18,19,20,21],
	"Salary":[21000,22000,56000,89000]
}
df = pd.DataFrame(data)//creates a dataframe(coverts dictionary to table)
print("Og\n",df)

minmax_scaler = MinMaxScaler()//creates an object of that class we imported

//fit_transform does two things, fits the data to df and transforms df

df_minmax = pd.DataFrame(minmmax_scaler.fit_transform(df),columns = df.columns)

//the columns = , just signifies to use og column names

print("scaled", df_minmax)

standard_scaler = StandardScaler()
df_standard = pd.DataFrame(standard_scaler.fit_transform(df), columns=df.columns)
print("scaled", df_standard)

```

```python title=test.py
import pandas as pd
from sklearn.preprocessing import MinMaxScaler,StandardScaler

df = pd.read_csv("employees.csv")
//selecting one column = df["Age"]
//selecting multiple = df [["Age", "Salary"]]//list of list

numeric = df[["Age","Salary"]]

minmax_scaler = MinMaxScaler()
scaled_data = minmax_scaler.fit_transform(numeric)

df_scaled = pd.DataFrame(scaled_data,columns=["Age","Marks"])

//adding Name column back
df_scaled["Name"] = df["Name"]//not great method

df_scaled.insert(0,"Name",df["Name"])

//incase you want to add multiple columns(do insert twice or)
df_full = pd.concat([df[["Employees","Name"]],df_scaled],axis=1)
//axis = 1 means columns

```

# encoding categorical data

