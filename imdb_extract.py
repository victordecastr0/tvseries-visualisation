import json
import requests as re

def only_keys(d, keys):
     return {x: d[x] for x in d if x in keys}

def episodes(infos):
    eps = {}
    desired_keys = [
        'episodeNumber', 'title', 'released', 'imDbRating'
    ]

    for i in range(1, len(infos['tvSeriesInfo']['seasons'])+1):
        ep_request = re.get('https://imdb-api.com/en/API/SeasonEpisodes/k_a7dsw5s1/tt0460681/' + str(i))
        ep_json = json.loads(ep_request.text)
        ep = [only_keys(ep, desired_keys) for ep in ep_json['episodes']]
        eps['season ' + str(i)] = ep

    return eps

def series_info(imdb_code):
    desired_keys = [
        'id', 'title', 'year', 'plot', 'stars', 'genres', 'imDbRating', 'imDbRatingVotes',
        'tvSeriesInfo', 'seasons'
    ]

    request_result = re.get('https://imdb-api.com/en/API/Title/k_a7dsw5s1/' + imdb_code)
    full_json = json.loads(request_result.text)

    info = only_keys(full_json, desired_keys)
    return info

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
    print(search_series('supernatural'))
    print(episodes(series_info('tt0460681')))
    return

if __name__ == '__main__':
    main()
