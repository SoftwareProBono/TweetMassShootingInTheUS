import requests
import os
import json


class Twitter:

    token_file_path = os.getenv('TOKEN_FILE_PATH')

    def __init__(self):
        with open(self.token_file_path, "r") as f:
            self.current_tokens = json.loads(f.read())

    def refresh_tokens(self):
        response = requests.post('https://api.twitter.com/2/oauth2/token', data={
            'refresh_token': self.current_tokens['refresh_token'],
            'grant_type': 'refresh_token',
            'client_id': os.getenv('TWITTER_CLIENT_ID')
        }, headers={
            'Authorization': 'Basic ' + os.getenv('TWITTER_BASIC_AUTH'),
            'Content-Type': 'application/x-www-form-urlencoded'
        })

        print('Refresh request with status code: ' + response.status_code.__str__())
        if 200 <= response.status_code < 300:
            self.current_tokens = response.json()

            with open(self.token_file_path, "w+") as f:
                f.write(json.dumps(self.current_tokens))
        else:
            print('Error: ' + json.dumps(response.json()))

    def tweet(self, message):
        response = requests.post('https://api.twitter.com/2/tweets', json = {
            'text': message
        }, headers={
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.current_tokens['access_token']
        })

        return response