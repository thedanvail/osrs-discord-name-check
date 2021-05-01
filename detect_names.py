import requests


def get_score(player_name: str):
    hs_api = 'https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player='

    response = requests.get(f'{hs_api}{player_name}')

    ## 200 is the response for an existing player
    ## 404 is no response / missing

    if response.status_code == 404:
        print(response.status_code)
        return None

    elif response.status_code == 200:
        print(response.content)
        return response.content

    # if high scores are down, or something else, ignore for now
    else:
        print(response.status_code)
        return None


def exists_player(player_name: str, ignore_char = "|") -> bool:

    if player_name is None:
        return False

    player_name = player_name.split(ignore_char)[0]

    print(player_name)
    score = get_score(player_name)

    ## 200 is the response for an existing player
    ## 404 is no response / missing

    if score:
        return True

    ## For future:
    # log response code
    # log scores

    return False

