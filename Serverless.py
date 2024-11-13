class Wsgi(object):

    def __init__(self, environ, start_response):
        import time
        import urllib.parse

        # Quiter Logger
        self.FcQuiter = False

        # Timer
        self.StartProcess = int(time.time() * 1000)
        self.EndProcess   = -1

        self.Environ       = environ
        self.StartResponse = start_response

        # Security Token Service
        self.Sts = {
            'AK'    : self.Environ['ALIBABA_CLOUD_ACCESS_KEY_ID'],
            'SK'    : self.Environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET'],
            'Token' : self.Environ['ALIBABA_CLOUD_SECURITY_TOKEN'],
            'Region': self.Environ['FC_REGION'],
        }

        # Fc Runtime Environment
        self.Server = {
            'Owner'    : self.Environ['FC_ACCOUNT_ID'],
            'Region'   : self.Environ['FC_REGION'],
            'Service'  : self.Environ['FC_SERVICE_NAME'],
            'Function' : self.Environ['FC_FUNCTION_NAME'],
            'Qualifier': self.Environ['FC_QUALIFIER'],
            'Instance' : self.Environ['FC_INSTANCE_ID']
        }

        # Request
        self.Request     = {}
        self.RequestSize = -1

        for Key, Value in self.Environ.items():
            if Key.startswith('HTTP_') and Key not in ['HTTP_ALI_CDN_ADAPTIVE_PORTS', 'HTTP_ALI_CDN_REAL_IP', 'HTTP_ALI_SWIFT_LOG_HOST', 'HTTP_ALI_SWIFT_STAT_HOST', 'HTTP_EAGLEEYE_TRACEID', 'HTTP_VIA', 'HTTP_X_CDN_DAUTH_DATE', 'HTTP_X_CDN_ORIGIN_DAUTH', 'HTTP_X_CLIENT_SCHEME', 'HTTP_X_FORWARDED_FOR', 'HTTP_X_FORWARDED_PROTO', 'HTTP_X_OSS_SECURITY_TOKEN', 'HTTP_X_FC_FUNCTION_HANDLER']:
                self.Request[
                    urllib.parse.unquote(Key[5:].replace('_', '-').title())
                ] = urllib.parse.unquote(Value)

        self.Request.update({
            'Id'    : self.Environ['fc.context'].request_id,
            'Ip'    : self.GetIp(),
            'Method': self.Environ.get('REQUEST_METHOD', ''),
            'Host'  : self.Environ.get('HTTP_HOST', ''),

            'Cookie': self.GetCookie(),
            'Path'  : self.GetPath(),
            'Param' : self.GetPam(),
            'Data'  : self.GetData(),

            'Referer'     : self.Environ.get('HTTP_REFERER', ''),
            'User-Agent'  : self.Environ.get('HTTP_USER_AGENT', ''),
            'Content-Type': self.Environ.get('CONTENT_TYPE', '').lower()
        })

        # Response
        self.Response      = ''
        self.ResponseCode  = ''
        self.ResponseSize  = -1

        # Variables & Config
        self.Var = {}
        self.Cfg = {
            'Log.Enable'             : False,
            'Log.Prefix'             : '',
            'Log.Key'                : '',

            'Payload.Enable'         : False,
            'Payload.Prefix'         : '',
            'Payload.Key'            : '',
            'Payload.IncludeHeader'  : False,
            'Payload.IncludeCookie'  : False,
            'Payload.IncludeParam'   : False,
            'Payload.IncludePayload' : False,
            'Payload.IncludeResponse': False,

            'Webhook.Enable'         : False,
            'Webhook.RequestDetail'  : False,
            'Webhook.ResponseDetail' : False,
            'Webhook.IncludeHead'    : False,
            'Webhook.IncludeOptions' : False
        }


    def __call__(self, Body, Code: str = '200', Header: dict = {}):
        import json
        import time

        self.Response     = Body if isinstance(Body, str) else json.dumps(Body, ensure_ascii = False)
        self.ResponseCode = Code if '100' <= Code <= '599' else '200'
        self.ResponseSize = len(self.Response)

        try:
            if isinstance(Header, dict) and not 'Content-Type' in Header.keys():
                Header['Content-Type'] = 'application/json'
            elif not isinstance(Header, dict):
                raise Exception()
        except:
            Header = {'Content-Type': 'application/json'}

        self.StartResponse(self.ResponseCode, [(Key, Value) for Key, Value in Header.items()])
        self.EndProcess = int(time.time() * 1000)
        return [self.Response]


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

        try:    self.RequestSize = int(self.Environ.get('CONTENT_LENGTH', '0'))
        except: self.RequestSize = 0

        def DecodeJson(_):
            try:    return json.loads(_)
            except: return {}

        def DecodeForm(_):
            try:
                Form = {}
                for KV in [_.split('=', 1) for _ in _.split('&') if _]:
                    if len(KV) > 1:
                        try:    Form[urllib.parse.unquote(KV[0])] = json.loads(urllib.parse.unquote(KV[1]))
                        except: Form[urllib.parse.unquote(KV[0])] = urllib.parse.unquote(KV[1])
                    else:
                        Form[urllib.parse.unquote(KV[0])] = ''
                return Form
            except:
                return {}

        def DecodeMultipart(_):
            import cgi
            try:
                Form = {}
                FieldStorage = cgi.FieldStorage(fp = _['wsgi.input'], environ = _, keep_blank_values = True)
                for Field in FieldStorage.keys():
                    if FieldStorage[Field].filename:
                        Form[Field] = {'filename': FieldStorage[Field].filename, 'content': FieldStorage[Field].file.read()}
                    else:
                        Form[Field] = FieldStorage[Field].value
                return Form
            except:
                return {}

        if self.RequestSize <= 0:
            return {}
        elif 'multipart/form-data' in ContentType:
            return DecodeMultipart(self.Environ)
        else:
            Data = self.Environ['wsgi.input'].read(self.RequestSize).decode('utf-8')
            if 'application/json' in ContentType:
                return DecodeJson(Data)
            if 'application/x-www-form-urlencoded' in ContentType:
                return DecodeForm(Data)
            return DecodeJson(Data) or DecodeForm(Data) or {}


    def GetCookie(self):
        import json
        import urllib.parse

        Cookie = {}
        for KV in [_.split('=', 1) for _ in urllib.parse.unquote(self.Environ.get('HTTP_COOKIE', '')).split('; ') if _]:
            if len(KV) > 1:
                try:    Cookie[urllib.parse.unquote(KV[0])] = json.loads(urllib.parse.unquote(KV[1]))
                except: Cookie[urllib.parse.unquote(KV[0])] = urllib.parse.unquote(KV[1])
            else:
                Cookie[urllib.parse.unquote(KV[0])] = ''
        return Cookie


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
                    Location = requests.get(Url, headers = Hed, params = Pam, timeout = 7.5, verify = False).json()['data']['location']
                    if '中国' in Location:
                        Location = Location.replace('省\t', ' ').replace('市\t', ' ').replace('自治区\t', ' ').replace('特别行政区\t', ' ').replace('自治州\t', ' ').replace('地区\t', ' ').replace('盟\t', ' ').replace('县\t', ' ').replace('区\t', ' ').replace('旗\t', ' ')
                        Location = Location.replace('省 ', ' ').replace('市 ', ' ').replace('自治区 ', ' ').replace('特别行政区 ', ' ').replace('自治州 ', ' ').replace('地区 ', ' ').replace('盟 ', ' ').replace('县 ', ' ').replace('区 ', ' ').replace('旗 ', ' ')
                        Location = Location.replace('中国电信', '电信').replace('中国联通', '联通').replace('中国移动', '移动').replace('中国铁通', '铁通').replace('中国教育网', '教育网').replace('中国教育和科研计算机网 (CERNET)', '教育网')

                    Location = Location.removesuffix('移动网络').removesuffix('无线基站网络').removesuffix('无线基站网络(物联网卡)').removesuffix('无线基站网络 (物联网卡)').removesuffix('公众宽带').removesuffix('政企专线')
                    Location = Location.replace('\t', ' ').replace('    ', ' ').replace('   ', ' ').replace('  ', ' ').strip()
                    return Location
                except:
                    return '未知 未知'

            return _ZxincApi()

        return '未知 未知'


    async def CallLog(self, Bucket, Region):
        if not self.Cfg.get('Log.Enable', False): return None

        if __name__ == '__main__':
            from  Oss import AppendObject
        else:
            from .Oss import AppendObject

        import time
        import asyncio
        Key  = '%s%s' % (self.Cfg.get('Log.Prefix', ''), self.Cfg.get('Log.Key', ''))
        Data = '%s - %s [%s] "%s /%s$%s@%s%s%s HTTP/1.1" %s %s %s "%s" "%s"\n' % (
            self.Request['Ip'],
            self.Request['Id'],
            time.strftime('%d/%b/%Y:%H:%M:%S %z', time.localtime()),
            self.Request['Method'],
            self.Server['Service'],
            self.Server['Function'],
            self.Server['Qualifier'],
            self.Request['Path'],
            '?%s' % ('&'.join(['%s=%s' % (Key, Value) for Key, Value in self.Request['Param'].items()])) if self.Request['Param'] else '',
            self.ResponseCode,
            self.ResponseSize,
            self.EndProcess - self.StartProcess,
            self.Request['Referer'],
            self.Request['User-Agent']
        )

        BasicLogging = asyncio.to_thread(AppendObject, {
            'Region'  : Region,
            'Bucket'  : Bucket,
            'Key'     : Key,
            'Data'    : Data,
            'AK'      : self.Sts['AK'],
            'SK'      : self.Sts['SK'],
            'STSToken': self.Sts['Token']
        })

        # Payload
        if not self.Cfg.get('Payload.Enable', False): return None

        if __name__ == '__main__':
            from  Oss import PutObject
        else:
            from .Oss import PutObject

        IncludeHeader   = self.Cfg.get('Payload.IncludeHeader', False)
        IncludeCookie   = self.Cfg.get('Payload.IncludeCookie', False)
        IncludeParam    = self.Cfg.get('Payload.IncludeParam', False)
        IncludePayload  = self.Cfg.get('Payload.IncludePayload', False)
        IncludeResponse = self.Cfg.get('Payload.IncludeResponse', False)
        if not (IncludeHeader or IncludeCookie or IncludeParam or IncludePayload or IncludeResponse): return None

        Key   = '%s%s' % (self.Cfg.get('Payload.Prefix', ''), self.Cfg.get('Payload.Key', '') or '%s.txt' % self.Request['Id'])
        Data += '\n\n'

        import json
        if IncludeHeader:
            Data += '[ Header ] '
            Data += json.dumps({Key: Value for Key, Value in self.Request.items() if Key not in ['Ip', 'Method', 'Host', 'Cookie', 'Path', 'Param', 'Data']}, ensure_ascii = False)
            Data += '\n'

        if IncludeCookie:
            Data += '[ Cookie ] '
            Data += json.dumps({Key: Value for Key, Value in self.Request['Cookie'].items()}, ensure_ascii = False)
            Data += '\n'

        if IncludeParam:
            Data += '[ Params ] '
            Data += json.dumps({Key: Value for Key, Value in self.Request['Param'].items()}, ensure_ascii = False)
            Data += '\n'

        if IncludePayload:
            Data += '[Payloads] '
            Data += json.dumps({Key: Value for Key, Value in self.Request['Data'].items()}, ensure_ascii = False)
            Data += '\n'

        if IncludeResponse:
            Data += '[Response] '
            try:    Data += json.dumps({Key: Value for Key, Value in self.Response.items()}, ensure_ascii = False)
            except: Data += self.Response
            Data += '\n'

        PayloadLogging = asyncio.to_thread(PutObject, {
            'Region'  : Region,
            'Bucket'  : Bucket,
            'Key'     : Key,
            'Data'    : Data,
            'AK'      : self.Sts['AK'],
            'SK'      : self.Sts['SK'],
            'STSToken': self.Sts['Token']
        })

        await asyncio.gather(BasicLogging, PayloadLogging)
        return None


    async def CallWebhook(self, AccessToken):
        if not self.Cfg.get('Webhook.Enable', False): return None

        ShowRequestDetail  = self.Cfg.get('Webhook.RequestDetail', False)
        ShowResponseDetail = self.Cfg.get('Webhook.ResponseDetail', False)
        IncludeHead        = self.Cfg.get('Webhook.IncludeHead', False)
        IncludeOptions     = self.Cfg.get('Webhook.IncludeOptions', False)

        if (self.Request['Method'] == 'HEAD' and not IncludeHead) or \
              (self.Request['Method'] == 'OPTIONS' and not IncludeOptions):
            return None

        import json

        if __name__ == '__main__':
            from  Webhook import DingTalk
        else:
            from .Webhook import DingTalk

        try:    Response, self.Response = self.Response, json.loads(self.Response)
        except: Response, self.Response = self.Response, {}

        Markdown = [{
            'Title': '用户请求信息',
            'Color': 'BLUE',
            'Text' : [
                f'请求接口: {self.Server["Function"]}/{self.Server["Qualifier"]}',
                f'请求方法: {self.Request["Method"]}',
                f'用户来源: {self.Request["Ip"]}',
                f'用户地区: {self.GetLocation()}',
                f'用户设备: {self.Request["User-Agent"]}'
            ]
        }]

        Markdown.append({
            'Title': '接口响应信息',
            'Color': 'RED' if self.Response.get('ErrorCode', self.Response.get('error_code', self.Response.get('Ec', self.Response.get('ec', 9999)))) else 'GREEN',
            'Text' : [
                f'集群编号: {self.Server["Service"]}_{self.Server["Instance"]}',
                f'错误代码: {self.Response.get("ErrorCode", self.Response.get("error_code", self.Response.get("Ec", self.Response.get("ec", 0)))) or "None"}',
                f'错误信息: {self.Response.get("ErrorMsg", self.Response.get("error_msg", self.Response.get("Em", self.Response.get("em", "")))) or "None"}',
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
                    f'响应负载: {Response}'
                ]
            })

        import asyncio
        await asyncio.to_thread(DingTalk, {
            'Org'  : '【Serverless】WSGI 请求监控',
            'Data' : Markdown,
            'Token': AccessToken
        })

        self.Response = Response
        return None


class FlowControl(object):

    def __init__(self, Ttl: int, Quota: int, Feature: str | list):
        self._TTL     = Ttl
        self._Quota   = Quota
        self._Feature = Feature if isinstance(Feature, list) else [str(Feature)]

        self._FeatureHash = self._hashFeature(Feature)
        self._PlusPrefix  = f'FlowCtrl_P_{self._FeatureHash}_'
        self._MinuPrefix  = f'FlowCtrl_M_{self._FeatureHash}_'


    def __iadd__(self, Count: int):
        for _ in range(Count):
            self._makeFile( self._PlusPrefix )
        return self


    def __isub__(self, Count: int):
        for _ in range( min(Count, self.count) ):
            self._makeFile(self._MinuPrefix)
        return self


    def _hashFeature(self, Feature):
        import time
        import hashlib
        return str(time.time() // self._TTL) + '_' + hashlib.md5('_'.join(sorted(Feature)).encode()).hexdigest()


    def _makeFile(self, Prefix):
        import uuid
        try:
            with open('%s%s' % (Prefix, uuid.uuid4()), 'w') as _: _.write('')
        except Exception as e: pass


    def _countFile(self, Prefix):
        import os
        return len([_ for _ in os.listdir() if _.startswith(Prefix)])


    def reset(self):
        self -= self.count


    @property
    def ok(self):
        return self.count <= self._Quota


    @property
    def ttl(self):
        return self._TTL


    @property
    def after(self):
        import time
        _ = time.time()
        return int((_ // self._TTL + 1) * self._TTL - _)


    @property
    def count(self):
        return self._countFile(self._PlusPrefix) - self._countFile(self._MinuPrefix)
