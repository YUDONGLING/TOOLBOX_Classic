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


def Read(Cfg = None):
    import json

    from alibabacloud_tea_util import models as UtilModels
    from alibabacloud_tea_openapi import models as OpenApiModels
    from alibabacloud_openapi_util.client import Client as OpenApiUtilClient

    if __name__ == '__main__':
        from  Merge import MergeCfg
    else:
        from .Merge import MergeCfg

    Config = {
        'Key'     : 'sample',            # 记录
        'Zone'    : 'webstore.net',      # 域名
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
        'Zone'     : '',
        'Data'     : None,
        'TaskId'   : [],
        'BlockId'  : [],
        'Count'    : -1
    }

    # # 读取数据
    # try:
    #     RR     = Config['Key'].strip('.').lower()
    #     Domain = Config['Zone'].strip('.').lower()

    #     Response['Key']  = RR
    #     Response['Zone'] = Domain

    #     Client  = __AliyunClient__(AK = Config['AK'], SK = Config['SK'], STSToken = Config['STSToken'], EndPoint = __AliyunEndPoint__(Config['RegionId']))
    #     Params  = OpenApiModels.Params(
    #         action        = 'DescribeDomainRecords',
    #         version       = '2015-01-09',
    #         protocol      = 'HTTPS',
    #         method        = 'POST',
    #         auth_type     = 'AK',
    #         style         = 'RPC',
    #         pathname      = '/',
    #         req_body_type = 'json',
    #         body_type     = 'json'
    #     )
    #     Request = OpenApiModels.OpenApiRequest(query = OpenApiUtilClient.query({
    #         'DomainName' : f'{Domain}',
    #         'RRKeyWord'  : f'{RR}',
    #         'TypeKeyWord': f'txt',
    #         'PageSize'   : 500
    #     }))
    #     Runtime = UtilModels.RuntimeOptions(autoretry = True, max_attempts = 3, read_timeout = 10000, connect_timeout = 10000)
    # except Exception as errorMsg:
    #     Response['ErrorCode'] = 50001
    #     Response['ErrorMsg']  = f'Fail to init openapi model, {str(errorMsg).lower().rstrip(".")}'
    #     return Response

    # try:
    #     # 复制代码运行请自行打印 API 的返回值
    #     # 返回值为 Map 类型，可从 Map 中获得三类数据：响应体 body、响应头 headers、HTTP 返回的状态码 statusCode。
    #     Body = Client.call_api(Params, Request, Runtime)['body']['DomainRecords']['Record']
    # except Exception as errorMsg:
    #     Response['ErrorCode'] = 50002
    #     Response['ErrorMsg']  = f'Fail to request openapi model, {str(errorMsg.data.get("Message", errorMsg.message)).lower().rstrip(".")}'
    #     return Response

    # # 合并数据
    # try:
    #     Response['Count'] = len(Body)
    #     Response['BlockId'] = [_['RecordId'] for _ in Body]

    #     Data_String = ''.join([_['Value'] for _ in sorted(Body, key = lambda x: x['RR'].split('.')[0].zfill(5))]).replace(r'\"', r'"').replace(r"\\u", r"\u")
    #     Data = json.loads(Data_String)

    #     Response['Data'] = Data['Data']
    # except Exception as errorMsg:
    #     Response['ErrorCode'] = 50003
    #     Response['ErrorMsg']  = f'Fail to process response of openapi model, {str(errorMsg).lower().rstrip(".")}'
    #     return Response

    return Response


def Write(Cfg = None):
    import time
    import json

    from alibabacloud_tea_util import models as UtilModels
    from alibabacloud_tea_openapi import models as OpenApiModels
    from alibabacloud_openapi_util.client import Client as OpenApiUtilClient

    if __name__ == '__main__':
        from  Merge import MergeCfg
    else:
        from .Merge import MergeCfg

    Config = {
        'Data'    : None,                # 数据
        'Key'     : 'sample',            # 记录
        'Zone'    : 'webstore.net',      # 域名
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
        'Zone'     : '',
        'TaskId'   : [],
        'BlockId'  : [],
        'Count'    : -1
    }

    # # 构造数据
    # try:
    #     if type(Config['Data']) in [dict, list, tuple, str, int, float, bool, type(None)]:
    #         Data = {
    #             'Ts'  : Base36(int(time.time() * 1000)).encode(), # MS TIMESTAMP, BASE36
    #             'Data': Config['Data']
    #         }
    #     else:
    #         Data = {
    #             'Ts'  : Base36(int(time.time() * 1000)).encode(), # MS TIMESTAMP, BASE36
    #             'Data': str(Config['Data'])
    #         }
    # except Exception as errorMsg:
    #     Response['ErrorCode'] = 50001
    #     Response['ErrorMsg']  = f'Fail to process given data, {str(errorMsg).lower().rstrip(".")}'
    #     return Response

    # # 划分数据, 构造请求体
    # try:
    #     Data_ToString = json.dumps(Data, ensure_ascii = True).replace(r'"', r"\"").replace(r"\u", r"\\u")

    #     Record = []
    #     RR     = Config['Key'].strip('.').lower()
    #     Domain = Config['Zone'].strip('.').lower()

    #     Response['Key']  = RR
    #     Response['Zone'] = Domain

    #     for _ in range(0, len(Data_ToString) // 510 + 1):
    #         Record.append({
    #             'Type'  : f'txt',
    #             'Domain': f'{Domain}',
    #             'Value' : f'{Data_ToString[_ * 510 : _ * 510+510]}',
    #             'Rr'    : f'{_ + 1}.{RR}'
    #         })

    #     Response['Count'] = _ + 1
    # except Exception as errorMsg:
    #     Response['ErrorCode'] = 50002
    #     Response['ErrorMsg']  = f'Fail to process given data, {str(errorMsg).lower().rstrip(".")}'
    #     return Response

    # # 写入数据
    # try:
    #     Client  = __AliyunClient__(AK = Config['AK'], SK = Config['SK'], STSToken = Config['STSToken'], EndPoint = __AliyunEndPoint__(Config['RegionId']))
    #     Params  = OpenApiModels.Params(
    #         action        = 'OperateBatchDomain',
    #         version       = '2015-01-09',
    #         protocol      = 'HTTPS',
    #         method        = 'POST',
    #         auth_type     = 'AK',
    #         style         = 'RPC',
    #         pathname      = '/',
    #         req_body_type = 'json',
    #         body_type     = 'json'
    #     )
    #     Request = OpenApiModels.OpenApiRequest(query = OpenApiUtilClient.query({
    #         'Type'           : 'RR_ADD',
    #         'DomainRecordInfo': Record
    #     }))
    #     Runtime = UtilModels.RuntimeOptions(autoretry = True, max_attempts = 3, read_timeout = 10000, connect_timeout = 10000)
    # except Exception as errorMsg:
    #     Response['ErrorCode'] = 50003
    #     Response['ErrorMsg']  = f'Fail to init openapi model, {str(errorMsg).lower().rstrip(".")}'
    #     return Response

    # try:
    #     # 复制代码运行请自行打印 API 的返回值
    #     # 返回值为 Map 类型，可从 Map 中获得三类数据：响应体 body、响应头 headers、HTTP 返回的状态码 statusCode。
    #     TaskId           = Client.call_api(Params, Request, Runtime)['body']['TaskId']
    #     Response['TaskId'].append(str(TaskId))
    # except Exception as errorMsg:
    #     Response['ErrorCode'] = 50004
    #     Response['ErrorMsg']  = f'Fail to request openapi model, {str(errorMsg.data.get("Message", errorMsg.message)).lower().rstrip(".")}'
    #     return Response

    # Wait = 0
    # while Wait < 100:
    #     try:
    #         Client  = __AliyunClient__(AK = Config['AK'], SK = Config['SK'], STSToken = Config['STSToken'], EndPoint = __AliyunEndPoint__(Config['RegionId']))
    #         Params  = OpenApiModels.Params(
    #             action        = 'DescribeBatchResultCount',
    #             version       = '2015-01-09',
    #             protocol      = 'HTTPS',
    #             method        = 'POST',
    #             auth_type     = 'AK',
    #             style         = 'RPC',
    #             pathname      = '/',
    #             req_body_type = 'json',
    #             body_type     = 'json'
    #         )
    #         Request = OpenApiModels.OpenApiRequest(query = OpenApiUtilClient.query({
    #             'TaskId': TaskId
    #         }))
    #         Runtime = UtilModels.RuntimeOptions(autoretry = True, max_attempts = 3, read_timeout = 10000, connect_timeout = 10000)
    #     except Exception as errorMsg:
    #         Response['ErrorCode'] = 50005
    #         Response['ErrorMsg']  = f'Fail to init openapi model, {str(errorMsg).lower().rstrip(".")}'
    #         # return Response

    #     try:
    #         # 复制代码运行请自行打印 API 的返回值
    #         # 返回值为 Map 类型，可从 Map 中获得三类数据：响应体 body、响应头 headers、HTTP 返回的状态码 statusCode。
    #         Status = Client.call_api(Params, Request, Runtime)['body']['Status']
    #     except Exception as errorMsg:
    #         Response['ErrorCode'] = 50006
    #         Response['ErrorMsg']  = f'Fail to request openapi model, {str(errorMsg.data.get("Message", errorMsg.message)).lower().rstrip(".")}'
    #         # return Response
        
    #     if Status >= 1:
    #         break
    #     else:
    #         time.sleep(0.25); Wait += 1

    # try:
    #     Client  = __AliyunClient__(AK = Config['AK'], SK = Config['SK'], STSToken = Config['STSToken'], EndPoint = __AliyunEndPoint__(Config['RegionId']))
    #     Params  = OpenApiModels.Params(
    #         action        = 'DescribeBatchResultDetail',
    #         version       = '2015-01-09',
    #         protocol      = 'HTTPS',
    #         method        = 'POST',
    #         auth_type     = 'AK',
    #         style         = 'RPC',
    #         pathname      = '/',
    #         req_body_type = 'json',
    #         body_type     = 'json'
    #     )
    #     Request = OpenApiModels.OpenApiRequest(query = OpenApiUtilClient.query({
    #         'TaskId'  : TaskId,
    #         'PageSize': 1000
    #     }))
    #     Runtime = UtilModels.RuntimeOptions(autoretry = True, max_attempts = 3, read_timeout = 10000, connect_timeout = 10000)
    # except Exception as errorMsg:
    #     Response['ErrorCode'] = 50007
    #     Response['ErrorMsg']  = f'Fail to init openapi model, {str(errorMsg).lower().rstrip(".")}'
    #     return Response

    # try:
    #     # 复制代码运行请自行打印 API 的返回值
    #     # 返回值为 Map 类型，可从 Map 中获得三类数据：响应体 body、响应头 headers、HTTP 返回的状态码 statusCode。
    #     Body                = Client.call_api(Params, Request, Runtime)['body']['BatchResultDetails']['BatchResultDetail']
    #     Response['BlockId'] = [_['RecordId'] for _ in Body]
    # except Exception as errorMsg:
    #     Response['ErrorCode'] = 50008
    #     Response['ErrorMsg']  = f'Fail to request openapi model, {str(errorMsg.data.get("Message", errorMsg.message)).lower().rstrip(".")}'
    #     return Response

    return Response
