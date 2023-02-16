import pickle
import streamlit as st
import requests
import pandas as pd

# Functions

def fetch_director(movie):
    url = "https://api.themoviedb.org/3/movie/{}/credits?api_key=f0c86086f96e336c33b3090ec586ea8c&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    data = data['crew']
    data = pd.DataFrame(data)
    crew_index = data.loc[data['job'] == 'Director'].index[0]
    name = data.iloc[crew_index]['name']
    profile_path = data.iloc[crew_index]['profile_path']
    return name, profile_path


def fetch_cast(movie):
    url = "https://api.themoviedb.org/3/movie/{}/credits?api_key=f0c86086f96e336c33b3090ec586ea8c&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    data = data['cast'][0:5]
    data = pd.DataFrame(data)
    name = data['name']
    profile_pic = data['profile_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + profile_pic
    return name, full_path


def get_videos(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}/videos?api_key=f0c86086f96e336c33b3090ec586ea8c&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    data = data['results']
    data = pd.DataFrame(data)
    key = data.loc[data['type'] == 'Trailer']
    key = pd.DataFrame(key)
    return key['key'].iloc[0]


def fetch_overview(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=f0c86086f96e336c33b3090ec586ea8c&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    overview = data['overview']
    return overview


def fetch_genres(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=f0c86086f96e336c33b3090ec586ea8c&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    data = data['genres']
    data = pd.DataFrame(data)
    genres = data['name']
    return genres


def fetch_poster(movie_id):
    # print(movie_id)
    url = "https://api.themoviedb.org/3/movie/{}?api_key=f0c86086f96e336c33b3090ec586ea8c&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    # print(movie_index)
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)),
                        reverse=True, key=lambda x: x[1])[1:6]
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in movie_list:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        # print(movie_id)
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters


# Load Machine Learning Model here:
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)


similarity = pickle.load(open('similarity.pkl', 'rb'))


# Main Layout - UI Interface
st.header('Movie Recommender System')
st.text("Hope you find good movies")


movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)


if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(
        selected_movie)
    
    #  Movie Details

    st.subheader(selected_movie)

    movie_index = movies[movies['title'] == selected_movie].index[0]
    movie_id = movies.loc[movie_index].movie_id
    

    cast_name_list, profile_path_list = fetch_cast(movie_id)

    poster, details = st.columns(2)
    with poster:
        st.image(fetch_poster(movie_id), caption='{}'.format(selected_movie))

        # cast Details

    with details:
        st.subheader('Overview')
        st.markdown(fetch_overview(movie_id))
        st.markdown('---')
        st.subheader('Genres')
        for i in fetch_genres(movie_id):
            st.text(i)
    # Cast
    cast1, cast2, cast3, cast4, cast5 = st.columns(5)
    with cast1:
        st.image(profile_path_list[0])
        st.text(cast_name_list[0])
    with cast2:
        st.image(profile_path_list[1])
        st.text(cast_name_list[1])
    with cast3:
        st.image(profile_path_list[2])
        st.text(cast_name_list[2])
    with cast4:
        st.image(profile_path_list[3])
        st.text(cast_name_list[3])
    with cast5:
        st.image(profile_path_list[4])
        st.text(cast_name_list[4])

    # Director
    st.subheader('Director')
    director_name, director_pic = fetch_director(movie_id)
    crew1, crew2 = st.columns(2)
    with crew1:
        st.image("https://image.tmdb.org/t/p/original/" + director_pic)
        st.text(director_name)

    st.markdown('---')
    
    # Recommendation 
    st.subheader('Recommended Movies')

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])

    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
