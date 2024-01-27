class Wsgi(object):

    def __init__(self, environ, start_response):
        self.Environ       = environ
        self.StartResponse = start_response

        self.Sts = {
            'AK'    : self.Environ['ALIBABA_CLOUD_ACCESS_KEY_ID'],
            'SK'    : self.Environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET'],
            'Token' : self.Environ['ALIBABA_CLOUD_SECURITY_TOKEN'],
            'Region': self.Environ['FC_REGION'],
        }

        self.Server = {
            'Owner'   : self.Environ['FC_ACCOUNT_ID'],
            'Region'  : self.Environ['FC_REGION'],
            'Service' : self.Environ['FC_SERVICE_NAME'],
            'Function': self.Environ['FC_FUNCTION_NAME'],
            'Instance': self.Environ['FC_INSTANCE_ID']
        }

        self.Request = {}
        for Key, Value in self.Environ.items():
            if Key.startswith("HTTP_"): self.Request[Key[5:].replace('_', '-').title()] = Value.lower()

        self.Request.update({
            'Id'    : self.Environ['fc.context'].request_id,
            'Ip'    : self.GetIp(),
            'Method': self.Environ.get('REQUEST_METHOD', ''),
            'Host'  : self.Environ.get('HTTP_HOST', ''),
            'Path'  : self.Environ.get('PATH_INFO', ''),
            'Param' : self.GetPam(),
            'Data'  : self.GetData(),

            'Referer'     : self.Environ.get('HTTP_REFERER', ''),
            'User-Agent'  : self.Environ.get('HTTP_USER_AGENT', ''),
            'Content-Type': self.Environ.get('CONTENT_TYPE', '').lower()
        })


    def __call__(self, Body, Code = None, Header = None):
        import json

        _ = {
            '100': '100 Continue',
            '101': '101 Switching Protocols',
            '102': '102 Processing',
            '103': '103 Early Hints',
            '200': '200 OK',
            '201': '201 Created',
            '202': '202 Accepted',
            '203': '203 Non-Authoritative Information',
            '204': '204 No Content',
            '205': '205 Reset Content',
            '206': '206 Partial Content',
            '207': '207 Multi-Status',
            '208': '208 Already Reported',
            '226': '226 IM Used',
            '300': '300 Multiple Choices',
            '301': '301 Moved Permanently',
            '302': '302 Found',
            '303': '303 See Other',
            '304': '304 Not Modified',
            '305': '305 Use Proxy',
            '307': '307 Temporary Redirect',
            '308': '308 Permanent Redirect',
            '400': '400 Bad Request',
            '401': '401 Unauthorized',
            '402': '402 Payment Required',
            '403': '403 Forbidden',
            '404': '404 Not Found',
            '405': '405 Method Not Allowed',
            '406': '406 Not Acceptable',
            '407': '407 Proxy Authentication Required',
            '408': '408 Request Timeout',
            '409': '409 Conflict',
            '410': '410 Gone',
            '411': '411 Length Required',
            '412': '412 Precondition Failed',
            '413': '413 Payload Too Large',
            '414': '414 URI Too Long',
            '415': '415 Unsupported Media Type',
            '416': '416 Range Not Satisfiable',
            '417': '417 Expectation Failed',
            '418': "418 I'm a teapot",
            '421': '421 Misdirected Request',
            '422': '422 Unprocessable Entity',
            '423': '423 Locked',
            '424': '424 Failed Dependency',
            '425': '425 Too Early',
            '426': '426 Upgrade Required',
            '428': '428 Precondition Required',
            '429': '429 Too Many Requests',
            '431': '431 Request Header Fields Too Large',
            '451': '451 Unavailable For Legal Reasons',
            '500': '500 Internal Server Error',
            '501': '501 Not Implemented',
            '502': '502 Bad Gateway',
            '503': '503 Service Unavailable',
            '504': '504 Gateway Timeout',
            '505': '505 HTTP Version Not Supported',
            '506': '506 Variant Also Negotiates',
            '507': '507 Insufficient Storage',
            '508': '508 Loop Detected',
            '510': '510 Not Extended',
            '511': '511 Network Authentication Required'
        }

        self.StartResponse(_.get(Code, '200 OK'), [('Content-Type', 'application/json')] + (Header or []))
        return [json.dumps(Body, ensure_ascii = False)]


    def GetIp(self):
        for _ in [
            'HTTP_X_FORWARDED_FOR',
            'HTTP_X_REAL_IP',
            'HTTP_X_FORWARDED',
            'HTTP_FORWARDED_FOR',
            'HTTP_FORWARDED',
            'HTTP_TRUE_CLIENT_IP',
            'HTTP_CLIENT_IP',
            'HTTP_ALI_CDN_REAL_IP',
            'HTTP_CDN_SRC_IP',
            'HTTP_CDN_REAL_IP',
            'HTTP_CF_CONNECTING_IP',
            'HTTP_X_CLUSTER_CLIENT_IP',
            'HTTP_WL_PROXY_CLIENT_IP',
            'HTTP_PROXY_CLIENT_IP',
            'HTTP_TRUE_CLIENT_IP',
            'REMOTE_ADDR']:
            if _ in self.Environ:
                return self.Environ[_].split(',')[0].strip()
        return '0.0.0.0'


    def GetPam(self):
        Param = {}
        for _ in [_.split('=') for _ in self.Environ.get('QUERY_STRING', '').split('&')]:
            if len(_) > 1: Param[_[0]] = '='.join(_[1:])
        return Param


    def GetData(self):
        import json

        ContentType = self.Environ.get('CONTENT_TYPE', '').lower()

        try: 
            ContentLength = int(self.Environ.get('CONTENT_LENGTH', '0'))
        except Exception as errorMsg:
            ContentLength = 0

        try:
            Data = self.Environ.get('wsgi.input', '').read(ContentLength).decode('utf-8')
        except Exception as errorMsg:
            Data = self.Environ.get('wsgi.input', '').read(ContentLength)

        def DecodeJson(_):
            try:
                return json.loads(_)
            except Exception as errorMsg:
                return {}

        def DecodeForm(_):
            Form = {}
            try:
                for _ in [_.split('=') for _ in _.split('&')]:
                    if len(_) > 1: Form[_[0]] = '='.join(_[1:])
                return Form
            except Exception as errorMsg:
                return Form

        if 'application/json' in ContentType:
            return DecodeJson(Data)
        elif 'form' in ContentType:
            return DecodeForm(Data)
        else:
            _ = DecodeJson(Data)
            if _: return _
            else: return DecodeForm(Data)
