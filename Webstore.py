def Get(Cfg = None):
    import json
    import time
    import requests

    if __name__ == '__main__':
        from   Merge import MergeCfg
        from  Aliyun import __AliyunClient__, __AliyunEndPoint__
    else:
        from  .Merge import MergeCfg
        from .Aliyun import __AliyunClient__, __AliyunEndPoint__

    Config = {
        'Web'     : True,
        'Key'     : None,                # 记录の键, '' OR ['', '', ...]
        'Space'   : 'sample-storage',    # 记录の域
        'AK'      : 'AccessKey Id',
        'SK'      : 'AccessKey Secret',
        'STSToken': '',                  # 临时性凭证 (可留空)
        'Region'  : 'cn-hangzhou'        # 服务接入点 (可留空)
    }
    Config = MergeCfg(Config, Cfg)

    Response = {
        'ErrorCode': 0,
        'ErrorMsg' : '',
        'Data'     : {}
    }

    if Config['Web']:
        try:
            Url = 'http://storage.edge-routine.yudongling.net.w.cdngslb.com/'
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
                try:    Rsp['Data'][Key]['value'] = json.loads(Value['value'])
                except: pass

            return Rsp
        except Exception as errorMsg:
            Response['ErrorCode'] = -1
            Response['ErrorMsg']  = ''

        return Response

    if not Config['Web']:
        import asyncio

        from alibabacloud_tea_util import models as UtilModels
        from alibabacloud_tea_openapi import models as OpenApiModels
        from alibabacloud_openapi_util.client import Client as OpenApiUtilClient

        # 限制并发请求数
        MaxReq = 16; Semaphore = asyncio.Semaphore(MaxReq)

        async def __AsyncReq__(Key, Client, Params, Runtime):
            Key = str(Key)

            if len(Key) > 512:
                return Key, {'code': 400, 'value': ''}

            try:
                async with Semaphore:
                    Request = OpenApiModels.OpenApiRequest(query=OpenApiUtilClient.query({
                        'Namespace': Config['Space'],
                        'Key'      : Key
                    }))
                    Result = await Client.call_api_async(Params, Request, Runtime)

                Exp, Val = Result['body']['Value'].split('|', 1); Exp = int(Exp)
                if Exp != -1 and Exp < time.time(): return Key, {'code': 404, 'value': ''}

                try:    return Key, {'code': 0, 'value': json.loads(Val)}
                except: return Key, {'code': 0, 'value': Val}
            except Exception as errorMsg:
                if errorMsg.data.get('Code') in ['InvalidKey.NotFound']:
                    return Key, {'code': 404, 'value': ''}
                else:
                    return Key, {'code': 500, 'value': ''}

        async def __AsyncMain__():
            try:
                Client  = __AliyunClient__(AK = Config['AK'], SK = Config['SK'], STSToken = Config['STSToken'], EndPoint = __AliyunEndPoint__(Config['Region'], 'Dcdn'))
                Params  = OpenApiModels.Params(
                    action        = 'GetDcdnKv',
                    version       = '2018-01-15',
                    protocol      = 'HTTP',
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

            Key    = Config['Key'] if isinstance(Config['Key'], list) else [Config['Key']]
            Result = await asyncio.gather(*[__AsyncReq__(_Key, Client, Params, Runtime) for _Key in Key])

            for Key, Data in Result: Response['Data'][Key] = Data
            return Response

        return asyncio.run(__AsyncMain__())


def Put(Cfg = None):
    import json
    import time
    import requests

    if __name__ == '__main__':
        from   Merge import MergeCfg
        from  Aliyun import __AliyunClient__, __AliyunEndPoint__
    else:
        from  .Merge import MergeCfg
        from .Aliyun import __AliyunClient__, __AliyunEndPoint__

    Config = {
        'Web'     : True,
        'Key'     : [],                  # 记录の键值对, Eg. { Key: 'Key', Value: 'Value', Ttl: 0, Expire: 1700000000 }
        'Space'   : 'sample-storage',    # 记录の域
        'AK'      : 'AccessKey Id',
        'SK'      : 'AccessKey Secret',
        'STSToken': '',                  # 临时性凭证 (可留空)
        'Region'  : 'cn-hangzhou'        # 服务接入点 (可留空)
    }
    Config = MergeCfg(Config, Cfg)

    Response = {
        'ErrorCode': 0,
        'ErrorMsg' : '',
        'Data'     : {}
    }

    if Config['Web']:
        Body = []
        for _ in Config['Key']:
            Info = { 'key'  : _['Key'] }

            if isinstance(_['Value'], str):
                Info['value'] = _['Value']
            elif isinstance(_['Value'], dict) or isinstance(_['Value'], list):
                Info['value'] = json.dumps(_['Value'], ensure_ascii = False)
            else:
                Info['value'] = str(_['Value'])

            if 'Ttl'    in _ and isinstance(_['Ttl']   , int): Info['ttl']    = _['Ttl']
            if 'Expire' in _ and isinstance(_['Expire'], int): Info['expire'] = _['Expire']

            Body.append(Info)

        try:
            Url = 'http://storage.edge-routine.yudongling.net.w.cdngslb.com/'
            Hed = {
                'Content-Type': 'application/json',
                'Host'        : 'storage.edge-routine.yudongling.net'
            }
            Dat = {
                'action'   : 'put',
                'namespace': Config['Space'],
                'key'      : Body
            }
            return requests.post(Url, headers = Hed, data = json.dumps(Dat), timeout = 5).json()
        except Exception as errorMsg:
            Response['ErrorCode'] = -1
            Response['ErrorMsg']  = ''

        return Response

    if not Config['Web']:
        import asyncio

        from alibabacloud_tea_util import models as UtilModels
        from alibabacloud_tea_openapi import models as OpenApiModels
        from alibabacloud_openapi_util.client import Client as OpenApiUtilClient

        # 限制并发请求数
        MaxReq = 16; Semaphore = asyncio.Semaphore(MaxReq)

        async def __AsyncReq__(KeyVal, Client, Params, Runtime):
            Key = str(KeyVal['Key'])

            if len(Key) > 512:
                return Key, {'code': 400 }

            Expire = -1
            if 'Expire' in KeyVal and isinstance(KeyVal['Expire'], int) and KeyVal['Expire'] > 0:
                Expire = KeyVal['Expire']
            elif 'Ttl'  in KeyVal and isinstance(KeyVal['Ttl']   , int) and KeyVal['Ttl']    > 0:
                Expire = int(time.time() + KeyVal['Ttl'])

            if isinstance(KeyVal['Value'], str):
                Value = KeyVal['Value']
            elif isinstance(KeyVal['Value'], dict) or isinstance(KeyVal['Value'], list):
                Value = json.dumps(KeyVal['Value'], ensure_ascii = False)
            else:
                Value = str(KeyVal['Value'])

            try:
                async with Semaphore:
                    if Expire == -1:
                        Request = OpenApiModels.OpenApiRequest(query=OpenApiUtilClient.query({
                            'Namespace': Config['Space'],
                            'Key'      : Key
                        }), body = {'Value': f'{Expire}|{Value}'})
                    else:
                        Request = OpenApiModels.OpenApiRequest(query=OpenApiUtilClient.query({
                            'Namespace' : Config['Space'],
                            'Key'       : Key,
                            'Expiration': Expire + 30
                        }), body = {'Value': f'{Expire}|{Value}'})
                    await Client.call_api_async(Params, Request, Runtime)

                return Key, {'code': 0 }
            except Exception as errorMsg:
                return Key, {'code': 500 }

        async def __AsyncMain__():
            try:
                Client  = __AliyunClient__(AK = Config['AK'], SK = Config['SK'], STSToken = Config['STSToken'], EndPoint = __AliyunEndPoint__(Config['Region'], 'Dcdn'))
                Params  = OpenApiModels.Params(
                    action        = 'PutDcdnKv',
                    version       = '2018-01-15',
                    protocol      = 'HTTP',
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

            KeyVal = Config['Key'] if isinstance(Config['Key'], list) else [Config['Key']]
            Result = await asyncio.gather(*[__AsyncReq__(_KeyVal, Client, Params, Runtime) for _KeyVal in KeyVal])

            for Key, Data in Result: Response['Data'][Key] = Data
            return Response

        return asyncio.run(__AsyncMain__())


def Delete(Cfg = None):
    import json
    import requests

    if __name__ == '__main__':
        from   Merge import MergeCfg
        from  Aliyun import __AliyunClient__, __AliyunEndPoint__
    else:
        from  .Merge import MergeCfg
        from .Aliyun import __AliyunClient__, __AliyunEndPoint__

    Config = {
        'Web'     : True,
        'Key'     : None,                # 记录の键, '' OR ['', '', ...]
        'Space'   : 'sample-storage',    # 记录の域
        'AK'      : 'AccessKey Id',
        'SK'      : 'AccessKey Secret',
        'STSToken': '',                  # 临时性凭证 (可留空)
        'Region'  : 'cn-hangzhou'        # 服务接入点 (可留空)
    }
    Config = MergeCfg(Config, Cfg)

    Response = {
        'ErrorCode': 0,
        'ErrorMsg' : '',
        'Data'     : {}
    }

    if Config['Web']:
        try:
            Url = 'http://storage.edge-routine.yudongling.net.w.cdngslb.com/'
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
        import asyncio

        from alibabacloud_tea_util import models as UtilModels
        from alibabacloud_tea_openapi import models as OpenApiModels
        from alibabacloud_openapi_util.client import Client as OpenApiUtilClient

        # 限制并发请求数
        MaxReq = 16; Semaphore = asyncio.Semaphore(MaxReq)

        async def __AsyncReq__(Key, Client, Params, Runtime):
            Key = str(Key)

            if len(Key) > 512:
                return Key, {'code': 400 }

            try:
                async with Semaphore:
                    Request = OpenApiModels.OpenApiRequest(query=OpenApiUtilClient.query({
                        'Namespace': Config['Space'],
                        'Key'      : Key
                    }))
                    await Client.call_api_async(Params, Request, Runtime)

                return Key, {'code': 0 }
            except Exception as errorMsg:
                if errorMsg.data.get('Code') in ['InvalidAccount.NotFound', 'InvalidNameSpace.NotFound', 'InvalidKey.NotFound']:
                    return Key, {'code': 404 }
                else:
                    return Key, {'code': 500 }

        async def __AsyncMain__():
            try:
                Client  = __AliyunClient__(AK = Config['AK'], SK = Config['SK'], STSToken = Config['STSToken'], EndPoint = __AliyunEndPoint__(Config['Region'], 'Dcdn'))
                Params  = OpenApiModels.Params(
                    action        = 'DeleteDcdnKv',
                    version       = '2018-01-15',
                    protocol      = 'HTTP',
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

            Key    = Config['Key'] if isinstance(Config['Key'], list) else [Config['Key']]
            Result = await asyncio.gather(*[__AsyncReq__(_Key, Client, Params, Runtime) for _Key in Key])

            for Key, Data in Result: Response['Data'][Key] = Data
            return Response

        return asyncio.run(__AsyncMain__())
