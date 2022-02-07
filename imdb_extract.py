# -*- coding: utf-8 -*-
import json
import requests as re
import sqlite3
import pandas as pd

#simple func just to filter keys i want in the final dict
def only_keys(d, keys):
     return {x: d[x] for x in d if x in keys}


#extracts all info about series episodes
def episodes(imdb_code):
    with sqlite3.connect('series_info.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM series_info WHERE imdb_code=?', (imdb_code,))
        row = cursor.fetchall()

        desired_keys = [
            'episodeNumber', 'title', 'released', 'imDbRating'
        ]

        for i in range(row[0][3]+1):
            ep_request = re.get('https://imdb-api.com/en/API/SeasonEpisodes/k_a7dsw5s1/'+ imdb_code +'/' + str(i))
            ep_json = json.loads(ep_request.text)
            eps = [only_keys(ep, desired_keys) for ep in ep_json['episodes']]

            for ep in eps:
                res = cursor.execute(
                    """INSERT INTO episodes (series_name, season, ep_number, ep_name, rating, release_date) VALUES (?,?,?,?,?,?)""",
                    (
                        row[0][2], i, ep['episodeNumber'], ep['title'], ep['imDbRating'], ep['released']
                    )
                )
    return


#with specific code this func inserts in database general info about series
def series_info(imdb_code):
    desired_keys = [
        'id', 'title', 'year', 'plot', 'stars', 'genres', 'imDbRating', 'imDbRatingVotes',
        'tvSeriesInfo'
    ]

    request_result = re.get('https://imdb-api.com/en/API/Title/k_a7dsw5s1/' + imdb_code)
    full_json = json.loads(request_result.text)
    info = only_keys(full_json, desired_keys)

    with sqlite3.connect('series_info.db') as conn:
        cursor = conn.cursor()
        res = cursor.execute(
            """INSERT INTO series_info (imdb_code, series_name, seasons, imdb_rating, rating_votes, year_released, year_ended, genres, stars, plot) VALUES (?,?,?,?,?,?,?,?,?,?)""",
            (
                info['id'], info['title'], len(info['tvSeriesInfo']['seasons']),
                info['imDbRating'], info['imDbRatingVotes'], info['year'],
                info['tvSeriesInfo']['yearEnd'], info['genres'], info['stars'],
                info['plot']
            )
        )
    return


#function that searches given name and return imdbs matching options
def search_series(name):
    request_result = re.get('https://imdb-api.com/en/API/SearchSeries/k_a7dsw5s1/' + name)
    matches = json.loads(request_result.text)

    options = []
    for match in matches['results']:
        name = match['title']
        name += ' ' + match['description'].split()[0]
        options.append((name, match['id']))

    return options


def main():
    # print(search_series('supernatural'))
    # print(series_info('tt0460681'))
    episodes('tt0460681')
    return

if __name__ == '__main__':
    main()
