# KKBOX OpenAPI SDK for Python

The SDK is for accessing various metadata of KKBOX tracks, albums, artist, playlists and stations.

### Installation
Source installation

    [sudo] python setup.py install

Pypi installation
    
    pip install kkbox-developer-sdk

The package works with Python 2 and Python 3.

### Test

First, go to https://developer.kkbox.com/ to get client id and client secret. If the site is unavailable, you can also contact vincentchiang or chrisyuan at KKBOX to get client id and client secret.

Second, create `client.py` in the `test` directory and create a class named ClientInfo, and put your client id and client secret in it. The content will be like: 

    class ClientInfo():
	    client_id = "YOUR_CLIENT_ID"
	    client_secret = "YOUR_CLIENT_SECRET"

And then we can run the tests.

## How to use the SDK

First we have to obtain the access token.

	from kkbox_developer_sdk.auth_flow import KKBOXOAuth
	auth = KKBOXOAuth(CLIENT_ID, CLIENT_SECRET)
	token = auth.fetch_access_token_by_client_credentials()

After obtaining the access token, you may call APIs like this:

	from kkbox_partner_sdk.api import KKBOXAPI
	kkboxapi = KKBOXAPI(token)
	artist_id = '8q3_xzjl89Yakn_7GB'
	artist = kkboxapi.artist_fetcher.fetch_artist(artist_id)

## Generate the SDK documentation
The SDK documentation depends on Sphinx and recommonmark, so first you have to install them.

	pip install Sphinx recommonmark

Then generate documentation by sphinx:

	sphinx-apidoc -o doc -f kkbox_developer_sdk
	cd doc
	make html
	
### [API Documentation](https://kkbox.gelato.io/)
### License
Copyright 2017 KKBOX Technologies Limited

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
