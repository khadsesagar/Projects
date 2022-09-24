import streamlit as st
import pickle
import pandas as pd
import random
import requests
import numpy as np


from sklearn.metrics.pairwise import cosine_similarity
prev = []
st.set_page_config(page_title=None, page_icon=None, layout="centered", initial_sidebar_state="auto", menu_items=None)


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data_json = data.json()
    path = data_json.get("poster_path")
    full_path = "https://image.tmdb.org/t/p/w500/" + str(path)
    return full_path

#__-------------------------------------------------------------------------
h=[]
def userdefine(rate,movie_user):
    movie_users = movie_user.append(rate, ignore_index=True)
    movie_users[np.isnan(movie_users)] = 0
    user_sim = cosine_similarity(movie_users)
    user_sim1 = pd.DataFrame(user_sim)
    sim_scores = list(enumerate(user_sim1.iloc[-1]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]
    user_ids = [i[0] for i in sim_scores]
    for i in user_ids:
        p = final['title'][final['rating'] == 5][final['userid'] == i].tolist()
        h.extend(p)
    s = list(set(h))
    l = random.sample(s, 5)

    ab = finalWithLink[['title', 'tmdbId']].loc[finalWithLink['title'].isin(l)]

    title_list = ab["title"].unique()
    # bc=link[link['movieId'].isin(id_list)]
    id_listtmdb = ab["tmdbId"].unique()
    recommended_movie_posters = []
    for k in id_listtmdb:
        recommended_movie_posters.append(fetch_poster(int(k)))
    return title_list.tolist(), recommended_movie_posters


#movie5 = pickle.load(open('mvp.pkl','rb'))
#movie5 = pd.DataFrame(movie5)

movie_user = pickle.load(open('movie_user.pkl','rb'))
movie_user = pd.DataFrame(movie_user)

rating5 = pickle.load(open('rating.pkl','rb'))
rating5 = pd.DataFrame(rating5)

#movies = pickle.load(open('moviess.pkl','rb'))
#movies = pd.DataFrame(movies)

cosine_sim = pickle.load(open('cosine_sim.pkl','rb'))
cosine_sim = pd.DataFrame(cosine_sim)

indices = pickle.load(open('indices.pkl','rb'))

final = pickle.load(open('final.pkl','rb'))

finalWithLink = pickle.load(open('finalWithLink.pkl','rb'))



df_titles = pickle.load(open('dist_movie.pkl','rb'))
df_titles = pd.DataFrame(df_titles)

st.title('Movie Recommendation System')

#title = st.selectbox('select movie', df_titles)

forestgump = st.selectbox('select rating Father of the Bride Part II (1995)', rating5)


father = st.selectbox('Select Rating for  Muppet Treasure Island (1996)', rating5)

chase = st.selectbox('Select Rating for Catwalk (1996)', rating5)

toystory = st.selectbox('Select Rating for Braveheart (1995)', rating5)

harry = st.selectbox('Select Rating for Jumanji (1995)', rating5)

rate={" Father of the Bride Part II (1995)":forestgump," Muppet Treasure Island (1996)":father,"Catwalk (1996)":chase,"Braveheart (1995) ":toystory,"Jumanji (1995)":harry}


if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = userdefine(rate, movie_user)
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
    prev.append(recommended_movie_names)
