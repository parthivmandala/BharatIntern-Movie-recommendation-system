import streamlit as st
import pickle
import requests

# Function to fetch the movie poster using the TMDb API
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raises an exception for HTTP errors
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
            return full_path
        else:
            return None
    except requests.exceptions.Timeout:
        st.error("The request timed out. Please try again later.")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")
        return None

# Load the movies and similarity data
movies = pickle.load(open("bharatIntern-movieRecommendationSystem-main/movies_list.pkl", 'rb'))
similarity = pickle.load(open("bharatIntern-movieRecommendationSystem-main/similarity.pkl", 'rb'))
movies_list = movies['title'].values

st.header("Movie Recommendation System")

# Create a dropdown to select a movie
selected_movie = st.selectbox("Select a movie:", movies_list)

# Function to recommend movies based on the selected movie
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    recommended_posters = []
    for i in distances[1:6]:  # Skip the first movie as it's the selected movie
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        poster_url = fetch_poster(movie_id)
        if poster_url:
            recommended_posters.append(poster_url)
        else:
            recommended_posters.append("")  # Use an empty string if poster URL is not available
    return recommended_movies, recommended_posters

if st.button("Recommend"):
    recommended_movies, recommended_posters = recommend(selected_movie)
    
    # Display the recommended movies and their posters
    columns = st.columns(5)
    for i in range(5):
        with columns[i]:
            st.text(recommended_movies[i])
            if recommended_posters[i]:
                st.image(recommended_posters[i])
            else:
                st.text("Poster not available")
