# KKBOX OpenAPI SDK for Python

The SDK is for accessing various metadata of KKBOX tracks, albums, artist, playlists and stations.

### Installation

    [sudo] python setup.py install

The package works with Python 2 and Python 3.

### Test

First, browse [KKBOX Developer Website](https://kkbox.gelato.io/) and create an developer account, and then contact chrisyuan or lance to get client secret for that account.

Second, create `client.py` in the `test` directory and create a class named ClientInfo, and put your client id and client secret in it. The content will be like: 

    class ClientInfo():
	    client_id = "YOUR_CLIENT_ID"
	    client_secret = "YOUR_CLIENT_SECRET"

And then we can run the tests.

## How to use the SDK

First we have to obtain the access token.

	auth = KKBOXOAuth(CLIENT_ID, CLIENT_SECRET)
	token = auth.fetch_access_token_by_client_credentials()

After obtaining the access token, you may call APIs like this:

	sdk = KKBOXSDK(token)
	artist_id = '8q3_xzjl89Yakn_7GB'
	artist = sdk.artist_fetcher.fetch_artist(artist_id)
	
### [API Documentation](https://docs.kkbox.codes/docs)
