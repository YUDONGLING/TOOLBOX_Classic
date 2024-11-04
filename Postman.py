import requests


def QueryLocalDns(Host, Global = False, Region = '' or []) -> str:
    import os
    import json

    File = 'Global_IPs.json' if Global else 'CN_IPs.json'
    if not os.path.exists(os.path.join(os.path.dirname(__file__), 'Extra', File)):
        raise FileNotFoundError('The file %s does not exist.' % File)
    else:
        with open(os.path.join(os.path.dirname(__file__), 'Extra', File), 'r', encoding = 'utf-8') as f:
            IPs = json.load(f)

    if isinstance(Region, str): Region = [Region]

    def FetchIPs(Zone, IPs):
        Zone = Zone.split('.'); Temp = IPs
        while Zone:
            try: Temp = Temp[Zone.pop(0)]
            except KeyError: return []
        return Temp

    Pool = []
    for Rule in [_ for _ in Region if     _.startswith('-')]: FetchIPs(Rule.removeprefix('-'), IPs).clear()
    for Rule in [_ for _ in Region if not _.startswith('-')]: Pool.append(FetchIPs(Rule, IPs))

    def MergeIPs(Tar, Src):
        if isinstance(Src, list):
            for _ in Src: MergeIPs(Tar, _)
        elif isinstance(Src, dict):
            for _, _IPs in Src.items(): MergeIPs(Tar, _IPs)
        else: Tar.append(Src)

    import random
    IP   = []; MergeIPs(IP, Pool)
    IP   = random.choice(IP)
    Host = Host.removeprefix('//').removeprefix('http://').removeprefix('https://').removesuffix('/')

    import requests
    try: return requests.get(f'https://dns.alidns.com/resolve?name={Host}&type=A&short=1&edns_client_subnet={Pool}', timeout = 10).json().pop()
    except Exception as e: return Host


class PostmanRequest(object):
    def __init__(self, postman_url: str | bytes,
                       postman_params          = None,
                       postman_headers         = None,
                       postman_cookies         = None,
                       postman_auth            = None,
                       postman_timeout         = None,
                       postman_allow_redirects = True,
                       postman_proxies         = None,
                       postman_hooks           = None,
                       postman_stream          = None,
                       postman_verify          = None,
                       postman_cert            = None):
        self.postman_method          = 'POST'
        self.postman_url             = postman_url
        self.postman_params          = postman_params
        self.postman_headers         = postman_headers
        self.postman_cookies         = postman_cookies
        self.postman_auth            = postman_auth
        self.postman_timeout         = postman_timeout
        self.postman_allow_redirects = postman_allow_redirects
        self.postman_proxies         = postman_proxies
        self.postman_hooks           = postman_hooks
        self.postman_stream          = postman_stream
        self.postman_verify          = postman_verify
        self.postman_cert            = postman_cert
  
    def request(self, method: str | bytes, url: str | bytes,
                      params          = None,
                      data            = None,
                      headers         = None,
                      cookies         = None,
                      auth            = None,
                      timeout         = None,
                      allow_redirects = True,
                      proxies         = None,
                      stream          = None,
                      verify          = None,
                      cert            = None):
        import json
        response = requests.request(
            method          = self.postman_method.upper(),
            url             = self.postman_url,
            params          = self.postman_params,
            headers         = self.postman_headers,
            cookies         = self.postman_cookies,
            auth            = self.postman_auth,
            timeout         = self.postman_timeout,
            allow_redirects = self.postman_allow_redirects,
            proxies         = self.postman_proxies,
            hooks           = self.postman_hooks,
            stream          = self.postman_stream,
            verify          = self.postman_verify,
            cert            = self.postman_cert,
            data            = json.dumps({
                'method'         : method.upper(),
                'url'            : url,
                'params'         : params,
                'data'           : json.dumps(data),
                'headers'        : headers,
                'cookies'        : cookies,
                'auth'           : auth,
                'timeout'        : timeout,
                'allow_redirects': allow_redirects,
                'proxies'        : proxies,
                'stream'         : stream,
                'verify'         : verify,
                'cert'           : cert
            })
        )

        if response.status_code != 200:
            # Postman Side Error
            raise requests.exceptions.HTTPError(f"Error: {response.status_code}, {response.text}")
        elif response.json().get('ErrorCode'):
            # Target Server Side Error
            _Type, _Msg = response.json().get('ErrorType'), response.json().get('ErrorMsg')
            match _Type:
                case 'URLRequired'          : raise requests.exceptions.URLRequired          ('TargetServer@%s' % _Msg)
                case 'InvalidURL'           : raise requests.exceptions.InvalidURL           ('TargetServer@%s' % _Msg)
                case 'MissingSchema'        : raise requests.exceptions.MissingSchema        ('TargetServer@%s' % _Msg)
                case 'InvalidSchema'        : raise requests.exceptions.InvalidSchema        ('TargetServer@%s' % _Msg)
                case 'InvalidHeader'        : raise requests.exceptions.InvalidHeader        ('TargetServer@%s' % _Msg)
                case 'InvalidProxyURL'      : raise requests.exceptions.InvalidProxyURL      ('TargetServer@%s' % _Msg)
                case 'JSONDecodeError'      : raise requests.exceptions.JSONDecodeError      ('TargetServer@%s' % _Msg)
                case 'InvalidJSONError'     : raise requests.exceptions.InvalidJSONError     ('TargetServer@%s' % _Msg)
                case 'ChunkedEncodingError' : raise requests.exceptions.ChunkedEncodingError ('TargetServer@%s' % _Msg)
                case 'ConnectTimeout'       : raise requests.exceptions.ConnectTimeout       ('TargetServer@%s' % _Msg)
                case 'ReadTimeout'          : raise requests.exceptions.ReadTimeout          ('TargetServer@%s' % _Msg)
                case 'Timeout'              : raise requests.exceptions.Timeout              ('TargetServer@%s' % _Msg)
                case 'SSLError'             : raise requests.exceptions.SSLError             ('TargetServer@%s' % _Msg)
                case 'ProxyError'           : raise requests.exceptions.ProxyError           ('TargetServer@%s' % _Msg)
                case 'ConnectionError'      : raise requests.exceptions.ConnectionError      ('TargetServer@%s' % _Msg)
                case 'TooManyRedirects'     : raise requests.exceptions.TooManyRedirects     ('TargetServer@%s' % _Msg)
                case 'HTTPError'            : raise requests.exceptions.HTTPError            ('TargetServer@%s' % _Msg)
                case 'ContentDecodingError' : raise requests.exceptions.ContentDecodingError ('TargetServer@%s' % _Msg)
                case 'StreamConsumedError'  : raise requests.exceptions.StreamConsumedError  ('TargetServer@%s' % _Msg)
                case 'UnrewindableBodyError': raise requests.exceptions.UnrewindableBodyError('TargetServer@%s' % _Msg)
                case 'RetryError'           : raise requests.exceptions.RetryError           ('TargetServer@%s' % _Msg)
                case 'RequestException'     : raise requests.exceptions.RequestException     ('TargetServer@%s' % _Msg)
                case 'TypeError'            : raise TypeError                                ('TargetServer@%s' % _Msg)
                case 'ValueError'           : raise ValueError                               ('TargetServer@%s' % _Msg)
                case 'IOError'              : raise IOError                                  ('TargetServer@%s' % _Msg)
                case _                      : raise Exception                                ('TargetServer@%s' % _Msg)
        else:
            return PostmanResponse(self, response.json())

    def get(self, url: str | bytes,
                  params = None, data = None, headers = None, cookies = None, auth   = None, timeout = None,
                  allow_redirects     = True, proxies = None, stream  = None, verify = None, cert    = None):
        return self.request('GET', url, params, data, headers, cookies, auth, timeout, allow_redirects, proxies, stream, verify, cert)

    def options(self, url: str | bytes,
                      params = None, data = None, headers = None, cookies = None, auth   = None, timeout = None,
                      allow_redirects     = True, proxies = None, stream  = None, verify = None, cert    = None):
          return self.request('OPTIONS', url, params, data, headers, cookies, auth, timeout, allow_redirects, proxies, stream, verify, cert)

    def head(self, url: str | bytes,
                   params = None, data = None, headers = None, cookies = None, auth   = None, timeout = None,
                   allow_redirects     = True, proxies = None, stream  = None, verify = None, cert    = None):
          return self.request('HEAD', url, params, data, headers, cookies, auth, timeout, allow_redirects, proxies, stream, verify, cert)

    def post(self, url: str | bytes,
                   params = None, data = None, headers = None, cookies = None, auth   = None, timeout = None,
                   allow_redirects     = True, proxies = None, stream  = None, verify = None, cert    = None):
          return self.request('POST', url, params, data, headers, cookies, auth, timeout, allow_redirects, proxies, stream, verify, cert)

    def put(self, url: str | bytes,
                  params = None, data = None, headers = None, cookies = None, auth   = None, timeout = None,
                  allow_redirects     = True, proxies = None, stream  = None, verify = None, cert    = None):
          return self.request('PUT', url, params, data, headers, cookies, auth, timeout, allow_redirects, proxies, stream, verify, cert)
    
    def patch(self, url: str | bytes,
                    params = None, data = None, headers = None, cookies = None, auth   = None, timeout = None,
                    allow_redirects     = True, proxies = None, stream  = None, verify = None, cert    = None):
            return self.request('PATCH', url, params, data, headers, cookies, auth, timeout, allow_redirects, proxies, stream, verify, cert)
    
    def delete(self, url: str | bytes,
                     params = None, data = None, headers = None, cookies = None, auth   = None, timeout = None,
                     allow_redirects     = True, proxies = None, stream  = None, verify = None, cert    = None):
            return self.request('DELETE', url, params, data, headers, cookies, auth, timeout, allow_redirects, proxies, stream, verify, cert)


class PostmanResponse(object):
    def __init__(self,
                 postman_request : PostmanRequest,
                 postman_response: requests.Response):
        import base64

        self._content = base64.b64decode(postman_response['_content'])
        self._content_consumed = True
        self._next = postman_response['next']

        #: Integer Code of responded HTTP Status, e.g. 404 or 200.
        self.status_code = postman_response['status_code']

        #: Case-insensitive Dictionary of Response Headers.
        #: For example, ``headers['content-encoding']`` will return the
        #: value of a ``'Content-Encoding'`` response header.
        self.headers = requests.structures.CaseInsensitiveDict(postman_response['headers'])

        #: File-like object representation of response (for advanced usage).
        #: Use of ``raw`` requires that ``stream=True`` be set on the request.
        #: This requirement does not apply for use internally to Requests.
        self.raw = postman_request

        #: Final URL location of Response.
        self.url = postman_response['url']

        #: Encoding to decode with when accessing r.text.
        self.encoding = postman_response['encoding']
        self.apparent_encoding = postman_response['apparent_encoding']

        #: A list of :class:`Response <Response>` objects from
        #: the history of the Request. Any redirect responses will end
        #: up here. The list is sorted from the oldest to the most recent request.
        self.history = []

        #: Textual reason of responded HTTP Status, e.g. "Not Found" or "OK".
        self.reason = postman_response['reason']

        #: A CookieJar of Cookies the server sent back.
        self.cookies = postman_response['cookies']

        #: The amount of time elapsed between sending the request
        #: and the arrival of the response (as a timedelta).
        #: This property specifically measures the time taken between sending
        #: the first byte of the request and finishing parsing the headers. It
        #: is therefore unaffected by consuming the response content or the
        #: value of the ``stream`` keyword argument.
        self.elapsed = postman_response['elapsed']

        #: The :class:`PreparedRequest <PreparedRequest>` object to which this
        #: is a response.
        self.request = None

        #: Other details of the response.
        try:
            self.content = self._content
            self.text = str(self.content, self.encoding, errors = 'replace')
        except (LookupError, TypeError):
            self.content = self._content
            self.text = str(self.content, errors = 'replace')

        self.ok = postman_response['ok']
        self.next = postman_response['next']
        self.links = postman_response['links']
        self.is_redirect = postman_response['is_redirect']
        self.is_permanent_redirect = postman_response['is_permanent_redirect']

    def __repr__(self):
        return f"<Response [{self.status_code}]>"

    def __bool__(self):
        return self.ok

    def __nonzero__(self):
        return self.ok

    def __iter__(self):
        return self.iter_content(128)

    def json(self, **kwargs):
        import json
        from requests.utils import guess_json_utf
        from requests.compat import JSONDecodeError
        from requests.exceptions import JSONDecodeError as RequestsJSONDecodeError

        if not self.encoding and self.content and len(self.content) > 3:
            # No encoding set. JSON RFC 4627 section 3 states we should expect
            # UTF-8, -16 or -32. Detect which one to use; If the detection or
            # decoding fails, fall back to `self.text` (using charset_normalizer to make
            # a best guess).
            encoding = guess_json_utf(self.content)
            if encoding is not None:
                try:
                    return json.loads(self.content.decode(encoding), **kwargs)
                except UnicodeDecodeError:
                    # Wrong UTF codec detected; usually because it's not UTF-8
                    # but some other 8-bit codec.  This is an RFC violation,
                    # and the server didn't bother to tell us what codec *was*
                    # used.
                    pass
                except JSONDecodeError as e:
                    raise RequestsJSONDecodeError(e.msg, e.doc, e.pos)

        try:
            return json.loads(self.text, **kwargs)
        except JSONDecodeError as e:
            # Catch JSON-related errors and raise as requests.JSONDecodeError
            # This aliases json.JSONDecodeError and simplejson.JSONDecodeError
            raise RequestsJSONDecodeError(e.msg, e.doc, e.pos)

    def close(self):
        release_conn = getattr(self.raw, 'release_conn', None)
        if release_conn is not None:
            release_conn()
