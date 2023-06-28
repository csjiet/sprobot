import requests
import os
import json
from functools import partial

def create_url():
    return "https://api.twitter.com/2/tweets/sample/stream"


def bearer_oauth(r, bearer_token = ""):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2SampledStreamPython"
    return r


def connect_to_endpoint(url, bearer_token = ""):

    bearer_func = partial(bearer_oauth, bearer_token=bearer_token)

    response = requests.request("GET", url, auth= bearer_func, stream=True)
    print(response.status_code)
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            print(json.dumps(json_response, indent=4, sort_keys=True))
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )


def main(bearer_token = ""):
    url = create_url()
    timeout = 0
    while True:
        connect_to_endpoint(url, bearer_token = bearer_token)
        timeout += 1


if __name__ == "__main__":
    pass