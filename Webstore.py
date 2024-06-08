def __AliyunClient__(AK: str, SK: str, EndPoint: str, STSToken: str = None):
    from alibabacloud_tea_openapi import models as OpenApiModels
    from alibabacloud_tea_openapi.client import Client as OpenApiClient
    if STSToken:
        return OpenApiClient(OpenApiModels.Config(access_key_id = AK, access_key_secret = SK, endpoint = EndPoint, security_token = STSToken))
    else:
        return OpenApiClient(OpenApiModels.Config(access_key_id = AK, access_key_secret = SK, endpoint = EndPoint))


def __AliyunEndPoint__(RegionId: str, ProductCode = 'Dcdn'):
    if RegionId in []:
        return f'dcdn.{RegionId}.aliyuncs.com'
    else:
        return f'dcdn.aliyuncs.com'


def Get(Cfg = None):
    import json

    if __name__ == '__main__':
        from  Merge import MergeCfg
    else:
        from .Merge import MergeCfg

    Config = {
        'Web'     : True,                # True: 从 Web Dcdn 请求数据, False: 从 API 请求数据
        'Key'     : 'sample',            # 记录の键
        'Space'   : 'sample-storage',    # 记录の域
        'AK'      : 'AccessKey Id',
        'SK'      : 'AccessKey Secret',
        'STSToken': '',                  # 临时性凭证 (可留空)
        'RegionId': 'cn-hangzhou'        # 服务接入点 (可留空)
    }
    Config = MergeCfg(Config, Cfg)

    Response = {
        'ErrorCode': 0,
        'ErrorMsg' : '',
        'Key'      : '',
        'Value'    : ''
    }

    if Config['Web']:
        import requests

        try:
            Url = f'http://storage.edge-routine.yudongling.net.w.cdngslb.com/'
            Hed = {
                'Content-Type': 'application/json',
                'Host'        : 'storage.edge-routine.yudongling.net'
            }
            Dat = {
                'action'   : 'get',
                'namespace': Config['Space'],
                'key'      : Config['Key']
            }
            Rsp = requests.post(Url, headers = Hed, data = json.dumps(Dat), timeout = 5).json()

            if Rsp['ErrorCode'] != 0:
                Response['ErrorCode'] = Rsp['ErrorCode']
                Response['ErrorMsg']  = Rsp['ErrorMsg']
            else:
                Response['Key']   = Rsp['Data']['Key']
                Response['Value'] = json.loads(Rsp['Data']['Value'])
        except Exception as errorMsg:
            Response['ErrorCode'] = 50000
            Response['ErrorMsg']  = f'Fail to request data via web, {str(errorMsg).lower().rstrip(".")}'

        return Response

    if not Config['Web']:
        from alibabacloud_tea_util import models as UtilModels
        from alibabacloud_tea_openapi import models as OpenApiModels
        from alibabacloud_openapi_util.client import Client as OpenApiUtilClient

        try:
            Client  = __AliyunClient__(AK = Config['AK'], SK = Config['SK'], STSToken = Config['STSToken'], EndPoint = __AliyunEndPoint__(Config['RegionId']))
            Params  = OpenApiModels.Params(
                action        = 'GetDcdnKv',
                version       = '2018-01-15',
                protocol      = 'HTTPS',
                method        = 'GET',
                auth_type     = 'AK',
                style         = 'RPC',
                pathname      = '/',
                req_body_type = 'json',
                body_type     = 'json'
            )
            Request = OpenApiModels.OpenApiRequest(query = OpenApiUtilClient.query({
                'Namespace': Config['Space'],
                'Key'      : Config['Key']
            }))
            Runtime = UtilModels.RuntimeOptions(autoretry = True, max_attempts = 3, read_timeout = 10000, connect_timeout = 10000)
        except Exception as errorMsg:
            Response['ErrorCode'] = 50001
            Response['ErrorMsg']  = f'Fail to init openapi model, {str(errorMsg).lower().rstrip(".")}'
            return Response

        try:
            # 复制代码运行请自行打印 API 的返回值
            # 返回值为 Map 类型，可从 Map 中获得三类数据：响应体 body、响应头 headers、HTTP 返回的状态码 statusCode。
            Response['Value'] = json.loads(Client.call_api(Params, Request, Runtime)['body']['Value'])
            Response['Key']   = Config['Key']
        except Exception as errorMsg:
            Response['ErrorCode'] = 50002
            Response['ErrorMsg']  = f'Fail to request openapi model, {str(errorMsg.data.get("Message", errorMsg.message)).lower().rstrip(".")}'
            return Response

        return Response


def Put(Cfg = None):
    import json

    if __name__ == '__main__':
        from  Merge import MergeCfg
    else:
        from .Merge import MergeCfg

    Config = {
        'Web'     : True,                # True: 从 Web Dcdn 请求数据, False: 从 API 请求数据
        'Key'     : 'sample',            # 记录の键
        'Value'   : 'sample-value',      # 记录の值
        'Space'   : 'sample-storage',    # 记录の域
        'AK'      : 'AccessKey Id',
        'SK'      : 'AccessKey Secret',
        'STSToken': '',                  # 临时性凭证 (可留空)
        'RegionId': 'cn-hangzhou'        # 服务接入点 (可留空)
    }
    Config = MergeCfg(Config, Cfg)

    Response = {
        'ErrorCode': 0,
        'ErrorMsg' : ''
    }

    if Config['Web']:
        import requests

        try:
            Url = f'http://storage.edge-routine.yudongling.net.w.cdngslb.com/'
            Hed = {
                'Content-Type': 'application/json',
                'Host'        : 'storage.edge-routine.yudongling.net'
            }
            Dat = {
                'action'   : 'put',
                'namespace': Config['Space'],
                'key'      : Config['Key'],
                'value'    : Config['Value']
            }
            Rsp = requests.post(Url, headers = Hed, data = json.dumps(Dat), timeout = 5).json()

            if Rsp['ErrorCode'] != 0:
                Response['ErrorCode'] = Rsp['ErrorCode']
                Response['ErrorMsg']  = Rsp['ErrorMsg']
        except Exception as errorMsg:
            Response['ErrorCode'] = 50000
            Response['ErrorMsg']  = f'Fail to request data via web, {str(errorMsg).lower().rstrip(".")}'

        return Response

    if not Config['Web']:
        from alibabacloud_tea_util import models as UtilModels
        from alibabacloud_tea_openapi import models as OpenApiModels
        from alibabacloud_openapi_util.client import Client as OpenApiUtilClient

        try:
            Client  = __AliyunClient__(AK = Config['AK'], SK = Config['SK'], STSToken = Config['STSToken'], EndPoint = __AliyunEndPoint__(Config['RegionId']))
            Params  = OpenApiModels.Params(
                action        = 'PutDcdnKv',
                version       = '2018-01-15',
                protocol      = 'HTTPS',
                method        = 'POST',
                auth_type     = 'AK',
                style         = 'RPC',
                pathname      = '/',
                req_body_type = 'formData',
                body_type     = 'json'
            )
            Request = OpenApiModels.OpenApiRequest(query = OpenApiUtilClient.query({
                'Namespace': Config['Space'],
                'Key'      : Config['Key']
            }), body = {'Value': Config['Value']})
            Runtime = UtilModels.RuntimeOptions(autoretry = True, max_attempts = 3, read_timeout = 10000, connect_timeout = 10000)
        except Exception as errorMsg:
            Response['ErrorCode'] = 50001
            Response['ErrorMsg']  = f'Fail to init openapi model, {str(errorMsg).lower().rstrip(".")}'
            return Response

        try:
            # 复制代码运行请自行打印 API 的返回值
            # 返回值为 Map 类型，可从 Map 中获得三类数据：响应体 body、响应头 headers、HTTP 返回的状态码 statusCode。
            Client.call_api(Params, Request, Runtime)
        except Exception as errorMsg:
            Response['ErrorCode'] = 50002
            Response['ErrorMsg']  = f'Fail to request openapi model, {str(errorMsg.data.get("Message", errorMsg.message)).lower().rstrip(".")}'
            return Response

        return Response


def Delete(Cfg = None):
    import json

    if __name__ == '__main__':
        from  Merge import MergeCfg
    else:
        from .Merge import MergeCfg

    Config = {
        'Web'     : True,                # True: 从 Web Dcdn 请求数据, False: 从 API 请求数据
        'Key'     : 'sample',            # 记录の键
        'Space'   : 'sample-storage',    # 记录の域
        'AK'      : 'AccessKey Id',
        'SK'      : 'AccessKey Secret',
        'STSToken': '',                  # 临时性凭证 (可留空)
        'RegionId': 'cn-hangzhou'        # 服务接入点 (可留空)
    }
    Config = MergeCfg(Config, Cfg)

    Response = {
        'ErrorCode': 0,
        'ErrorMsg' : ''
    }

    if Config['Web']:
        import requests

        try:
            Url = f'http://storage.edge-routine.yudongling.net.w.cdngslb.com/'
            Hed = {
                'Content-Type': 'application/json',
                'Host'        : 'storage.edge-routine.yudongling.net'
            }
            Dat = {
                'action'   : 'delete',
                'namespace': Config['Space'],
                'key'      : Config['Key']
            }
            Rsp = requests.post(Url, headers = Hed, data = json.dumps(Dat), timeout = 5).json()

            if Rsp['ErrorCode'] != 0:
                Response['ErrorCode'] = Rsp['ErrorCode']
                Response['ErrorMsg']  = Rsp['ErrorMsg']
        except Exception as errorMsg:
            Response['ErrorCode'] = 50000
            Response['ErrorMsg']  = f'Fail to request data via web, {str(errorMsg).lower().rstrip(".")}'

        return Response

    if not Config['Web']:
        from alibabacloud_tea_util import models as UtilModels
        from alibabacloud_tea_openapi import models as OpenApiModels
        from alibabacloud_openapi_util.client import Client as OpenApiUtilClient

        try:
            Client  = __AliyunClient__(AK = Config['AK'], SK = Config['SK'], STSToken = Config['STSToken'], EndPoint = __AliyunEndPoint__(Config['RegionId']))
            Params  = OpenApiModels.Params(
                action        = 'DeleteDcdnKv',
                version       = '2018-01-15',
                protocol      = 'HTTPS',
                method        = 'POST',
                auth_type     = 'AK',
                style         = 'RPC',
                pathname      = '/',
                req_body_type = 'json',
                body_type     = 'json'
            )
            Request = OpenApiModels.OpenApiRequest(query = OpenApiUtilClient.query({
                'Namespace': Config['Space'],
                'Key'      : Config['Key']
            }))
            Runtime = UtilModels.RuntimeOptions(autoretry = True, max_attempts = 3, read_timeout = 10000, connect_timeout = 10000)
        except Exception as errorMsg:
            Response['ErrorCode'] = 50001
            Response['ErrorMsg']  = f'Fail to init openapi model, {str(errorMsg).lower().rstrip(".")}'
            return Response

        try:
            # 复制代码运行请自行打印 API 的返回值
            # 返回值为 Map 类型，可从 Map 中获得三类数据：响应体 body、响应头 headers、HTTP 返回的状态码 statusCode。
            Client.call_api(Params, Request, Runtime)
        except Exception as errorMsg:
            Response['ErrorCode'] = 50002
            Response['ErrorMsg']  = f'Fail to request openapi model, {str(errorMsg.data.get("Message", errorMsg.message)).lower().rstrip(".")}'
            return Response

        return Response
