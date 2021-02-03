import requests


def exists_player(player_name: str) -> bool:
    hs_api = 'https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player='

    response = requests.get(f'{hs_api}{player_name}')

    if response.status_code != 200:
        print(response.status_code)
        return False

    elif response.status_code == 200:
        print(response.content)
        return True

    # log response code

    # log score

    return False

