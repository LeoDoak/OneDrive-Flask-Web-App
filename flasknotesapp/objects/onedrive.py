""" Module relating to groups and such  """

import webbrowser
from datetime import datetime
import json
import os
import msal

# user_code = "placement_code"

GRAPH_API_ENDPOINT = 'https://graph.microsoft.com/v1.0/'


def generate_access_token(app_id, scopes):
    """Summary or Description of the function

    Parameters: app id token to use onedrive, scopes: permissions onedrive grants the application,
    in this case read/write files
    Returns: access token to access onedrive account
    """

    # Save Session Token as a token file
    access_token_cache = msal.SerializableTokenCache()

    # read the token file
    if os.path.exists('ms_graph_api_token.json'):
        with open("ms_graph_api_token.json", "r", encoding='utf-8') as file:
            access_token_cache.deserialize(file.read())
        with open("ms_graph_api_token.json", "r", encoding='utf-8') as file:
            token_detail = json.load(file)
        token_detail_key = list(token_detail['AccessToken'].keys())[0]
        token_expiration = datetime.fromtimestamp(
            int(token_detail['AccessToken'][token_detail_key]['expires_on']))
        if datetime.now() > token_expiration:
            os.remove('ms_graph_api_token.json')
            access_token_cache = msal.SerializableTokenCache()

    # assign a SerializableTokenCache object to the client instance
    client = msal.PublicClientApplication(
        client_id=app_id, token_cache=access_token_cache)

    accounts = client.get_accounts()
    if accounts:
        # load the session
        token_response = client.acquire_token_silent(scopes, accounts[0])
    else:
        # authetnicate your accoutn as usual
        flow = client.initiate_device_flow(scopes=scopes)
        user_code = flow['user_code']
        print('user_code: ' + user_code)
        webbrowser.open('https://microsoft.com/devicelogin')
        display_popup(user_code)
        token_response = client.acquire_token_by_device_flow(flow)

    with open('ms_graph_api_token.json', 'w', encoding='utf-8') as _f:
        _f.write(access_token_cache.serialize())

    return token_response


def display_popup(user_code):
    """Summary or Description of the function
        opens up a new webpage with the user code
    Parameters: user code
    """
    html_content = f"""
    <html>
    <head>
    <title>User Code</title>
    <style>
    body {{
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 20px;
        text-align: center;
    }}
    .popup {{
        width: 300px;
        height: 200px;
        margin: auto;
        background-color: #f9f9f9;
        border: 1px solid #ccc;
        border-radius: 5px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        padding: 20px;
    }}
    </style>
    </head>
    <body>
    <div class="popup">
    <h1>User Code</h1>
    <p>{user_code}</p>
    <button onclick="window.close()">Close</button>
    </div>
    <script>
    window.moveTo(((window.screen.width - window.outerWidth) / 2) - 150,
    ((window.screen.height - window.outerHeight) / 2) - 100);
    </script>
    </body>
    </html>
    """

    with open('popup.html', 'w', encoding='utf-8') as file:
        file.write(html_content)

    # chat gpt helped with this
    current_directory = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to popup.html
    html_file_path = os.path.join(current_directory, '..', 'popup.html')
    # Convert the file path to a URL using the file:// protocol
    html_url = 'file://' + html_file_path
    print(html_url)
    # Open the HTML file in the default web browser
    webbrowser.open(html_url)


if __name__ == '__main__':
    ...

# #pip install msal
# #video https://www.youtube.com/watch?v=1Jyd7SA-0kI&t=141s
# #possible https://www.youtube.com/watch?v=oW1SJxGiaZA
# import webbrowser
# import requests
# from msal import PublicClientApplication

# APPLICATION_ID = '5e84b5a7-fd04-4398-a15f-377e3d85703e'
# CLIENT_SECRET = 'ZyD8Q~cyR5CAFFQat2ZvtTcnUJB3BJmCPj2FbdoR'
# authority_url = 'https://login.microsoftonline.com/consumers/'

# base_url = 'https://graph.microsoft.com/v1.0/'
# endpoint = base_url + 'me'

# SCOPES = ['User.Read']

# app = PublicClientApplication(
#     APPLICATION_ID,
#     authority=authority_url
# )

# # accounts = app.get_accounts()
# # if accounts:
# #     app.acquire_token_silent(scopes=SCOPES, account=accounts[0])

# flow = app.initiate_device_flow(scopes=SCOPES)
# print(flow)
# print(flow['message'])
# webbrowser.open(flow['verification_uri'])

# result = app.acquire_token_by_device_flow(flow)
# access_token_id = result['access_token']
# headers = {'Authorization': 'Bearer ' + access_token_id}

# endpoint = base_url + 'me'
# response = requests.get(endpoint, headers=headers)
# print(response)
# print(response.json())
