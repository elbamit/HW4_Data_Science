from platform import platform
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np

# Function that gets a path of a 'xlsx' file, reads it and converts it to a dataframe
def load_xlsx(path):
    # Checks the path is for an 'xlsx' file
    if path.endswith(".xlsx"):
        df = pd.read_excel(path)
        return df
    else:
        return None

# Function that gets a dataframe and completes numerical columns that have missing values
def complete_missing_numerical_values(df):
    df = df.fillna(df.mean())
    return df

# Function that standardize all the numerical columns (except year)
def standardize_df(df):
    # Gets a list of all the column names except country (str) and year (don't want to standardize)
    columns = df.columns.to_list()
    columns.remove("country")
    columns.remove("year")

    # Standardize each column of the dataframe
    for colName in columns:
        df[colName] = (df[colName] - df[colName].mean()) / df[colName].std()
    
    return df

# Function that groups all the rows by the country and calculates their means in each column. It also removes the 'year' column
def group_by_country(df):
    df = df.groupby(['country']).mean()
    df.drop('year', axis=1, inplace=True)
    return df

# Function that creates a KMeans model with the given number of clusters and number of iterations
def create_KMeans_model(df, n_clusters, n_init):
    kmeans_res = KMeans(n_clusters=n_clusters, init='random', n_init=n_init).fit_predict(df)
    df["cluster"] = kmeans_res
    return df

# Function that receives a dataframe and create a scatter plot by the 'Generosity' and 'social_support' features
def show_scatter_plot(df):
    plt.scatter(df["Social support"].to_numpy(), df["Generosity"].to_numpy(), s=10, c=df["cluster"].to_numpy(), alpha=0.5)
    plt.show()

    # return plot/





df = load_xlsx("Dataset.xlsx")
df = complete_missing_numerical_values(df)
df = standardize_df(df)
df = group_by_country(df)
df = create_KMeans_model(df, 5, 3)
# print(df)
show_scatter_plot(df)
# plot.show()




# np.random.seed(19680801)

# N = 164
# x = df["Social support"].to_numpy()
# y = df["Generosity"].to_numpy()
# plt.scatter(df["Social support"].to_numpy(), df["Generosity"].to_numpy(), s=10, c=df["cluster"].to_numpy(), alpha=0.5)

# colors = np.random.rand(N)
# area = (30 * np.random.rand(N))**2  # 0 to 15 point radii

# plt.scatter(x, y, s=20, alpha=0.5)
# plt.show()


