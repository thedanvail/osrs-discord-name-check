import requests


def exists_player(player_name: str) -> bool:

    if player_name is None:
        return False

    print(player_name)
    hs_api = 'https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player='

    response = requests.get(f'{hs_api}{player_name}')

    ## 200 is the response for an existing player
    ## 404 is no response / missing

    if response.status_code == 404:
        print(response.status_code)
        return False

    elif response.status_code == 200:
        print(response.content)
        return True

    # if high scores are down, or something else, ignore for now
    else:
        print(response.status_code)
        return True

    ## For future:
    # log response code
    # log scores

    return False

