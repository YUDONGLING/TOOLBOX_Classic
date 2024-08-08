def __AliyunClient__(AK: str, SK: str, EndPoint: str, STSToken: str = None):
    from alibabacloud_tea_openapi import models as OpenApiModels
    from alibabacloud_tea_openapi.client import Client as OpenApiClient
    if STSToken:
        return OpenApiClient(OpenApiModels.Config(access_key_id = AK, access_key_secret = SK, endpoint = EndPoint, security_token = STSToken))
    else:
        return OpenApiClient(OpenApiModels.Config(access_key_id = AK, access_key_secret = SK, endpoint = EndPoint))


def __AliyunEndPoint__(Region: str = None, ProductCode: str = None, **ExtraFields):
    try:    Region = (Region or 'CN-HANGZHOU').lower()
    except: raise Exception('Invalid Region')

    try:    ProductCode = ProductCode.title()
    except: raise Exception('Invalid ProductCode')

    try:    ExtraFields = ExtraFields['ExtraFields']
    except: pass

    # 操作审计 Action Trail
    # Document: https://api.aliyun.com/product/Actiontrail
    if ProductCode == 'Actiontrail':
        if Region in ['cn-beijing', 'cn-chengdu', 'cn-guangzhou', 'cn-hangzhou', 'cn-heyuan', 'cn-huhehaote', 'cn-hongkong', 'cn-nanjing', 'cn-qingdao', 'cn-shanghai', 'cn-shenzhen', 'cn-wulanchabu', 'cn-zhangjiakou', 'ap-southeast-2', 'ap-southeast-5', 'ap-northeast-1', 'ap-southeast-3', 'ap-southeast-1', 'ap-northeast-2', 'ap-southeast-7', 'eu-central-1', 'eu-west-1', 'us-west-1', 'us-east-1', 'ap-south-1', 'me-east-1', 'cn-shanghai-finance-1']:
            return 'actiontrail.{Region}.aliyuncs.com'.format(Region = Region)
        raise Exception('Invalid Region')

    # API 网关 API Gateway
    # Document: https://api.aliyun.com/product/CloudAPI
    if ProductCode == 'Apigateway':
        if Region in ['cn-beijing', 'cn-chengdu', 'cn-guangzhou', 'cn-hangzhou', 'cn-heyuan', 'cn-huhehaote', 'cn-hongkong', 'cn-qingdao', 'cn-shanghai', 'cn-shenzhen', 'cn-wulanchabu', 'cn-zhangjiakou', 'ap-southeast-2', 'ap-southeast-5', 'ap-northeast-1', 'ap-southeast-3', 'ap-southeast-6', 'ap-southeast-1', 'ap-northeast-2', 'ap-southeast-7', 'eu-central-1', 'eu-west-1', 'us-west-1', 'us-east-1', 'ap-south-1', 'me-central-1', 'me-east-1', 'cn-hangzhou-finance', 'cn-shanghai-finance-1', 'cn-beijing-finance-1', 'cn-shenzhen-finance-1', 'cn-heyuan-acdr-1']:
            return 'apigateway.{Region}.aliyuncs.com'.format(Region = Region)
        raise Exception('Invalid Region')

    # 云账单 Billing
    # Document: https://api.aliyun.com/product/BssOpenApi
    if ProductCode == 'Billing':
        if Region in ['cn-beijing', 'cn-chengdu', 'cn-hangzhou', 'cn-huhehaote', 'cn-hongkong', 'cn-qingdao', 'cn-shanghai', 'cn-shenzhen', 'cn-wulanchabu', 'cn-zhangjiakou', 'cn-hangzhou-finance', 'cn-shanghai-finance-1', 'cn-beijing-finance-1', 'cn-shenzhen-finance-1']:
            return 'business.aliyuncs.com'
        if Region in ['ap-southeast-2', 'ap-southeast-5', 'ap-northeast-1', 'ap-southeast-3', 'ap-southeast-1', 'ap-northeast-2', 'eu-central-1', 'eu-west-1', 'us-west-1', 'us-east-1', 'ap-south-1', 'me-east-1']:
            return 'business.ap-southeast-1.aliyuncs.com'
        raise Exception('Invalid Region')

    # 数字证书管理服务（原SSL证书） Certificate Management Service
    # Document: https://api.aliyun.com/product/Cas
    if ProductCode == 'Cas':
        if Region in ['cn-hangzhou']:
            return 'cas.aliyuncs.com'
        if Region in ['ap-southeast-1', 'eu-central-1']:
            return 'cas.{Region}.aliyuncs.com'.format(Region = Region)
        raise Exception('Invalid Region')

    # 内容分发 CDN
    # Document: https://api.aliyun.com/product/Cdn
    if ProductCode == 'Cdn':
        if Region in ['cn-beijing', 'cn-chengdu', 'cn-hangzhou', 'cn-huhehaote', 'cn-hongkong', 'cn-qingdao', 'cn-shanghai', 'cn-shenzhen', 'cn-zhangjiakou', 'cn-hangzhou-finance', 'cn-shanghai-finance-1', 'cn-shenzhen-finance-1']:
            return 'cdn.aliyuncs.com'
        if Region in ['ap-southeast-2', 'ap-southeast-5', 'ap-northeast-1', 'ap-southeast-3', 'ap-southeast-1', 'eu-central-1', 'eu-west-1', 'us-west-1', 'us-east-1', 'ap-south-1', 'me-east-1']:
            return 'cdn.ap-southeast-1.aliyuncs.com'
        raise Exception('Invalid Region')

    # 云监控 Cloud Monitor
    # Document: https://api.aliyun.com/product/Cms
    if ProductCode == 'Cms':
        if Region in ['cn-beijing', 'cn-chengdu', 'cn-fuzhou', 'cn-guangzhou', 'cn-hangzhou', 'cn-heyuan', 'cn-huhehaote', 'cn-hongkong', 'cn-nanjing', 'cn-qingdao', 'cn-shanghai', 'cn-shenzhen', 'cn-wulanchabu', 'cn-zhangjiakou', 'ap-southeast-2', 'ap-southeast-5', 'ap-northeast-1', 'ap-southeast-3', 'ap-southeast-6', 'ap-southeast-1', 'ap-northeast-2', 'ap-southeast-7', 'cn-zhengzhou-jva', 'eu-central-1', 'eu-west-1', 'us-west-1', 'us-east-1', 'ap-south-1', 'me-central-1', 'me-east-1', 'cn-shanghai-finance-1', 'cn-beijing-finance-1', 'cn-shenzhen-finance-1']:
            return 'metrics.{Region}.aliyuncs.com'.format(Region = Region)
        raise Exception('Invalid Region')

    # 全站加速 DCDN (Dynamic Route for CDN)
    # Document: https://api.aliyun.com/product/Dcdn
    if ProductCode == 'Dcdn':
        if Region in ['cn-beijing', 'cn-chengdu', 'cn-hangzhou', 'cn-huhehaote', 'cn-hongkong', 'cn-qingdao', 'cn-shanghai', 'cn-shenzhen', 'cn-zhangjiakou', 'ap-southeast-2', 'ap-southeast-5', 'ap-northeast-1', 'ap-southeast-3', 'ap-southeast-1', 'eu-central-1', 'eu-west-1', 'us-west-1', 'us-east-1', 'ap-south-1', 'me-east-1', 'cn-hangzhou-finance', 'cn-shanghai-finance-1', 'cn-beijing-finance-1', 'cn-shenzhen-finance-1']:
            return 'dcdn.aliyuncs.com'
        raise Exception('Invalid Region')

    # 云解析 Cloud DNS
    # Document: https://api.aliyun.com/product/Alidns
    if ProductCode == 'Dns':
        if Region in ['cn-beijing', 'cn-chengdu', 'cn-hangzhou', 'cn-huhehaote', 'cn-hongkong', 'cn-shanghai', 'cn-shenzhen', 'cn-zhangjiakou', 'ap-southeast-2', 'ap-southeast-5', 'ap-northeast-1', 'ap-southeast-3', 'ap-southeast-1', 'eu-central-1', 'eu-west-1', 'us-west-1', 'us-east-1', 'ap-south-1', 'me-east-1', 'cn-hangzhou-finance', 'cn-shanghai-finance-1', 'cn-shenzhen-finance-1']:
            return 'alidns.{Region}.aliyuncs.com'.format(Region = Region)
        if Region in ['cn-qingdao', 'cn-wulanchabu', 'cn-beijing-finance-1']:
            return 'alidns.aliyuncs.com'
        raise Exception('Invalid Region')

    # 域名服务 Domain
    # Document: https://api.aliyun.com/product/Domain
    if ProductCode == 'Domain':
        if Region in ['cn-hangzhou']:
            return 'domain.aliyuncs.com'
        if Region in ['ap-southeast-1']:
            return 'domain-intl.aliyuncs.com'
        raise Exception('Invalid Region')

    # 数据传输 Data Transmission
    # Document: https://api.aliyun.com/product/Dts
    if ProductCode == 'Dts':
        if Region in ['cn-beijing', 'cn-chengdu', 'cn-hangzhou', 'cn-huhehaote', 'cn-hongkong', 'cn-qingdao', 'cn-shanghai', 'cn-shenzhen', 'cn-zhangjiakou', 'ap-southeast-2', 'ap-southeast-5', 'ap-northeast-1', 'ap-southeast-3', 'ap-southeast-1', 'eu-central-1', 'eu-west-1', 'us-west-1', 'us-east-1', 'ap-south-1', 'me-east-1', 'cn-beijing-finance-1']:
            return 'dts.{Region}.aliyuncs.com'.format(Region = Region)
        if Region in ['cn-wulanchabu']:
            return 'dts.aliyuncs.com'
        if Region in ['cn-hangzhou-finance', 'cn-shanghai-finance-1', 'cn-shenzhen-finance-1']:
            return 'dts.cn-hangzhou.aliyuncs.com'
        raise Exception('Invalid Region')

    # 云服务器 Elastic Compute Service
    # Document: https://api.aliyun.com/product/Ecs
    if ProductCode == 'Ecs':
        if Region in ['cn-beijing', 'cn-chengdu', 'cn-fuzhou', 'cn-guangzhou', 'cn-hangzhou', 'cn-heyuan', 'cn-huhehaote', 'cn-hongkong', 'cn-nanjing', 'cn-qingdao', 'cn-shanghai', 'cn-shenzhen', 'cn-wulanchabu', 'cn-wuhan-lr', 'cn-zhangjiakou', 'ap-southeast-2', 'ap-southeast-5', 'ap-northeast-1', 'ap-southeast-3', 'ap-southeast-6', 'ap-southeast-1', 'ap-northeast-2', 'ap-southeast-7', 'cn-zhengzhou-jva', 'eu-central-1', 'eu-west-1', 'us-west-1', 'us-east-1', 'ap-south-1', 'me-central-1', 'me-east-1', 'cn-shanghai-finance-1', 'cn-beijing-finance-1', 'cn-shenzhen-finance-1']:
            return 'ecs.{Region}.aliyuncs.com'.format(Region = Region)
        if Region in ['cn-hangzhou-finance']:
            return 'ecs.aliyuncs.com'
        raise Exception('Invalid Region')

    # 函数计算 Function Compute
    # Document: https://api.aliyun.com/product/FC-Open
    if ProductCode == 'Fc':
        if Region in ['cn-beijing', 'cn-chengdu', 'cn-hangzhou', 'cn-huhehaote', 'cn-hongkong', 'cn-qingdao', 'cn-shanghai', 'cn-shenzhen', 'cn-zhangjiakou', 'ap-southeast-2', 'ap-southeast-5', 'ap-northeast-1', 'ap-southeast-3', 'ap-southeast-1', 'ap-northeast-2', 'ap-southeast-7', 'eu-central-1', 'eu-west-1', 'us-west-1', 'us-east-1', 'ap-south-1']:
            return 'fc.{Region}.aliyuncs.com'.format(Region = Region)
        if Region in ['cn-hangzhou-finance']:
            if ExtraFields.get('AccountId'): return '{AccountId}.{Region}.fc.aliyuncs.com'.format(AccountId = ExtraFields.get('AccountId'), Region = Region)
            else: raise Exception('Require AccountId')
        raise Exception('Invalid Region')

    # 移动解析 HttpDNS
    # Document: https://api.aliyun.com/product/Httpdns
    if ProductCode == 'Httpdns':
        if Region in ['cn-hangzhou']:
            return 'httpdns-api.aliyuncs.com'
        if Region in ['ap-southeast-1']:
            return 'httpdns.ap-southeast-1.aliyuncs.com'
        raise Exception('Invalid Region')

    # 智能媒体管理 Intelligent Media Management
    # Document: https://api.aliyun.com/product/Imm
    if ProductCode == 'Imm':
        if Region in ['cn-beijing', 'cn-chengdu', 'cn-guangzhou', 'cn-hangzhou', 'cn-hongkong', 'cn-qingdao', 'cn-shanghai', 'cn-shenzhen', 'cn-zhangjiakou', 'ap-southeast-2', 'ap-southeast-5', 'ap-southeast-1', 'eu-central-1', 'eu-west-1', 'us-west-1', 'us-east-1', 'ap-south-1']:
            return 'imm.{Region}.aliyuncs.com'.format(Region = Region)
        raise Exception('Invalid Region')

    # 身份管理 RAM Identity Management Service
    # Document: https://api.aliyun.com/product/Ims
    if ProductCode == 'Ims':
        if Region in ['cn-hangzhou']:
            return 'ims.aliyuncs.com'
        raise Exception('Invalid Region')

    # 视频直播 Apsara Video Live
    # Document: https://api.aliyun.com/product/Live
    if ProductCode == 'Live':
        if Region in ['cn-beijing', 'cn-chengdu', 'cn-hangzhou', 'cn-huhehaote', 'cn-hongkong', 'cn-qingdao', 'cn-shanghai', 'cn-shenzhen', 'cn-wulanchabu', 'cn-zhangjiakou', 'ap-southeast-5', 'ap-northeast-1', 'ap-southeast-1', 'eu-central-1', 'ap-south-1', 'cn-hangzhou-finance', 'cn-shanghai-finance-1', 'cn-beijing-finance-1', 'cn-shenzhen-finance-1']:
            return 'live.aliyuncs.com'
        if Region in ['ap-southeast-2', 'ap-southeast-3', 'eu-west-1', 'us-west-1', 'us-east-1', 'me-east-1']:
            return 'live.ap-southeast-1.aliyuncs.com'
        raise Exception('Invalid Region')

    # 对象存储 Oss (Object Storage Service)
    # Document: https://api.aliyun.com/product/Oss
    if ProductCode == 'Oss':
        EndPoint = '.aliyuncs.com'

        if Region in ['cn-beijing', 'cn-chengdu', 'cn-fuzhou', 'cn-guangzhou', 'cn-hangzhou', 'cn-heyuan', 'cn-huhehaote', 'cn-hongkong', 'cn-nanjing', 'cn-qingdao', 'cn-shanghai', 'cn-shenzhen', 'cn-wulanchabu', 'cn-wuhan-lr', 'cn-zhangjiakou', 'ap-southeast-2', 'ap-southeast-5', 'ap-northeast-1', 'ap-southeast-3', 'ap-southeast-6', 'ap-southeast-1', 'ap-northeast-2', 'ap-southeast-7', 'eu-central-1', 'eu-west-1', 'us-west-1', 'us-east-1', 'ap-south-1', 'me-east-1']:
            if ExtraFields.get('Accelerate'):
                if ExtraFields.get('Overseas'): EndPoint = '-overseas' + EndPoint
                EndPoint = 'oss-accelerate' + EndPoint
            else:
                if ExtraFields.get('Internal'): EndPoint = '-internal' + EndPoint
                EndPoint = 'oss-{Region}'.format(Region = Region) + EndPoint

            if ExtraFields.get('S3'): EndPoint = 's3.' + EndPoint

        if Region in ['cn-hzfinance', 'cn-shanghai-finance-1-pub', 'oss-cn-szfinance', 'oss-cn-beijing-finance-1-pub']:
            if ExtraFields.get('Internal'): EndPoint = '-internal' + EndPoint
            EndPoint = 'oss-{Region}'.format(Region = Region) + EndPoint

        if Region in ['cn-shanghai-finance-1', 'cn-beijing-finance-1', 'cn-shenzhen-finance-1']:
            EndPoint = 'oss-{Region}-internal'.format(Region = Region) + EndPoint

        if Region in ['cn-hangzhou-finance', 'cn-hzjbp']:
            EndPoint = 'oss-cn-hzjbp-b-console' + EndPoint

        if Region in ['cn-hzjbp']:
            EndPoint = ('oss-cn-hzjbp-a-internal' or 'oss-cn-hzjbp-b-internal') + EndPoint

        if EndPoint == '.aliyuncs.com':
            raise Exception('Invalid Region')
        else:
            return '{Bucket}.{EndPoint}'.format(Bucket = ExtraFields.get('Bucket'), EndPoint = EndPoint) if ExtraFields.get('Bucket') else EndPoint

    # P2P 内容分发 PCDN
    # Document: https://api.aliyun.com/product/Pcdn
    if ProductCode == 'Pcdn':
        if Region in ['cn-beijing', 'cn-chengdu', 'cn-hangzhou', 'cn-huhehaote', 'cn-hongkong', 'cn-qingdao', 'cn-shanghai', 'cn-shenzhen', 'cn-wulanchabu', 'cn-zhangjiakou', 'ap-southeast-2', 'ap-southeast-5', 'ap-northeast-1', 'ap-southeast-3', 'ap-southeast-1', 'eu-central-1', 'eu-west-1', 'us-west-1', 'us-east-1', 'ap-south-1', 'me-east-1', 'cn-hangzhou-finance', 'cn-shanghai-finance-1', 'cn-beijing-finance-1', 'cn-shenzhen-finance-1']:
            return 'pcdn.aliyuncs.com'
        raise Exception('Invalid Region')

    # 性能测试 Performance Testing
    # Document: https://api.aliyun.com/product/PTS
    if ProductCode == 'Pts':
        if Region in ['cn-beijing', 'cn-chengdu', 'cn-hangzhou', 'cn-huhehaote', 'cn-hongkong', 'cn-qingdao', 'cn-shanghai', 'cn-shenzhen', 'cn-zhangjiakou', 'ap-southeast-2', 'ap-southeast-5', 'ap-northeast-1', 'ap-southeast-3', 'ap-southeast-1', 'eu-central-1', 'eu-west-1', 'us-west-1', 'us-east-1', 'ap-south-1', 'me-east-1', 'cn-hangzhou-finance', 'cn-shanghai-finance-1', 'cn-beijing-finance-1', 'cn-shenzhen-finance-1']:
            return 'pts.aliyuncs.com'
        raise Exception('Invalid Region')

    # 云解析 Private Zone
    # Document: https://api.aliyun.com/product/Pvtz
    if ProductCode == 'Pvtz':
        if Region in ['cn-hangzhou', 'cn-qingdao', 'ap-southeast-2', 'ap-northeast-1', 'eu-west-1', 'us-west-1', 'us-east-1', 'ap-south-1', 'me-east-1', 'cn-hangzhou-finance', 'cn-shanghai-finance-1', 'cn-beijing-finance-1', 'cn-shenzhen-finance-1']:
            return 'pvtz.aliyuncs.com'
        raise Exception('Invalid Region')

    # 配额中心 Quota
    # Document: https://api.aliyun.com/product/Quotas
    if ProductCode == 'Quota':
        if Region in ['cn-beijing', 'cn-chengdu', 'cn-hangzhou', 'cn-huhehaote', 'cn-hongkong', 'cn-qingdao', 'cn-shanghai', 'cn-shenzhen', 'cn-wulanchabu', 'cn-zhangjiakou', 'ap-southeast-2', 'ap-southeast-5', 'ap-northeast-1', 'ap-southeast-3', 'ap-southeast-1', 'eu-central-1', 'eu-west-1', 'us-west-1', 'us-east-1', 'ap-south-1', 'me-east-1', 'cn-hangzhou-finance', 'cn-shanghai-finance-1', 'cn-shenzhen-finance-1']:
            return 'quotas.aliyuncs.com'
        raise Exception('Invalid Region')

    # 访问控制 Resource Access Management
    # Document: https://api.aliyun.com/product/Ram
    if ProductCode == 'Ram':
        if Region in ['cn-beijing', 'cn-chengdu', 'cn-hangzhou', 'cn-huhehaote', 'cn-hongkong', 'cn-qingdao', 'cn-shanghai', 'cn-shenzhen', 'cn-zhangjiakou', 'ap-southeast-2', 'ap-southeast-5', 'ap-northeast-1', 'ap-southeast-3', 'ap-southeast-1', 'eu-central-1', 'eu-west-1', 'us-west-1', 'us-east-1', 'ap-south-1', 'me-east-1', 'cn-hangzhou-finance', 'cn-shanghai-finance-1', 'cn-beijing-finance-1', 'cn-shenzhen-finance-1']:
            return 'ram.aliyuncs.com'
        raise Exception('Invalid Region')

    # 安全加速 SCDN
    # Document: https://api.aliyun.com/product/Scdn
    if ProductCode == 'Scdn':
        if Region in ['cn-beijing', 'cn-chengdu', 'cn-hangzhou', 'cn-huhehaote', 'cn-hongkong', 'cn-qingdao', 'cn-shanghai', 'cn-shenzhen', 'cn-zhangjiakou', 'ap-southeast-2', 'ap-southeast-5', 'ap-northeast-1', 'ap-southeast-3', 'ap-southeast-1', 'eu-central-1', 'eu-west-1', 'us-west-1', 'us-east-1', 'ap-south-1', 'me-east-1', 'cn-hangzhou-finance', 'cn-shanghai-finance-1', 'cn-beijing-finance-1', 'cn-shenzhen-finance-1']:
            return 'scdn.aliyuncs.com'
        raise Exception('Invalid Region')
    
    # 日志服务 Simple Log Service
    # Document: https://api.aliyun.com/product/Sls
    if ProductCode == 'Sls':
        if Region in ['cn-beijing', 'cn-chengdu', 'cn-fuzhou', 'cn-guangzhou', 'cn-hangzhou', 'cn-heyuan', 'cn-huhehaote', 'cn-hongkong', 'cn-nanjing', 'cn-qingdao', 'cn-shanghai', 'cn-shenzhen', 'cn-wulanchabu', 'cn-zhangjiakou', 'ap-southeast-2', 'ap-southeast-5', 'ap-northeast-1', 'ap-southeast-3', 'ap-southeast-6', 'ap-southeast-1', 'ap-northeast-2', 'ap-southeast-7', 'eu-central-1', 'eu-west-1', 'us-west-1', 'us-east-1', 'ap-south-1', 'me-central-1', 'me-east-1']:
            return '{Region}.log.aliyuncs.com'.format(Region = Region)
        raise Exception('Invalid Region')
    
    # 安全令牌 Security Token Service
    # Document: https://api.aliyun.com/product/Sts
    if ProductCode == 'Sts':
        if Region in ['cn-beijing', 'cn-chengdu', 'cn-fuzhou', 'cn-guangzhou', 'cn-hangzhou', 'cn-heyuan', 'cn-huhehaote', 'cn-hongkong', 'cn-nanjing', 'cn-qingdao', 'cn-shanghai', 'cn-shenzhen', 'cn-wulanchabu', 'cn-wuhan-lr', 'cn-zhangjiakou', 'ap-southeast-2', 'ap-southeast-5', 'ap-northeast-1', 'ap-southeast-3', 'ap-southeast-1', 'ap-northeast-2', 'ap-southeast-7', 'eu-central-1', 'eu-west-1', 'us-west-1', 'us-east-1', 'ap-south-1', 'me-central-1', 'me-east-1', 'cn-shanghai-finance-1', 'cn-beijing-finance-1']:
            return 'sts.{Region}.aliyuncs.com'.format(Region = Region)
        if Region in ['cn-hangzhou-finance', 'cn-shenzhen-finance-1']:
            return 'sts.aliyuncs.com'
        raise Exception('Invalid Region')

    # 轻量应用服务器 Simple Application Server
    # Document: https://api.aliyun.com/product/SWAS-OPEN
    if ProductCode == 'Swas':
        if Region in ['cn-qingdao', 'cn-beijing', 'cn-zhangjiakou', 'cn-huhehaote', 'cn-wulanchabu', 'cn-hangzhou', 'cn-shanghai', 'cn-nanjing', 'cn-fuzhou', 'cn-shenzhen', 'cn-heyuan', 'cn-guangzhou', 'cn-wuhan-lr', 'ap-southeast-2', 'ap-southeast-6', 'ap-northeast-2', 'ap-southeast-3', 'ap-northeast-1', 'ap-southeast-7', 'cn-chengdu', 'ap-southeast-1', 'ap-southeast-5', 'cn-hongkong', 'eu-central-1', 'us-east-1', 'us-west-1', 'eu-west-1', 'ap-south-1']:
            return 'swas.{Region}.aliyuncs.com'.format(Region = Region)
        raise Exception('Invalid Region')

    # 云工单 Ticket
    # Document: https://api.aliyun.com/product/Workorder
    if ProductCode == 'Workorder':
        if Region in ['cn-beijing', 'cn-chengdu', 'cn-hangzhou', 'cn-huhehaote', 'cn-hongkong', 'cn-qingdao', 'cn-shanghai', 'cn-shenzhen', 'cn-zhangjiakou', 'ap-southeast-2', 'ap-southeast-5', 'ap-southeast-3', 'eu-central-1', 'eu-west-1', 'us-west-1', 'us-east-1', 'ap-south-1', 'me-east-1', 'cn-hangzhou-finance', 'cn-shanghai-finance-1', 'cn-beijing-finance-1', 'cn-shenzhen-finance-1']:
            return 'workorder.aliyuncs.com'
        if Region in ['ap-northeast-1', 'ap-southeast-1']:
            return 'workorder.{Region}.aliyuncs.com'.format(Region = Region)
        raise Exception('Invalid Region')

    raise Exception('Invalid ProductCode')


def __AliyunOssSign__(Method: str, Url: str, Expires: int, AK: str, SK: str, Region: str, Bucket: str, STSToken: str = None, Version: int = None):
    '''
    The Url Should Startwith '/',
    Return Signed Url Startwith '/'
    '''

    import hmac
    import time
    import base64
    import hashlib
    import urllib.parse

    if Version == 1:
        if Expires < time.time(): Expires += int(time.time())

        if STSToken: StringToSign = f'{Method}\n\n\n{Expires}\n/{Bucket}{Url}&security-token={STSToken}' if '?' in Url else f'{Method}\n\n\n{Expires}\n/{Bucket}{Url}?security-token={STSToken}'
        else:        StringToSign = f'{Method}\n\n\n{Expires}\n/{Bucket}{Url}'

        Signature = urllib.parse.quote(base64.b64encode(hmac.new(SK.encode('utf-8'), StringToSign.encode('utf-8'), hashlib.sha1).digest()).decode(), safe = '')

        if STSToken: return Url + ('&' if '?' in Url else '?') + f'OSSAccessKeyId={AK}&Expires={Expires}&Signature={Signature}&security-token={urllib.parse.quote(STSToken, safe = "")}'
        else:        return Url + ('&' if '?' in Url else '?') + f'OSSAccessKeyId={AK}&Expires={Expires}&Signature={Signature}'

    else:
        Expires    = min(604800, Expires)
        Now        = time.gmtime()
        Key, Query = Url.split('?') if '?' in Url else (Url, '')

        Param = {
            'x-oss-signature-version': 'OSS4-HMAC-SHA256',
            'x-oss-credential'       : f'{AK}/{time.strftime("%Y%m%d", Now)}/{Region}/oss/aliyun_v4_request',
            'x-oss-date'             : time.strftime("%Y%m%dT%H%M%SZ", Now),
            'x-oss-expires'          : str(Expires)
        }
        if STSToken: Param['x-oss-security-token'] = STSToken

        for QueryKey, QueryValue in [Query.split('=', 1) if '=' in Query else (Query, '') for Query in Query.split('&')]:
            Param[QueryKey] = QueryValue
        Param = dict(sorted(Param.items(), key=lambda x: x[0]))

        Query = ''
        for QueryKey, QueryValue in Param.items():
            if QueryValue: Query += '%s=%s&' % (urllib.parse.quote(QueryKey, safe=''), urllib.parse.quote(QueryValue, safe=''))
            elif QueryKey: Query += '%s&' % urllib.parse.quote(QueryKey, safe='')
        Query = Query[:-1]

        Sign = hmac.new(hmac.new(hmac.new(hmac.new(hmac.new(f'aliyun_v4{SK}'.encode(), time.strftime('%Y%m%d', Now).encode(), hashlib.sha256).digest(), Region.encode(), hashlib.sha256).digest(), 'oss'.encode(), hashlib.sha256).digest(), 'aliyun_v4_request'.encode(), hashlib.sha256).digest(), ('OSS4-HMAC-SHA256\n%s\n%s\n%s' % (Param['x-oss-date'], Param['x-oss-credential'].removeprefix(f'{AK}/'), hashlib.sha256(f'{Method}\n/{Bucket}{Key}\n{Query}\n\n\nUNSIGNED-PAYLOAD'.encode()).hexdigest())).encode(), hashlib.sha256).hexdigest()
        return f'{Key}?{Query}&x-oss-signature={Sign}'


def __AliyunOssBucket__(AK: str, SK: str, Region: str, Bucket: str, Endpoint: str = None, STSToken: str = None, Timeout: int = None, Version: int = None):
    '''
    The Endpoint Should Include BucketName if Needed
    '''
    if STSToken:
        from oss2 import StsAuth
        Auth = StsAuth(AK, SK, STSToken, auth_version = 'v1' if Version == 1 else 'v4')
    elif Version == 1:
        from oss2 import Auth as BaseAuth
        Auth = BaseAuth(AK, SK)
    else:
        try: from oss2 import AuthV4 as BaseAuth
        except ImportError: from oss2 import Auth as BaseAuth
        Auth = BaseAuth(AK, SK)

    from oss2 import Bucket as OssBucket
    return OssBucket(
        auth            = Auth,
        region          = Region,
        bucket_name     = Bucket,
        endpoint        = Endpoint or 'oss-%s.aliyuncs.com' % Region,
        is_cname        = True if Endpoint else False,
        connect_timeout = Timeout
    )


def __AliyunOssService__(AK: str, SK: str, Region: str, Endpoint: str = None, STSToken: str = None, Timeout: int = None, Version: int = None):
    '''
    The Endpoint Should Use Aliyun Default Endpoint Only, No Custom CNAME Endpoint
    '''
    if STSToken:
        from oss2 import StsAuth
        Auth = StsAuth(AK, SK, STSToken, auth_version = 'v1' if Version == 1 else 'v4')
    elif Version == 1:
        from oss2 import Auth as BaseAuth
        Auth = BaseAuth(AK, SK)
    else:
        try: from oss2 import AuthV4 as BaseAuth
        except ImportError: from oss2 import Auth as BaseAuth
        Auth = BaseAuth(AK, SK)

    from oss2 import Service as OssService
    return OssService(
        auth            = Auth,
        region          = Region,
        endpoint        = Endpoint or 'oss-%s.aliyuncs.com' % Region,
        connect_timeout = Timeout
    )
