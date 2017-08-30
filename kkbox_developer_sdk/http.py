#!/usr/bin/env python
# encoding: utf-8
try:
    # Python 3
    import urllib.parse as url_parse
    import urllib.request as url_request
    import functools
except:
    # Python 2
    import urllib as url_parse
    import urllib2 as url_request
    import functools
import base64
import json

class KKBOXHTTP:    
    '''
    Do request to open api server with authorization header and error catch.
    '''
    USER_AGENT = 'KKBOX Open/Partner API Python SDK'

    def __init__(self, access_token = None):
        self.access_token = access_token

    def _do_post(self, url, data, headers):
        try:  # Python 3
            if data != None:
                data = bytes(data, 'utf-8')
        except:  # Python 2
            pass

        try:
            req = url_request.Request(url=url, data=data, headers=headers)
            req.add_header('User-Agent', KKBOXHTTP.USER_AGENT)
            f = url_request.urlopen(req)
            r = f.read()
        except url_request.HTTPError as e:
            print(e.fp.read())
            raise (e)
        except Exception as e:
            raise (e)

        try:  # Python 3
            r = str(r, 'utf-8')
        except:  # Python 2
            pass
            
        json_object = json.loads(r)
        return json_object

    def _post_data(self, url, post_parameters, headers):
        data = url_parse.urlencode(
            post_parameters) if post_parameters != None else None
        return self._do_post(url, data, headers)

    def _headers_with_access_token(self):
        return {'Authorization': 'Bearer %s' % self.access_token.access_token}



