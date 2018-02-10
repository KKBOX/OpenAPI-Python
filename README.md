# KKBOX OpenAPI SDK for Python

[![License Apache 2.0](https://img.shields.io/badge/license-Apache-green.svg?style=flat)](https://raw.githubusercontent.com/KKBOX/OpenAPI-Python/master/LICENSE.txt)
[![pypi](https://img.shields.io/pypi/v/kkbox-developer-sdk/.svg)](https://pypi.python.org/pypi/kkbox-developer-sdk/)
[![pypi](https://img.shields.io/pypi/dm/kkbox-developer-sdk/.svg)](https://pypi.python.org/pypi/kkbox-developer-sdk/)


The SDK helps accessing various metadata such as KKBOX tracks, albums, artists, playlists and stations.

### Installation

Source installation

    [sudo] python setup.py install

Pypi installation

    pip install kkbox-developer-sdk

The package works with both Python 2 and Python 3.

### Running Tests

Test cases are placed in the `test` folder. To run the tests, first, please visit https://developer.kkbox.com/ to obtain a valid client ID and client secret.

Second, create `client.py` in the `test` directory which contains a class named ClientInfo, and put your client id and client secret in it. It will looks like:

    class ClientInfo():
	    client_id = "YOUR_CLIENT_ID"
	    client_secret = "YOUR_CLIENT_SECRET"

Then we can run the tests.

## Usage

To access all of the KKBOX's APIs, we have to obtain an access token at first.

	from kkbox_developer_sdk.auth_flow import KKBOXOAuth
	auth = KKBOXOAuth(CLIENT_ID, CLIENT_SECRET)
	token = auth.fetch_access_token_by_client_credentials()

Once the access token is obtained, we may call APIs like this:

	from kkbox_developer_sdk.api import KKBOXAPI
	kkboxapi = KKBOXAPI(token)
	artist_id = '8q3_xzjl89Yakn_7GB'
	artist = kkboxapi.artist_fetcher.fetch_artist(artist_id)

### Documentation

Documentation of the SDK is available at https://kkbox.github.io/OpenAPI-Python/ .

To get started, visit [Beginner's Guide for Python Developers](https://docs-en.kkbox.codes/docs/beginners-guide-for-python-developers).

## Documentation Generation

We use Sphinx, recommonmark and sphinx-rtd-theme to build the documentation of the SDK. Thus, you need to install these tools by the following command.

	pip install Sphinx recommonmark sphinx-rtd-theme

Then you can generate documentation using sphinx:

	sphinx-apidoc -o doc -f kkbox_developer_sdk
	cd doc
	make html

### API Documentation

KKBOX's Open API documentation is available at https://developer.kkbox.com/.

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
