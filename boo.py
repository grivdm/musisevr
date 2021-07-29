import telebot
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys
import cred
import ast
from yandex_music import Client
from ytmusicapi import YTMusic
import re

ytm = YTMusic()
client = Client()
TOKEN = cred.TOKEN
bot = telebot.TeleBot(TOKEN)
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=cred.client_id, client_secret=cred.client_secret))


# spoty

def get_input(textSearch):
    if re.match(r'http', textSearch):
        if re.search(r'spotify', textSearch):
            if re.search(r'artist', textSearch):
                res_art = sp.artist(textSearch)
                artistNm1 = res_art['name']
                trackNm1 = None
            else:
                results = sp.track(textSearch)
                try:
                    res_art1 = results['artists']
                    res_art2 = ast.literal_eval(''.join(str(x) for x in res_art1))
                    artistNm1 = res_art2['name']
                    trackNm1 = results['name']
                except SyntaxError:
                    res_art1 = results['artists'][0]
                    artistNm1 = res_art1['name']
                    trackNm1 = results['name']
            return artistNm1, trackNm1

        elif re.search(r'yandex', textSearch):
            if re.search(r'artist', textSearch):
                ids = re.findall(r'[0-9]+', textSearch)
                idartist = ids[0]
                search_result = client.artists(idartist)
                res_art = search_result[0]['name']
                res_track = None
                return res_art, res_track
            else:
                ids = re.findall(r'[0-9]+', textSearch)
                if re.search(r'album', textSearch):
                    search_result = client.tracks(ids[1])
                    res_art = search_result[0]['artists'][0]['name']
                    res_track = search_result[0]['title']
                else:
                    search_result = client.tracks(ids[0])
                    res_art = search_result[0]['artists'][0]['name']
                    res_track = search_result[0]['title']
                return res_art, res_track
    else:
        if len(textSearch) > 0:
            inreq = textSearch.split('-')
            artistNm1 = inreq[0]
            if len(inreq) >= 2:
                trackNm1 = inreq[1]
            else:
                trackNm1 = None
            return artistNm1, trackNm1
        else:
            print('none')


def get_trackSpoty(artist, track):
    if len(sys.argv) > 1:
        name = ' '.join(sys.argv[1:])
    else:
        name = artist
    try:
        resultsa = sp.search(q="artist:" + name + " track:" + track, limit=1, type="track")
        itemsa = resultsa['tracks']['items']
    except TypeError:
        resultsa = sp.search(q="artist:" + name, limit=1, type="artist")
        itemsa = resultsa['artists']['items']
    for i_ar in itemsa:
        dict_art = dict()
        dict_art['urls'], dict_art['artName'] = i_ar['external_urls'], i_ar['name']
        return dict_art


# Ya.Muz

def get_trackYa(artist, track):
    try:
        if track is not None:
            search_result = client.search("artist: " + artist + " track: " + track)
            track_id = search_result.best['result']['id']
            album_id00 = ast.literal_eval(''.join(str(x) for x in search_result.best['result']['albums']))
            album_id = album_id00['id_']
            return f'https://music.yandex.ru/album/{album_id}/track/{track_id}'
        else:
            search_result = client.search("artist: " + artist)
            artist_id = search_result.best['result']['id']
            return f'https://music.yandex.ru/artist/{artist_id}'
    except:
        return None


# ytmusic

def ytMus(artist, track):
    try:
        if track is not None:
            search = ytm.search("artist:" + artist + " track:" + track)
            ss = search[0]['videoId']
            return f'https://youtu.be/{ss}'
        else:
            search = ytm.search(artist)
            ss = search[0]['browseId']
            return f'https://music.youtube.com/channel/{ss}'
    except:
        return None


def get_output(text):
    artist, track = get_input(text)
    print(artist, track)
    out_S = get_trackSpoty(artist, track)
    out_Y = get_trackYa(artist, track)
    out_ytm = ytMus(artist, track)
    return out_S, out_Y, out_ytm


# telegram

@bot.message_handler(commands=['start'])
def welcome_start(message):
    bot.send_message(message.chat.id, 'Приветствую тебя, {username}. \n'
                                      '\nТут всё просто, напиши в чате:'
                                      '\nИмя исполнителя - Название песни '
                                      '\nили \nИмя исполнителя.'
                                      '\nМожешь скинуть ссылку на исполнителя или песню.'
                                      '\nРаботаю с сервисами  Spotify & YaMusic. '
                                      '\nВперед!'.format(username=message.from_user.first_name))


@bot.message_handler(content_types=["text"])
def get_msg(message):
    spotyRep, yandRep, ytmRep = get_output(message.text)
    markup = telebot.types.InlineKeyboardMarkup()
    try:
        if spotyRep is not None:
            markup.add(telebot.types.InlineKeyboardButton(text='spotify', url=spotyRep['urls']['spotify']))
        if yandRep is not None:
            markup.add(telebot.types.InlineKeyboardButton(text='yandex', url=yandRep))
        bot.send_message(message.chat.id, 'Смотри, что удалось найти: \n' + ytmRep, reply_markup=markup)
    except:
        bot.send_message(message.chat.id, 'К сожалению, ничего не найдено.'
                                          '\nПопробуй ещё раз или почитай /start')


if __name__ == '__main__':
    bot.infinity_polling()
