# KKBOX OpenAPI SDK for Python

The SDK is for accessing various metadata of KKKBOX tracks, albums, artist, playlists and stations.

## Installation

Use `[sudo] python setup.py install` to install the package.

The package works with Python 2 and Python 3.

## Test

First, browse [KKBOX Developer Website](https://kkbox.gelato.io/) and create an developer account, and then contact chrisyuan or lance to get client secret for that account.

Then, open `client.py` in the `test` directory and put your client id and client secret in it.

	client_id = "YOUR_CLIENT_ID"
	client_secret = "YOUR_CLIENT_SECRET"
	auth_code = "YOUR_AUTH_CODE"

And then run the test `authTest.py`. If the running success, it will return you an URL.

Browse your URL and log in KKBOX, then you can obtain your auth code.

    http://localhost/?code=_YOUR_AUTH_CODE_&state=1234

Follow the steps as client id and client secret, put your auth code in `client.py`.

## How to use the SDK

After obtaining a valid access token, you may call APIs like this:

	artist_id = '8q3_xzjl89Yakn_7GB'
	artist = sdk.fetch_artist(artist_id)

For further information, please visit [API Documentation](https://docs.kkbox.codes).
