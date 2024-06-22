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
        'Web'     : True,
        'Key'     : None,                # 记录の键, '' OR ['', '', ...]
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
        'Data'     : {}
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
                'key'      : Config['Key'] if isinstance(Config['Key'], list) else [Config['Key']]
            }
            Rsp = requests.post(Url, headers = Hed, data = json.dumps(Dat), timeout = 5).json()

            for Key, Value in Rsp['Data'].items():
                try:
                    Rsp['Data'][Key]['value'] = json.loads(Value['value'])
                except:
                    pass

            return Rsp
        except Exception as errorMsg:
            Response['ErrorCode'] = -1
            Response['ErrorMsg']  = ''

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
            Runtime = UtilModels.RuntimeOptions(autoretry = True, max_attempts = 3, read_timeout = 10000, connect_timeout = 10000)
        except Exception as errorMsg:
            Response['ErrorCode'] = -1
            Response['ErrorMsg']  = ''
            return Response

        for Key in Config['Key'] if isinstance(Config['Key'], list) else [Config['Key']]:
            Key = str(Key)

            if len(Key) > 512:
                Response['Data'][Key] = {'code': 400, 'value': ''}
                continue

            try:
                Request = OpenApiModels.OpenApiRequest(query = OpenApiUtilClient.query({
                    'Namespace': Config['Space'],
                    'Key'      : Key
                }))
                Result  = Client.call_api(Params, Request, Runtime)

                try:
                    Response['Data'][Key] = {'code': 0, 'value': json.loads(Result['body']['Value'])}
                except:
                    Response['Data'][Key] = {'code': 0, 'value': Result['body']['Value']}
            except Exception as errorMsg:
                if errorMsg.data.get('Code') in ['InvalidKey.NotFound']:
                    Response['Data'][Key] = {'code': 404, 'value': ''}
                else:
                    Response['Data'][Key] = {'code': 500, 'value': ''}

        return Response


def Put(Cfg = None):
    import json

    if __name__ == '__main__':
        from  Merge import MergeCfg
    else:
        from .Merge import MergeCfg

    Config = {
        'Web'     : True,
        'KeyValue': [],                  # 记录の键值对
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
        'Data'     : {}
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
                'key'      : [_['Key'] for _ in Config['KeyValue']],
                'value'    : [_['Value'] for _ in Config['KeyValue']],
                'ttl'      : [_.get('Ttl', 0) for _ in Config['KeyValue']]
            }
            return requests.post(Url, headers = Hed, data = json.dumps(Dat), timeout = 5).json()
        except Exception as errorMsg:
            Response['ErrorCode'] = -1
            Response['ErrorMsg']  = ''

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
            Runtime = UtilModels.RuntimeOptions(autoretry = True, max_attempts = 3, read_timeout = 10000, connect_timeout = 10000)
        except Exception as errorMsg:
            Response['ErrorCode'] = -1
            Response['ErrorMsg']  = ''
            return Response

        for KvPair in Config['KeyValue']:
            Key = str(KvPair['Key'])

            if len(Key) > 512:
                Response['Data'][Key] = {'code': 400}
                continue

            if isinstance(KvPair['Value'], str):
                Value = KvPair['Value']
            elif isinstance(KvPair['Value'], dict) or isinstance(KvPair['Value'], list):
                Value = json.dumps(KvPair['Value'])
            else:
                Value = str(KvPair['Value'])

            try:
                Request = OpenApiModels.OpenApiRequest(query = OpenApiUtilClient.query({
                    'Namespace'    : Config['Space'],
                    'Key'          : Key,
                    'ExpirationTtl': KvPair.get('Ttl', 0)
                }), body = {'Value': Value})
                Client.call_api(Params, Request, Runtime)
                Response['Data'][Key] = {'code': 0}
            except Exception as errorMsg:
                Response['Data'][Key] = {'code': 500}

        return Response


def Delete(Cfg = None):
    import json

    if __name__ == '__main__':
        from  Merge import MergeCfg
    else:
        from .Merge import MergeCfg

    Config = {
        'Web'     : True,
        'Key'     : None,                # 记录の键, '' OR ['', '', ...]
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
        'Data'     : {}
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
                'key'      : Config['Key'] if isinstance(Config['Key'], list) else [Config['Key']]
            }
            return requests.post(Url, headers = Hed, data = json.dumps(Dat), timeout = 5).json()
        except Exception as errorMsg:
            Response['ErrorCode'] = -1
            Response['ErrorMsg']  = ''

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
            Runtime = UtilModels.RuntimeOptions(autoretry = True, max_attempts = 3, read_timeout = 10000, connect_timeout = 10000)
        except Exception as errorMsg:
            Response['ErrorCode'] = -1
            Response['ErrorMsg']  = ''
            return Response

        for Key in Config['Key'] if isinstance(Config['Key'], list) else [Config['Key']]:
            Key = str(Key)

            if len(Key) > 512:
                Response['Data'][Key] = {'code': 400}
                continue

            try:
                Request = OpenApiModels.OpenApiRequest(query = OpenApiUtilClient.query({
                    'Namespace': Config['Space'],
                    'Key'      : Key
                }))
                Client.call_api(Params, Request, Runtime)
                Response['Data'][Key] = {'code': 0}
            except Exception as errorMsg:
                if errorMsg.data.get('Code') in ['InvalidAccount.NotFound', 'InvalidNameSpace.NotFound', 'InvalidKey.NotFound']:
                    Response['Data'][Key] = {'code': 404}
                else:
                    Response['Data'][Key] = {'code': 500}

        return Response
