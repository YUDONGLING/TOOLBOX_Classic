class Context(object):

    def __init__(self, object, start_response):
        start_response('200 OK', [('Content-Type', 'application/json')])

        self.Sts = {
            'AK'    : object['ALIBABA_CLOUD_ACCESS_KEY_ID'],
            'SK'    : object['ALIBABA_CLOUD_ACCESS_KEY_SECRET'],
            'Token' : object['ALIBABA_CLOUD_SECURITY_TOKEN'],
            'Region': object['FC_REGION'],
        }

        self.Server = {
            'Owner'   : object['FC_ACCOUNT_ID'],
            'Region'  : object['FC_REGION'],
            'Service' : object['FC_SERVICE_NAME'],
            'Function': object['FC_FUNCTION_NAME'],
            'Instance': object['FC_INSTANCE_ID']
        }

        self.Request = {}
        for Key, Value in object.items():
            if Key.startswith("HTTP_"): self.Request[Key[5:].replace('_', '-').title()] = Value.lower()

        self.Request.update({
            'Id'    : object['fc.context'].request_id,
            'Ip'    : self.GetIp(object),
            'Method': object.get('REQUEST_METHOD', ''),
            'Host'  : object.get('HTTP_HOST', ''),
            'Path'  : object.get('PATH_INFO', ''),
            'Param' : self.GetPam(object),
            'Data'  : self.GetData(object),

            'Referer'     : object.get('HTTP_REFERER', ''),
            'User-Agent'  : object.get('HTTP_USER_AGENT', ''),
            'Content-Type': object.get('CONTENT_TYPE', '').lower()
        })


    def __call__(self, object):
        import json
        return [json.dumps(object, indent = 4, ensure_ascii = False)]


    def GetIp(self, object):
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
            if _ in object:
                return object[_].split(',')[0].strip()
        return '0.0.0.0'


    def GetPam(self, object):
        Param = {}
        for _ in [_.split('=') for _ in object.get('QUERY_STRING', '').split('&')]:
            if len(_) > 1: Param[_[0]] = '='.join(_[1:])
        return Param


    def GetData(self, object):
        import json

        ContentType = object.get('CONTENT_TYPE', '').lower()

        try: 
            ContentLength = int(object.get('CONTENT_LENGTH', '0'))
        except Exception as errorMsg:
            ContentLength = 0

        try:
            Data = object.get('wsgi.input', '').read(ContentLength).decode('utf-8')
        except Exception as errorMsg:
            Data = object.get('wsgi.input', '').read(ContentLength)

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
