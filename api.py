import requests
import settings


def response(success, message):
    return {
    "success": success,
    "message": message
    }


def user_request(username):
    params = {
            "username": username,
            "authorization": settings.API_AUTH
            }

    url = settings.API_URL + "/user"

    return __get(params, url)


def challenge_request():
    params = {
            "authorization" : settings.API_AUTH
            }

    url = settings.API_URL + "/weekly_challenge"

    return __get(params, url)


def __get(url, params):
    try:
        r = requests.get(url, params)
        if r.ok:
            return response(true, r.json())
        elif r.status_code == 404:
            return response(false, "Request failed. Its likely the account is not registered at r6.leaderboards.io")
        else:
            return response(false, f"Stat request failed. Status code {r.status_code}")
    except ConnectionError as ex:
        return response(false, f"There was a connection error. Message: {ex.message}")
    except Timeout as ex:
        return response(false, f"The request timed out. Message {ex.message}")

