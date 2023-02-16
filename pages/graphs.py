import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


movie = pd.read_csv(
    'tmdb_5000_movies.csv')
popular = movie.sort_values('popularity', ascending=False)

st.header("Popular Movies")
fig = plt.figure(figsize=(12, 4))
plt.barh(popular['title'].head(10), popular['popularity'].head(
    10), align='center', color='darkblue')
plt.gca().invert_yaxis()
plt.xlabel('popularity')
plt.title('Popular Movies')

st.pyplot(fig)

budget = movie.sort_values('budget', ascending=False)

st.header("Highest Budget")
fig1 = plt.figure(figsize=(12, 4))
plt.barh(budget['title'].head(10), budget['budget'].head(
    10), align='center', color='darkblue')
plt.gca().invert_yaxis()
plt.xlabel('Budget')
plt.title('Highest Budget')

st.pyplot(fig1)

st.header("Relation between Runtime and N.of movies")
plt.title("Relation between Runtime and N.of movies")
fig2 = plt.figure(figsize=(12, 4))
plt.xlabel("runtime of movies ")
plt.ylabel("number of movies ")
plt.hist(movie["runtime"], bins=30, color="y")
st.pyplot(fig2)

st.header("Relation Between Runtime and Budget")
plt.title("Relation Between Runtime and Budget")
fig3 = plt.figure(figsize=(12, 4))
plt.xlabel("runtime")
plt.ylabel("Highest Budget")
plt.scatter(movie["runtime"], movie["budget"], alpha=0.3, color="g")
st.pyplot(fig3)

count = pd.Series(movie['genres'].str.cat(
    sep='|').split('|')).value_counts(ascending=False)

st.header("Top Genors")
fig4 = plt.figure(figsize=(12, 4))
diagram = count[:10].plot.bar(fontsize=6)
diagram.set(title='Top Genres')
diagram.set_xlabel('Type of genres')
diagram.set_ylabel('Number of Movies')

st.pyplot(fig4)



graph_fig = [fig, fig1, fig2, fig3, fig4]
caption = ["Popular Movies","Highest Budget","Relation between Runtime and N.of movies", "Relation Between Runtime and Budget", "Top Genors"]


        # cols[1].pyplot(j)




