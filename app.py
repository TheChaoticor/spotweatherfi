import streamlit as st
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# WeatherAPI function to fetch weather data
def get_weather(city, api_key):
    url = f"http://api.weatherapi.com/v1/current.json?key={"715c0cf517b04c0087c105026242308"}&q={city}&aqi=no"
    response = requests.get(url)
    return response.json()

# Spotify function to fetch songs based on mood
def get_songs(mood, client_id, client_secret):
    auth_manager = SpotifyClientCredentials(client_id, client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    results = sp.search(q=mood, type='playlist', limit=1)
    playlist_id = results['playlists']['items'][0]['id']
    playlist_tracks = sp.playlist_tracks(playlist_id)
    return [track['track']['name'] for track in playlist_tracks['items']]

# Map weather conditions to moods
weather_to_mood = {
    "Sunny": "happy vibes",
    "Clear": "uplifting tunes",
    "Cloudy": "chill beats",
    "Partly cloudy": "relaxing tracks",
    "Rain": "rainy-day vibes",
    "Thunderstorm": "moody tones",
    "Snow": "cozy winter tunes",
    "Overcast": "reflective music",
}

# Streamlit app interface
def main():
    st.title("Weather-Based Music Playlist 🎵")
    st.write("Enter your location to generate a playlist suitable for the current weather.")

    # Input for city
    city = st.text_input("Enter your city:", "New York")

    # Generate playlist button
    if st.button("Generate Playlist"):
        weather_api_key = "715c0cf517b04c0087c105026242308"  # Replace with your WeatherAPI key
        spotify_client_id = "a7eaf07405994dd9a364580ba3454520"  # Replace with your Spotify client ID
        spotify_client_secret = "3a56c32ef4be4a09bfd49f2ad4c84042"  # Replace with your Spotify client secret

        # Fetch weather data
        weather_data = get_weather(city, weather_api_key)
        if "current" in weather_data:
            condition = weather_data["current"]["condition"]["text"]
            temp = weather_data["current"]["temp_c"]

            st.write(f"**Weather:** {condition}")
            st.write(f"**Temperature:** {temp}°C")

            # Determine mood and fetch songs
            mood = weather_to_mood.get(condition, "relaxing music")
            st.write(f"**Suggested Mood:** {mood}")

            playlist = get_songs(mood, spotify_client_id, spotify_client_secret)
            st.write("### Generated Playlist:")
            for i, song in enumerate(playlist, 1):
                st.write(f"{i}. {song}")

            # Regenerate option
            if st.button("Regenerate Playlist"):
                st.write("Generating a new playlist...")
                playlist = get_songs(mood, spotify_client_id, spotify_client_secret)
                st.write("### New Playlist:")
                for i, song in enumerate(playlist, 1):
                    st.write(f"{i}. {song}")
        else:
            st.error("Could not fetch weather data. Please try again.")

if __name__ == "__main__":
    main()
