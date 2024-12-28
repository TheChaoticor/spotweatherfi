import streamlit as st
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os
import random  

load_dotenv()


WEATHERAPI_KEY = os.getenv("WEATHERAPI_KEY")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")


def get_weather(city, api_key):
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no"
    response = requests.get(url)
    return response.json()


def get_songs(mood, client_id, client_secret):
    auth_manager = SpotifyClientCredentials(client_id, client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    results = sp.search(q=mood, type='playlist', limit=5)
    

    if 'playlists' in results and results['playlists']['items']:
    
        random_playlist = random.choice(results['playlists']['items'])
        playlist_id = random_playlist['id']
        playlist_url = random_playlist['external_urls']['spotify']
        playlist_tracks = sp.playlist_tracks(playlist_id)
        track_names = [track['track']['name'] for track in playlist_tracks['items']]
        return track_names, playlist_url
    else:
        return None, None



weather_to_mood = {
    "Sunny": "happy vibes",
    "Clear": "uplifting tunes",
    "Cloudy": "chill beats",
    "Partly cloudy": "relaxing tracks",
    "Rain": "rainy-day vibes",
    "Light rain": "soothing rain sounds",
    "Drizzle": "calm and peaceful",
    "Thunderstorm": "moody tones",
    "Snow": "cozy winter tunes",
    "Overcast": "reflective music",
    "Mist": "mysterious vibes",
    "Fog": "ambient sounds",
    "Haze": "relaxing melodies",
    "Windy": "chill and breezy tracks",
    "Blizzard": "intense winter storm vibes",
    "Sleet": "wintery mix tunes",
    "Showers": "refreshing beats",
    "Heavy rain": "deep rainy vibes",
    "Light snow": "gentle snowfall vibes",
    "Partly cloudy with rain": "soft rain music",
    "Cloudy with rain": "melancholic rainy-day vibes",
    "Light snow": "peaceful snowfall music",
    "Clear sky": "bright morning tunes",
    "Scattered clouds": "gentle cloud music",
    "Fair": "easy listening vibes",
}


def main():
    st.title("Weather-Based Music Playlist 🎵")
    st.write("Enter your location to generate a playlist suitable for the current weather.")


    city = st.text_input("Enter your city:", "New York")

    spotify_client_id = SPOTIFY_CLIENT_ID
    spotify_client_secret = SPOTIFY_CLIENT_SECRET


    if st.button("Generate Playlist"):
        weather_api_key = WEATHERAPI_KEY  

        weather_data = get_weather(city, weather_api_key)
        if "current" in weather_data:
            condition = weather_data["current"]["condition"]["text"]
            temp = weather_data["current"]["temp_c"]

            st.write(f"**Weather:** {condition}")
            st.write(f"**Temperature:** {temp}°C")

    
            mood = weather_to_mood.get(condition, "relaxing music") 
            st.write(f"**Suggested Mood:** {mood}")

    
            st.session_state.mood = mood

        
            playlist, playlist_url = get_songs(mood, spotify_client_id, spotify_client_secret)

            st.session_state.playlist = playlist
            st.session_state.playlist_url = playlist_url
            
            if playlist:
                st.write("### Generated Playlist:")
               

   
                st.markdown(f"[Listen to the full playlist on Spotify]({playlist_url})")

     
                st.markdown(f'<iframe src="https://open.spotify.com/embed/playlist/{playlist_url.split("/")[-1]}" width="300" height="380" frameBorder="0" allowtransparency="true" allow="encrypted-media"></iframe>', unsafe_allow_html=True)
                
            else:
                st.write("No playlists found for the mood. Please try again with a different mood or weather condition.")


    if st.button("Regenerate Playlist") and 'mood' in st.session_state:
        st.write("Generating a new playlist...")


        new_playlist, new_playlist_url = get_songs(st.session_state.mood, spotify_client_id, spotify_client_secret)
        

        st.session_state.playlist = new_playlist
        st.session_state.playlist_url = new_playlist_url

        if new_playlist:
            st.write("### New Playlist:")
           

           
            st.markdown(f"[Listen to the full playlist on Spotify]({new_playlist_url})")
            st.markdown(f'<iframe src="https://open.spotify.com/embed/playlist/{new_playlist_url.split("/")[-1]}" width="300" height="380" frameBorder="0" allowtransparency="true" allow="encrypted-media"></iframe>', unsafe_allow_html=True)
        else:
            st.write("No playlists found for the mood. Please try again.")

if __name__ == "__main__":
    main()
