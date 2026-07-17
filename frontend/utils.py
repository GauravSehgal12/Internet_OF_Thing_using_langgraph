import requests

BASE_URL = "http://127.0.0.1:8000"


def send_command(command):

    response = requests.post(

        f"{BASE_URL}/invoke",

        json={"command": command}

    )

    return response.json()


def get_devices():

    response = requests.get(

        f"{BASE_URL}/devices"

    )

    return response.json()


def reset_home():

    requests.post(

        f"{BASE_URL}/reset"

    )