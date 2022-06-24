from platform import platform
from matplotlib.figure import Figure
import pandas as pd
from sklearn import cluster
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

import numpy as np
import plotly.express as px
import chart_studio.plotly as py
from urllib.request import urlopen
import json


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
    df = df.groupby(['country'], as_index=False).mean()
    df.drop('year', axis=1, inplace=True)
    return df

# Function that creates a KMeans model with the given number of clusters and number of iterations
def create_KMeans_model(df, n_clusters, n_init):
    kmeans_res = KMeans(n_clusters=n_clusters, init='random', n_init=n_init).fit_predict(df.iloc[:,1:])
    df["cluster"] = kmeans_res
    return df

# Function that receives a dataframe and create a scatter plot by the 'Generosity' and 'social_support' features
def scatter_plot(df):
    figure = Figure(figsize=(4,4))
    plt = figure.add_subplot(111)
    list_of_clusters = df['cluster'].unique().tolist()
    list_of_clusters.sort()
    list_of_clusters.append(len(list_of_clusters))
    
    
    myplot = plt.scatter(df["Social support"].to_numpy(), df["Generosity"].to_numpy(), s=10, c=df["cluster"], alpha=0.5)
    figure.colorbar(myplot, boundaries = list_of_clusters)
    plt.set_xlabel("Social support")
    plt.set_ylabel("Generosity")
    plt.title.set_text("Social support over Generosity")



    # plt.legend(handle)

    return figure

    # return plot/

def choropleth_map(df):
    
    try:
        with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
            countries = json.load(response)

        
            
            fig = px.choropleth(geojson=countries, locations=df['country'], color=df['cluster'],
                                range_color=(0, len(df['cluster'].unique().tolist())-1),
                                locationmode = "country names",
                                scope="world",
                                labels={'unemp':'clusters'}
                                )
            fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, title_text='K Means Clustering Visualization Per Country')
            # fig.show()

            py.sign_in("amitelb", "YDSzG3wsuZmLH33ulK5r")
            py.image.save_as(fig, filename = "Horopleth.png")
        return True
    except:
        return False

# YDSzG3wsuZmLH33ulK5r



# df = load_xlsx("Dataset.xlsx")
# df = complete_missing_numerical_values(df)
# df = standardize_df(df)
# df = group_by_country(df)
# df = create_KMeans_model(df, 4, 3)

# scatter_plot(df)
# show_horopleth_map(df)
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


