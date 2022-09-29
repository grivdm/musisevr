import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys
import cred
import ast
from yandex_music import Client
from ytmusicapi import YTMusic as ytm
import re


sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=cred.client_id, client_secret=cred.client_secret))


# Input

def input_request(text_search):           # in-data from user
    if re.match(r'http', text_search):           # Links handling part starts here
        if re.search(r'spotify', text_search):           # Spotify links part
            if re.search(r'artist', text_search):           # Artist link
                input_artist_name = sp.artist(text_search)
                input_artist_name = input_artist_name['name']
                input_track_name = None
            else:
                search_track_result = sp.track(text_search)           # Track link
                try:
                    array_from_spotify = search_track_result['artists']
                    convert_result = ast.literal_eval(''.join(str(x) for x in array_from_spotify))
                    input_artist_name = convert_result['name']
                    input_track_name = search_track_result['name']
                except SyntaxError:
                    array_from_spotify = search_track_result['artists'][0]
                    input_artist_name = array_from_spotify['name']
                    input_track_name = search_track_result['name']
            return input_artist_name, input_track_name

        elif re.search(r'yandex', text_search):         # Yandex link part
            if re.search(r'artist', text_search):           # Artist link
                link_id = re.findall(r'[0-9]+', text_search)
                artist_id = link_id[0]
                search_result_hash = Client().artists(artist_id)
                input_artist_name = search_result_hash[0]['name']
                input_track_name = None
                return input_artist_name, input_track_name
            else:
                link_id = re.findall(r'[0-9]+', text_search)            # Track link
                if re.search(r'album', text_search):
                    search_result_hash = Client().tracks(link_id[1])
                    input_artist_name = search_result_hash[0]['artists'][0]['name']
                    input_track_name = search_result_hash[0]['title']
                else:
                    search_result_hash = Client().tracks(link_id[0])
                    input_artist_name = search_result_hash[0]['artists'][0]['name']
                    input_track_name = search_result_hash[0]['title']
                return input_artist_name, input_track_name
    else:
        if len(text_search) > 0:            # Text handling part
            input_text_list = text_search.split('-')
            input_artist_name = input_text_list[0]
            if len(input_text_list) >= 2:
                input_track_name = input_text_list[1]
            else:
                input_track_name = None
            return input_artist_name, input_track_name
        else:
            pass


# Spotify

def get_data_spotify(artist, track):
    if len(sys.argv) > 1:
        artist_name = ' '.join(sys.argv[1:])
    else:
        artist_name = artist
    try:
        search_result_hash = sp.search(q="artist:" + artist_name + " track:" + track, limit=1, type="track")
        result_items = search_result_hash['tracks']['items']
    except TypeError:
        search_result_hash = sp.search(q="artist:" + artist_name, limit=1, type="artist")
        result_items = search_result_hash['artists']['items']
    for value in result_items:
        spotify_results = dict()
        spotify_results['urls'], spotify_results['artName'] = value['external_urls'], value['name']
        return spotify_results


# Yandex music

def get_data_yandex(artist, track):
    try:
        if track is not None:
            search_result_hash = Client().search("artist: " + artist + " track: " + track)
            track_id = search_result_hash.best['result']['id']
            album_id_convert = ast.literal_eval(''.join(str(x) for x in search_result_hash.best['result']['albums']))
            album_id = album_id_convert['id_']
            return f'https://music.yandex.ru/album/{album_id}/track/{track_id}'
        else:
            search_result_hash = Client().search("artist: " + artist)
            artist_id = search_result_hash.best['result']['id']
            return f'https://music.yandex.ru/artist/{artist_id}'
    except:
        return None


# Youtube music

def get_data_youtube(artist, track):
    try:
        if track is not None:
            search_result_hash = ytm().search("artist:" + artist + " track:" + track)
            result_id = search_result_hash[0]['videoId']
            return f'https://youtu.be/{result_id}'
        else:
            search_result_hash = ytm().search(artist)
            result_id = search_result_hash[0]['browseId']
            return f'https://music.youtube.com/channel/{result_id}'
    except:
        return None


# Output

def get_output(text):
    artist, track = input_request(text)
    print(artist, track)
    output_spotify = get_data_spotify(artist, track)
    output_yandex = get_data_yandex(artist, track)
    output_youtube = get_data_youtube(artist, track)
    return output_spotify, output_yandex, output_youtube
