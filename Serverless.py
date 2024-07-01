class Wsgi(object):

    def __init__(self, environ, start_response):
        import urllib.parse

        self.TempStore     = {} # 用于存储临时数据
        self.Response      = {}
        self.Environ       = environ
        self.StartResponse = start_response

        self.Sts = {
            'AK'    : self.Environ['ALIBABA_CLOUD_ACCESS_KEY_ID'],
            'SK'    : self.Environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET'],
            'Token' : self.Environ['ALIBABA_CLOUD_SECURITY_TOKEN'],
            'Region': self.Environ['FC_REGION'],
        }

        self.Server = {
            'Owner'    : self.Environ['FC_ACCOUNT_ID'],
            'Region'   : self.Environ['FC_REGION'],
            'Service'  : self.Environ['FC_SERVICE_NAME'],
            'Function' : self.Environ['FC_FUNCTION_NAME'],
            'Qualifier': self.Environ['FC_QUALIFIER'],
            'Instance' : self.Environ['FC_INSTANCE_ID']
        }

        self.Request = {}

        for Key, Value in self.Environ.items():
            if Key.startswith("HTTP_"):
                self.Request[
                    urllib.parse.unquote(Key[5:].replace('_', '-').title())
                ] = urllib.parse.unquote(Value)

        self.Request.update({
            'Id'    : self.Environ['fc.context'].request_id,
            'Ip'    : self.GetIp(),
            'Method': self.Environ.get('REQUEST_METHOD', ''),
            'Host'  : self.Environ.get('HTTP_HOST', ''),

            'Path'  : self.GetPath(),
            'Param' : self.GetPam(),
            'Data'  : self.GetData(),

            'Referer'     : self.Environ.get('HTTP_REFERER', ''),
            'User-Agent'  : self.Environ.get('HTTP_USER_AGENT', ''),
            'Content-Type': self.Environ.get('CONTENT_TYPE', '').lower()
        })


    def __call__(self, Body, Code = None, Header = None):
        import json

        self.Response = Body

        try   : Code = str(Code)
        except: Code = ''

        self.StartResponse(
            {
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
            }.get(Code, '200 OK'),
            [('Content-Type', 'application/json')] + (Header or [])
        )
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
            if _ in self.Environ and self.Environ[_].split(',')[0].strip() != '':
                return self.Environ[_].split(',')[0].strip()
        return '0.0.0.0'


    def GetPam(self):
        import json
        import urllib.parse

        Param = {}
        for KV in [_.split('=', 1) for _ in urllib.parse.unquote(self.Environ.get('QUERY_STRING', '')).split('&') if _]:
            if len(KV) > 1:
                try:    Param[urllib.parse.unquote(KV[0])] = json.loads(urllib.parse.unquote(KV[1]))
                except: Param[urllib.parse.unquote(KV[0])] = urllib.parse.unquote(KV[1])
            else:
                Param[urllib.parse.unquote(KV[0])] = ''
        return Param


    def GetPath(self):
        import urllib.parse
        return urllib.parse.unquote(self.Environ.get('PATH_INFO', ''))


    def GetData(self):
        import json
        import urllib.parse

        ContentType = self.Environ.get('CONTENT_TYPE', '').lower()

        try:    ContentLength = int(self.Environ.get('CONTENT_LENGTH', '0'))
        except: ContentLength = 0

        try:    Data = urllib.parse.unquote(self.Environ.get('wsgi.input', '').read(ContentLength).decode('utf-8'))
        except: Data = ''

        def DecodeJson(_):
            try:    return json.loads(_)
            except: return {}

        def DecodeForm(_):
            Form = {}
            for KV in [_.split('=', 1) for _ in _.split('&') if _]:
                if len(KV) > 1:
                    try:    Form[urllib.parse.unquote(KV[0])] = json.loads(urllib.parse.unquote(KV[1]))
                    except: Form[urllib.parse.unquote(KV[0])] = urllib.parse.unquote(KV[1])
                else:
                    Form[urllib.parse.unquote(KV[0])] = ''
            return Form

        if 'application/json' in ContentType:
            return DecodeJson(Data)
        elif 'form' in ContentType:
            return DecodeForm(Data)
        else:
            _ = DecodeJson(Data)
            if _: return _
            else: return DecodeForm(Data)


    def GetLocation(self):
        import requests

        ########### IPv4 ###########
        if '.' in self.Request['Ip']:
            def _IpApi():
                Url = 'http://ip-api.com/json/%s' % (self.Request['Ip'])
                Pam = {
                    'fields': 'country,regionName,city,isp,as',
                    'lang'  : 'zh-CN'
                }
                try:
                    Rsp = requests.get(Url, params = Pam, timeout = 7.5, verify = False).json()
                    Country = Rsp['country']
                    Region  = Rsp['regionName'].removesuffix('省').removesuffix('市').removesuffix('自治区').removesuffix('特别行政区') if Country == '中国' else Rsp['regionName']
                    City    = Rsp['city'].removesuffix('市').removesuffix('自治州').removesuffix('地区').removesuffix('盟').removesuffix('县').removesuffix('区').removesuffix('旗') if Country == '中国' else Rsp['city']

                    if Country == '中国':
                        Isp = Rsp['isp']; As = Rsp['isp'].upper() + Rsp['as'].upper()
                        if   'TELECOM' in As or 'CHINANET'  in As: Isp = '电信'
                        elif 'UNICOM'  in As or 'CHINA169'  in As: Isp = '联通'
                        elif 'MOBILE'  in As or 'CMNET'     in As: Isp = '移动'
                        elif 'TIETONG' in As or 'RAILWAT'   in As: Isp = '铁通'
                        elif 'CERNET'  in As or 'EDUCATION' in As: Isp = '教育网'
                    else:
                        Isp = Rsp['isp']

                    return ('%s %s %s %s' % (Country, Region, City, Isp)).replace('   ', ' ').replace('  ', ' ').strip()
                except:
                    return '未知 未知'

            def _CsdnApi():
                Url = 'https://searchplugin.csdn.net/api/v1/ip/get'
                Pam = {
                    'ip': self.Request['Ip']
                }
                try:
                    return requests.get(Url, params = Pam, timeout = 7.5, verify = False).json()['data']['address'].replace('    ', ' ').replace('   ', ' ').replace('  ', ' ').strip()
                except:
                    return '未知 未知'

            return _CsdnApi()

        ########### IPv6 ###########
        if ':' in self.Request['Ip']:
            def _ZxincApi():
                Url = 'http://ip.zxinc.org/api.php'
                Hed = {
                    'Accept'          : '*/*',
                    'Accept-Language' : 'zh-CN,zh;q=0.9',
                    'Cache-Control'   : 'no-cache',
                    'Dnt'             : '1',
                    'Pragma'          : 'no-cache',
                    'Priority'        : 'u=1, i',
                    'Referer'         : 'https://ip.zxinc.org/ipquery/',
                    'user-agent'      : self.Request['User-Agent'],
                    'X-Requested-With': 'XMLHttpRequest'
                }
                Pam = {
                    'type': 'json',
                    'ip'  : self.Request['Ip']
                }
                try:
                    Location = requests.get(Url, headers = Hed, params = Pam, timeout = 7.5).json()['data']['location']
                    if '中国' in Location:
                        Location = Location.replace('省\t', ' ').replace('市\t', ' ').replace('自治区\t', ' ').replace('特别行政区\t', ' ').replace('自治州\t', ' ').replace('地区\t', ' ').replace('盟\t', ' ').replace('县\t', ' ').replace('区\t', ' ').replace('旗\t', ' ')
                        Location = Location.replace('中国电信', '电信').replace('中国联通', '联通').replace('中国移动', '移动').replace('中国铁通', '铁通').replace('中国教育网', '教育网').replace('中国教育和科研计算机网 (CERNET)', '教育网').removesuffix('无线基站网络').removesuffix('有线宽带网络').removesuffix('政企专线')
                        Location = Location.replace('\t', ' ').replace('    ', ' ').replace('   ', ' ').replace('  ', ' ').strip()
                        return Location
                    else:
                        return Location
                except:
                    return '未知 未知'

            return _ZxincApi()

        return '未知 未知'


    def CallWebhook(self, AccessToken, ShowRequestDetail = False, ShowResponseDetail = False, IncludeOptions = False):
        if self.Request['Method'] == 'OPTIONS' and not IncludeOptions:
            return None

        self.Request['Location'] = self.GetLocation()

        if __name__ == '__main__':
            from  Webhook import DingTalk
        else:
            from .Webhook import DingTalk

        Markdown = [{
            'Title': '用户请求信息',
            'Color': 'BLUE',
            'Text' : [
                f'请求接口: {self.Server["Function"]}/{self.Server["Qualifier"]}',
                f'请求方法: {self.Request["Method"]}',
                f'用户来源: {self.Request["Ip"]}',
                f'用户地区: {self.Request["Location"]}',
                f'用户设备: {self.Request["User-Agent"]}'
            ]
        }]

        Markdown.append({
            'Title': '接口响应信息',
            'Color': 'RED' if self.Response['ErrorCode'] else 'GREEN',
            'Text' : [
                f'集群编号: {self.Server["Service"]}_{self.Server["Instance"]}',
                f'错误代码: {self.Response["ErrorCode"] or "None"}',
                f'错误信息: {self.Response["ErrorMsg"] or "None"}',
            ]
        })

        if ShowRequestDetail:
            import json
            Markdown.append({
                'Title': '详细请求日志',
                'Color': 'BLUE',
                'Text' : [
                    f'请求参数: {json.dumps(self.Request["Param"], ensure_ascii = False).replace("{}", "None")}',
                    f'请求负载: {json.dumps(self.Request["Data"], ensure_ascii = False).replace("{}", "None")}'
                ]
            })

        if ShowResponseDetail:
            import json
            Markdown.append({
                'Title': '详细响应日志',
                'Color': 'BLUE',
                'Text' : [
                    f'响应负载: {json.dumps(self.Response["Data"], ensure_ascii = False).replace("{}", "None")}'
                ]
            })

        DingTalk({
            'Org'  : '【Serverless】WSGI 请求监控',
            'Data' : Markdown,
            'Token': AccessToken
        })

        return None
