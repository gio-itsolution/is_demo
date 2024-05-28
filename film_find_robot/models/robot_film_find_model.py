import requests

from integration_utils.bitrix_robots.models import BaseRobot


class FilmRobot(BaseRobot):
    CODE = 'film_robot'
    NAME = 'Робот возвращает информацию о фильме'
    USE_SUBSCRIPTION = True

    PROPERTIES = {
        'film_name': {
            'Name': {'ru': 'Название фильма'},
            'Type': 'string',
            'Required': 'Y',
        },
        's_key': {
            'Name': {'ru': 'Ключ sKey'},
            'Type': 'string',
            'Required': 'Y',
        },
    }

    RETURN_PROPERTIES = {
        'film_name': {
            'Name': {'ru': 'Название фильма'},
            'Type': 'string',
            'Required': 'Y',
        },
        'film_rating': {
            'Name': {'ru': 'Рейтинг фильма'},
            'Type': 'double',
            'Required': 'N',
        },
        'year': {
            'Name': {'ru': 'Год выхода'},
            'Type': 'int',
            'Required': 'N',
        },
        'short_description': {
            'Name': {'ru': 'Краткое описание'},
            'Type': 'string',
            'Required': 'N',
        },
        'image_link': {
            'Name': {'ru': 'Ссылка на превью'},
            'Type': 'string',
            'Required': 'N',
        },
        'ok': {
            'Name': {'ru': 'ok'},
            'Type': 'bool',
            'Required': 'Y',
        },
        'error': {
            'Name': {'ru': 'error'},
            'Type': 'string',
            'Required': 'N',
        },
    }

    def process(self) -> dict:
        try:
            method = "v1.4/movie/search"
            BASE_URL = f"https://api.kinopoisk.dev/{method}"
            s_key = self.props['s_key']
            headers = {"X-API-KEY": s_key,
                       'accept': 'application/json'}
            params = {'query': self.props['film_name']}

            response = requests.get(BASE_URL, params=params, headers=headers)
            json_response = response.json()

            film_name = json_response["docs"][0]["name"]
            film_rating = json_response["docs"][0]["rating"]["imdb"]
            year = json_response["docs"][0]["year"]
            short_description = json_response["docs"][0]["shortDescription"]
            image_link = json_response["docs"][0]["poster"]["previewUrl"]


            self.dynamic_token.call_api_method('bizproc.event.send', {"event_token": self.event_token,
                                                                      "return_values": {"film_name": film_name,
                                                                                        "film_rating": film_rating,
                                                                                        "year": year,
                                                                                        "short_description": short_description,
                                                                                        "image_link": image_link,
                                                                                        }})

        except Exception as exc:
            return dict(ok=False, error=str(exc))

        return dict(ok=True)
