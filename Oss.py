class ProgressBar(object):
    def __init__(self, Name, Size):
        import threading

        from tqdm import tqdm

        self.pbar = tqdm(desc = Name, total = Size, unit = 'B', unit_scale = True)
        self.lock = threading.Lock()

    def __call__(self, Uploaded_Bytes, Total_Bytes):
        self.pbar.total = Total_Bytes or self.pbar.total
        self.pbar.update(Uploaded_Bytes - self.pbar.n)

    def full(self):
        self.pbar.update(self.pbar.total - self.pbar.n)

    def close(self):
        self.pbar.close()


def SignUrl(Cfg = None):
    if __name__ == '__main__':
        from  Merge import MergeCfg
        from  Aliyun import __AliyunOssSign__, __AliyunOssBucket__, __AliyunEndPoint__
    else:
        from .Merge import MergeCfg
        from .Aliyun import __AliyunOssSign__, __AliyunOssBucket__, __AliyunEndPoint__

    Config = {
        'Region'  : '',                 # 存储桶区域
        'Bucket'  : '',                 # 存储桶名称
        'Endpoint': None,               # 存储桶域名 或 __AliyunEndPoint__.ExtraField
        'Method'  : '',
        'Key'     : '',
        'Header'  : {},
        'Param'   : {},
        'Expires' : 3600,               # 签名过期 (秒)
        'Version' : None,               # 签名版本 (可留空), V1 或 V4
        'AK'      : 'AccessKey Id',
        'SK'      : 'AccessKey Secret',
        'STSToken': '',                 # 临时性凭证 (可留空)
    }
    Config = MergeCfg(Config, Cfg)

    Response = {
        'ErrorCode': 0,
        'ErrorMsg' : '',
        'Url'      : {
            'Http'   : '',
            'Https'  : '',
            'NoSheme': ''
        }
    }

    # Config Check
    # ① 需要提供 Bucket, Method
    # ② 签名版本不为 V1 时需要提供 Region
    if not all([Config['Bucket'], Config['Method']]):
        Response['ErrorCode'] = 40001
        Response['ErrorMsg']  = 'Missing Bucket or Method'
        return Response

    if Config['Version'] != 'V1' and not Config['Region']:
        Response['ErrorCode'] = 40002
        Response['ErrorMsg']  = 'Missing Region for Non-V1 Version Signature'
        return Response

    if isinstance(Config['Endpoint'], dict) and not 'Bucket' in Config['Endpoint']:
        Config['Endpoint']['Bucket'] = Config['Bucket']

    # Manual Sign, for Bucket Operation (Key == '' or '/+')
    if Config['Key'].removeprefix('/') == '':
        try:
            SignedUrl_WithoutEndpoint = __AliyunOssSign__(
                Method   = Config['Method'],
                Url      = '%s%s' % ('' if Config['Key'] else '/', Config['Key']),
                Expires  = Config['Expires'],
                AK       = Config['AK'],
                SK       = Config['SK'],
                Region   = Config['Region'],
                Bucket   = Config['Bucket'],
                STSToken = Config['STSToken'],
                Version  = Config['Version']
            )

            if isinstance(Config['Endpoint'], str):
                Endpoint = Config['Endpoint'].removeprefix('http://').removeprefix('https://').removeprefix('//')
            else:
                Endpoint = __AliyunEndPoint__(Config['Region'], 'Oss', ExtraFields = Config['Endpoint'])

            Response['Url']['NoSheme'] = f'{Endpoint}{SignedUrl_WithoutEndpoint}'
            Response['Url']['Https']   = f'https://{Response["Url"]["NoSheme"]}'
            Response['Url']['Http']    = f'http://{Response["Url"]["NoSheme"]}'
        except Exception as ErrorMsg:
            Response['ErrorCode'] = 50001
            Response['ErrorMsg']  = f'Failed to sign url, {str(ErrorMsg).lower()}'
    # Sign for Object
    else:
        try:
            Response['Url']['NoSheme'] = __AliyunOssBucket__(
                AK       = Config['AK'],
                SK       = Config['SK'],
                Region   = Config['Region'],
                Bucket   = Config['Bucket'],
                Endpoint = None if not Config['Endpoint'] else Config['Endpoint'] if isinstance(Config['Endpoint'], str) else __AliyunEndPoint__(Config['Region'], 'Oss', ExtraFields = Config['Endpoint']),
                STSToken = Config['STSToken'],
                Version  = Config['Version']
            ).sign_url(
                method = Config['Method'],
                key    = Config['Key'].removeprefix('/'),
                expires= Config['Expires'],
                headers= Config['Header'],
                params = Config['Param'],
                slash_safe = True
            ).removeprefix('http://').removeprefix('https://').removeprefix('//')
            Response['Url']['Https']   = f'https://{Response["Url"]["NoSheme"]}'
            Response['Url']['Http']    = f'http://{Response["Url"]["NoSheme"]}'
        except Exception as ErrorMsg:
            Response['ErrorCode'] = 50002
            Response['ErrorMsg']  = f'Failed to sign url, {str(ErrorMsg).lower()}'

    return Response


def GetObject(Cfg = None):
    from oss2 import Bucket
    from oss2 import AnonymousAuth
    from oss2.exceptions import NotFound

    if __name__ == '__main__':
        from  Merge import MergeCfg
        from  Aliyun import __AliyunOssBucket__, __AliyunEndPoint__
    else:
        from .Merge import MergeCfg
        from .Aliyun import __AliyunOssBucket__, __AliyunEndPoint__

    Config = {
        'Region'     : '',                 # 存储桶区域
        'Bucket'     : '',                 # 存储桶名称
        'Endpoint'   : None,               # 存储桶域名 或 __AliyunEndPoint__.ExtraField
        'Key'        : '',
        'Range'      : None,
        'Header'     : {},
        'Param'      : {},
        'Url'        : '',                 # 签名链接 (优先)
        'Folder'     : '',                 # 保存路径 (优先)
        'File'       : '',                 # 保存文件 (优先)
        'ProgressBar': False,
        'Version'    : None,               # 签名版本 (可留空), V1 或 V4
        'AK'         : 'AccessKey Id',
        'SK'         : 'AccessKey Secret',
        'STSToken'   : '',                 # 临时性凭证 (可留空)
    }
    Config = MergeCfg(Config, Cfg)

    Response = {
        'ErrorCode': 0,
        'ErrorMsg' : '',
        'Data'     : None
    }

    # Config Check
    # ① 需要提供 Bucket, Key; 或 Url
    # ② 签名版本不为 V1 时需要提供 Region
    if not all([Config['Bucket'], Config['Key']]) and not Config['Url']:
        Response['ErrorCode'] = 40001
        Response['ErrorMsg']  = 'Missing Bucket, Key or Url'
        return Response

    if not isinstance(Config['Key'], str) and not Config['Url']:
        Response['ErrorCode'] = 40002
        Response['ErrorMsg']  = 'Require Key as String'
        return Response

    if Config['Version'] != 'V1' and not Config['Region'] and not Config['Url']:
        Response['ErrorCode'] = 40003
        Response['ErrorMsg']  = 'Missing Region for Non-V1 Version Signature'
        return Response
    
    if isinstance(Config['Endpoint'], dict) and not 'Bucket' in Config['Endpoint']:
        Config['Endpoint']['Bucket'] = Config['Bucket']

    if Config['File']:
        try:
            import os
            os.makedirs(Config['Folder'] or '.', exist_ok = True)
            Path = os.path.join(Config['Folder'] or '.', Config['File'])
        except Exception as ErrorMsg:
            Response['ErrorCode'] = 50001
            Response['ErrorMsg']  = f'Failed to create folder, {str(ErrorMsg).lower()}'
            return Response
    else:
        Path = None

    Pbar = ProgressBar(Name = Path or Config['Key'], Size = 0) if Config['ProgressBar'] else None

    if Config['Url']:
        try:
            Bucket = Bucket(
                auth        = AnonymousAuth(),
                endpoint    = 'oss.aliyuncs.com',
                bucket_name = 'oss-aliyuncs-com'
            )
        except Exception as ErrorMsg:
            Response['ErrorCode'] = 50002
            Response['ErrorMsg']  = f'Failed to init bucket, {str(ErrorMsg).lower()}'
            return Response

        try:
            Response['Data'] = Bucket.get_object_with_url_to_file(
                sign_url          = Config['Url'],
                filename          = Path,
                byte_range        = Config['Range'],
                headers           = Config['Header'],
                progress_callback = Pbar
            ) if Path else Bucket.get_object_with_url(
                sign_url          = Config['Url'],
                byte_range        = Config['Range'],
                headers           = Config['Header'],
                progress_callback = Pbar
            )
        except NotFound:
            Response['ErrorCode'] = 40401
            Response['ErrorMsg']  = f'Failed to get object, object not exists'
            return Response
        except Exception as ErrorMsg:
            Response['ErrorCode'] = 50003
            Response['ErrorMsg']  = f'Failed to get object, {str(ErrorMsg).lower()}'
            return Response
    else:
        try:
            Bucket = __AliyunOssBucket__(
                AK       = Config['AK'],
                SK       = Config['SK'],
                Region   = Config['Region'],
                Bucket   = Config['Bucket'],
                Endpoint = None if not Config['Endpoint'] else Config['Endpoint'] if isinstance(Config['Endpoint'], str) else __AliyunEndPoint__(Config['Region'], 'Oss', ExtraFields = Config['Endpoint']),
                STSToken = Config['STSToken'],
                Version  = Config['Version']
            )
        except Exception as ErrorMsg:
            Response['ErrorCode'] = 50004
            Response['ErrorMsg']  = f'Failed to init bucket, {str(ErrorMsg).lower()}'
            return Response

        try:
            Response['Data'] = Bucket.get_object_to_file(
                key               = Config['Key'],
                filename          = Path,
                byte_range        = Config['Range'],
                headers           = Config['Header'],
                params            = Config['Param'],
                progress_callback = Pbar
            ) if Path else Bucket.get_object(
                key               = Config['Key'],
                byte_range        = Config['Range'],
                headers           = Config['Header'],
                params            = Config['Param'],
                progress_callback = Pbar
            )
        except NotFound:
            Response['ErrorCode'] = 40402
            Response['ErrorMsg']  = f'Failed to get object, object not exists'
            return Response
        except Exception as ErrorMsg:
            Response['ErrorCode'] = 50005
            Response['ErrorMsg']  = f'Failed to get object, {str(ErrorMsg).lower()}'
            return Response

    return Response


def PutObject(Cfg = None):
    import os

    from oss2 import Bucket
    from oss2 import AnonymousAuth

    if __name__ == '__main__':
        from  Merge import MergeCfg
        from  Aliyun import __AliyunOssBucket__, __AliyunEndPoint__
    else:
        from .Merge import MergeCfg
        from .Aliyun import __AliyunOssBucket__, __AliyunEndPoint__

    Config = {
        'Region'     : '',                 # 存储桶区域
        'Bucket'     : '',                 # 存储桶名称
        'Endpoint'   : None,               # 存储桶域名 或 __AliyunEndPoint__.ExtraField
        'Key'        : '',
        'Data'       : '',                 # 上传数据 (优先)
        'Header'     : {},
        'Url'        : '',                 # 签名链接 (优先)
        'Folder'     : '',
        'File'       : '',
        'ProgressBar': False,
        'Version'    : None,               # 签名版本 (可留空), V1 或 V4
        'AK'         : 'AccessKey Id',
        'SK'         : 'AccessKey Secret',
        'STSToken'   : '',                 # 临时性凭证 (可留空)
    }
    Config = MergeCfg(Config, Cfg)

    Response = {
        'ErrorCode': 0,
        'ErrorMsg' : '',
        'Data'     : None
    }

    # Config Check
    # ① 需要提供 Bucket, Key; 或 Url
    # ② 签名版本不为 V1 时需要提供 Region
    if not all([Config['Bucket'], Config['Key']]) and not Config['Url']:
        Response['ErrorCode'] = 40001
        Response['ErrorMsg']  = 'Missing Bucket, Key or Url'
        return Response

    if not isinstance(Config['Key'], str) and not Config['Url']:
        Response['ErrorCode'] = 40002
        Response['ErrorMsg']  = 'Require Key as String'
        return Response

    if Config['Version'] != 'V1' and not Config['Region'] and not Config['Url']:
        Response['ErrorCode'] = 40003
        Response['ErrorMsg']  = 'Missing Region for Non-V1 Version Signature'
        return Response
    
    if isinstance(Config['Endpoint'], dict) and not 'Bucket' in Config['Endpoint']:
        Config['Endpoint']['Bucket'] = Config['Bucket']

    if not Config['Data']:
        if not os.path.exists(os.path.join(Config['Folder'] or '.', Config['File'])):
            Response['ErrorCode'] = 40004
            Response['ErrorMsg']  = 'Missing File'
            return Response

    Pbar = ProgressBar(Name = os.path.join(Config['Folder'] or '.', Config['File']) or Config['Key'], Size = 0) if Config['ProgressBar'] else None

    if Config['Url']:
        try:
            Bucket = Bucket(
                auth        = AnonymousAuth(),
                endpoint    = 'oss.aliyuncs.com',
                bucket_name = 'oss-aliyuncs-com'
            )
        except Exception as ErrorMsg:
            Response['ErrorCode'] = 50002
            Response['ErrorMsg']  = f'Failed to init bucket, {str(ErrorMsg).lower()}'
            return Response

        try:
            Response['Data'] = Bucket.put_object_with_url(
                sign_url          = Config['Url'],
                data              = Config['Data'],
                headers           = Config['Header'],
                progress_callback = Pbar
            ) if Config['Data'] else Bucket.put_object_with_url_from_file(
                sign_url          = Config['Url'],
                filename          = os.path.join(Config['Folder'] or '.', Config['File']),
                headers           = Config['Header'],
                progress_callback = Pbar
            )
        except Exception as ErrorMsg:
            Response['ErrorCode'] = 50003
            Response['ErrorMsg']  = f'Failed to put object, {str(ErrorMsg).lower()}'
            return Response
    else:
        try:
            Bucket = __AliyunOssBucket__(
                AK       = Config['AK'],
                SK       = Config['SK'],
                Region   = Config['Region'],
                Bucket   = Config['Bucket'],
                Endpoint = None if not Config['Endpoint'] else Config['Endpoint'] if isinstance(Config['Endpoint'], str) else __AliyunEndPoint__(Config['Region'], 'Oss', ExtraFields = Config['Endpoint']),
                STSToken = Config['STSToken'],
                Version  = Config['Version']
            )
        except Exception as ErrorMsg:
            Response['ErrorCode'] = 50004
            Response['ErrorMsg']  = f'Failed to init bucket, {str(ErrorMsg).lower()}'
            return Response

        try:
            Response['Data'] = Bucket.put_object(
                key               = Config['Key'],
                data              = Config['Data'],
                headers           = Config['Header'],
                progress_callback = Pbar
            ) if Config['Data'] else Bucket.put_object_from_file(
                key               = Config['Key'],
                filename          = os.path.join(Config['Folder'] or '.', Config['File']),
                headers           = Config['Header'],
                progress_callback = Pbar
            )
        except Exception as ErrorMsg:
            Response['ErrorCode'] = 50005
            Response['ErrorMsg']  = f'Failed to put object, {str(ErrorMsg).lower()}'
            return Response

    return Response


def MultipartPutObject(Cfg = None):
    import os

    from oss2.models import PartInfo
    from oss2 import SizedFileAdapter
    from oss2 import determine_part_size as DeterminePartSize

    if __name__ == '__main__':
        from  Merge import MergeCfg
        from  Aliyun import __AliyunOssBucket__, __AliyunEndPoint__
    else:
        from .Merge import MergeCfg
        from .Aliyun import __AliyunOssBucket__, __AliyunEndPoint__

    Config = {
        'Region'     : '',                 # 存储桶区域
        'Bucket'     : '',                 # 存储桶名称
        'Endpoint'   : None,               # 存储桶域名 或 __AliyunEndPoint__.ExtraField
        'Key'        : '',
        'Header'     : {},
        'Folder'     : '',
        'File'       : '',
        'BlockSize'  : 1024 * 1024 * 10,   # 分片大小, In Bytes
        'ProgressBar': False,
        'Version'    : None,               # 签名版本 (可留空), V1 或 V4
        'AK'         : 'AccessKey Id',
        'SK'         : 'AccessKey Secret',
        'STSToken'   : '',                 # 临时性凭证 (可留空)
    }
    # 从qiniu upload 复制一下进度条的代码

    Config = MergeCfg(Config, Cfg)

    Response = {
        'ErrorCode': 0,
        'ErrorMsg' : '',
        'Data'     : None
    }

    # Config Check
    # ① 需要提供 Bucket, Key
    # ② 签名版本不为 V1 时需要提供 Region
    if not all([Config['Bucket'], Config['Key']]):
        Response['ErrorCode'] = 40001
        Response['ErrorMsg']  = 'Missing Bucket or Key'
        return Response

    if not isinstance(Config['Key'], str):
        Response['ErrorCode'] = 40002
        Response['ErrorMsg']  = 'Require Key as String'
        return Response

    if Config['Version'] != 'V1' and not Config['Region'] and not Config['Url']:
        Response['ErrorCode'] = 40003
        Response['ErrorMsg']  = 'Missing Region for Non-V1 Version Signature'
        return Response

    if isinstance(Config['Endpoint'], dict) and not 'Bucket' in Config['Endpoint']:
        Config['Endpoint']['Bucket'] = Config['Bucket']

    if not os.path.exists(os.path.join(Config['Folder'] or '.', Config['File'])):
        Response['ErrorCode'] = 40003
        Response['ErrorMsg']  = 'Missing File'
        return Response
    else:
        TotalSize = os.path.getsize(os.path.join(Config['Folder'] or '.', Config['File']))
        BlockSize = DeterminePartSize(TotalSize, preferred_size = Config['BlockSize'] if Config['BlockSize'] > 0 else None)

    Pbar = ProgressBar(Name = os.path.join(Config['Folder'] or '.', Config['File']) or Config['Key'], Size = TotalSize) if Config['ProgressBar'] else None

    try:
        Bucket = __AliyunOssBucket__(
            AK       = Config['AK'],
            SK       = Config['SK'],
            Region   = Config['Region'],
            Bucket   = Config['Bucket'],
            Endpoint = None if not Config['Endpoint'] else Config['Endpoint'] if isinstance(Config['Endpoint'], str) else __AliyunEndPoint__(Config['Region'], 'Oss', ExtraFields = Config['Endpoint']),
            STSToken = Config['STSToken'],
            Version  = Config['Version']
        )
    except Exception as ErrorMsg:
        Response['ErrorCode'] = 50001
        Response['ErrorMsg']  = f'Failed to init bucket, {str(ErrorMsg).lower()}'
        return Response

    try:
        Acl  = Config['Header'].pop('X-Oss-Object-Acl', None) # 移除 ACL, 在 CompleteMultipartUpload 时设置

        UploadId    = Bucket.init_multipart_upload(Config['Key'], headers = Config['Header']).upload_id
        UploadParts = []

        with open(os.path.join(Config['Folder'] or '.', Config['File']), 'rb') as File:
            PartNumber = 1
            Offset     = 0
            while Offset < TotalSize:
                NumToUpload = min(BlockSize, TotalSize - Offset)
                Result      = Bucket.upload_part(Config['Key'], UploadId, PartNumber, SizedFileAdapter(File, NumToUpload))
                UploadParts.append(PartInfo(PartNumber, Result.etag))
                Offset     += NumToUpload
                PartNumber += 1
                if Pbar: Pbar(Offset, TotalSize)
    except Exception as ErrorMsg:
        Response['ErrorCode'] = 50002
        Response['ErrorMsg']  = f'Failed to init multipart upload, {str(ErrorMsg).lower()}'
        return Response

    try:
        Response['Data'] = Bucket.complete_multipart_upload(
            key       = Config['Key'],
            upload_id = UploadId,
            parts     = UploadParts,
            headers   = {'X-Oss-Object-Acl': Acl} if Acl else None
        )
    except Exception as ErrorMsg:
        Response['ErrorCode'] = 50003
        Response['ErrorMsg']  = f'Failed to complete multipart upload, {str(ErrorMsg).lower()}'
        return Response

    return Response


def AppendObject(Cfg = None):
    from oss2.exceptions import NotFound

    if __name__ == '__main__':
        from  Merge import MergeCfg
        from  Aliyun import __AliyunOssBucket__, __AliyunEndPoint__
    else:
        from .Merge import MergeCfg
        from .Aliyun import __AliyunOssBucket__, __AliyunEndPoint__

    Config = {
        'Region'     : '',                 # 存储桶区域
        'Bucket'     : '',                 # 存储桶名称
        'Endpoint'   : None,               # 存储桶域名 或 __AliyunEndPoint__.ExtraField
        'Key'        : '',
        'Data'       : '',                 # 上传数据 (优先)
        'Header'     : {},
        'Param'      : {},
        'Folder'     : '',
        'File'       : '',
        'ProgressBar': False,
        'Version'    : None,               # 签名版本 (可留空), V1 或 V4
        'AK'         : 'AccessKey Id',
        'SK'         : 'AccessKey Secret',
        'STSToken'   : '',                 # 临时性凭证 (可留空)
    }
    Config = MergeCfg(Config, Cfg)

    Response = {
        'ErrorCode': 0,
        'ErrorMsg' : ''
    }

    # Config Check
    # ① 需要提供 Bucket, Key
    # ② 签名版本不为 V1 时需要提供 Region
    if not all([Config['Bucket'], Config['Key']]):
        Response['ErrorCode'] = 40001
        Response['ErrorMsg']  = 'Missing Bucket or Key'
        return Response

    if not isinstance(Config['Key'], str):
        Response['ErrorCode'] = 40002
        Response['ErrorMsg']  = 'Require Key as String'
        return Response

    if Config['Version'] != 'V1' and not Config['Region']:
        Response['ErrorCode'] = 40003
        Response['ErrorMsg']  = 'Missing Region for Non-V1 Version Signature'
        return Response

    if isinstance(Config['Endpoint'], dict) and not 'Bucket' in Config['Endpoint']:
        Config['Endpoint']['Bucket'] = Config['Bucket']

    if not Config['Data']:
        try:
            import os
            with open(os.path.join(Config['Folder'] if Config['Folder'] else '.', Config['File']), 'rb') as File:
                Config['Data'] = File.read()
        except Exception as ErrorMsg:
            Response['ErrorCode'] = 40003
            Response['ErrorMsg']  = 'Missing Data'
            return Response

    Pbar = ProgressBar(Name = Config['Key'], Size = 0) if Config['ProgressBar'] else None

    try:
        Bucket = __AliyunOssBucket__(
            AK       = Config['AK'],
            SK       = Config['SK'],
            Region   = Config['Region'],
            Bucket   = Config['Bucket'],
            Endpoint = None if not Config['Endpoint'] else Config['Endpoint'] if isinstance(Config['Endpoint'], str) else __AliyunEndPoint__(Config['Region'], 'Oss', ExtraFields = Config['Endpoint']),
            STSToken = Config['STSToken'],
            Version  = Config['Version']
        )
    except Exception as ErrorMsg:
        Response['ErrorCode'] = 50001
        Response['ErrorMsg']  = f'Failed to init bucket, {str(ErrorMsg).lower()}'
        return Response

    try:
        Position = Bucket.head_object(
            key     = Config['Key'],
            headers = Config['Header'],
            params  = Config['Param']
        ).content_length
    except NotFound:
        Position = 0
    except Exception as ErrorMsg:
        Response['ErrorCode'] = 50002
        Response['ErrorMsg']  = f'Failed to get append object start position, {str(ErrorMsg).lower()}'
        return Response

    try:
        Bucket.append_object(
            key               = Config['Key'],
            position          = Position,
            data              = Config['Data'],
            headers           = Config['Header'],
            progress_callback = Pbar
        )
    except Exception as ErrorMsg:
        Response['ErrorCode'] = 50003
        Response['ErrorMsg']  = f'Failed to append object, {str(ErrorMsg).lower()}'
        return Response

    return Response


def DeleteObject(Cfg = None):
    if __name__ == '__main__':
        from  Merge import MergeCfg
        from  Aliyun import __AliyunOssBucket__, __AliyunEndPoint__
    else:
        from .Merge import MergeCfg
        from .Aliyun import __AliyunOssBucket__, __AliyunEndPoint__

    Config = {
        'Region'  : '',                 # 存储桶区域
        'Bucket'  : '',                 # 存储桶名称
        'Endpoint': None,               # 存储桶域名 或 __AliyunEndPoint__.ExtraField
        'Key'     : None,
        'Header'  : {},
        'Param'   : {},
        'Version' : None,               # 签名版本 (可留空), V1 或 V4
        'AK'      : 'AccessKey Id',
        'SK'      : 'AccessKey Secret',
        'STSToken': '',                 # 临时性凭证 (可留空)
    }
    Config = MergeCfg(Config, Cfg)

    Response = {
        'ErrorCode': 0,
        'ErrorMsg' : '',
        'Key'      : []
    }

    # Config Check
    # ① 需要提供 Bucket, Key, 其中 Key 可以为字符串或列表
    # ② 签名版本不为 V1 时需要提供 Region
    if not all([Config['Bucket'], Config['Key']]):
        Response['ErrorCode'] = 40001
        Response['ErrorMsg']  = 'Missing Bucket or Key'
        return Response

    if not (isinstance(Config['Key'], str) or isinstance(Config['Key'], list)):
        Response['ErrorCode'] = 40002
        Response['ErrorMsg']  = 'Require Key as String or List'
        return Response

    if Config['Version'] != 'V1' and not Config['Region']:
        Response['ErrorCode'] = 40002
        Response['ErrorMsg']  = 'Missing Region for Non-V1 Version Signature'
        return Response
    
    if isinstance(Config['Endpoint'], dict) and not 'Bucket' in Config['Endpoint']:
        Config['Endpoint']['Bucket'] = Config['Bucket']

    try:
        Bucket = __AliyunOssBucket__(
            AK       = Config['AK'],
            SK       = Config['SK'],
            Region   = Config['Region'],
            Bucket   = Config['Bucket'],
            Endpoint = None if not Config['Endpoint'] else Config['Endpoint'] if isinstance(Config['Endpoint'], str) else __AliyunEndPoint__(Config['Region'], 'Oss', ExtraFields = Config['Endpoint']),
            STSToken = Config['STSToken'],
            Version  = Config['Version']
        )
    except Exception as ErrorMsg:
        Response['ErrorCode'] = 50001
        Response['ErrorMsg']  = f'Failed to init bucket, {str(ErrorMsg).lower()}'
        return Response

    try:
        if isinstance(Config['Key'], str):
            Bucket.delete_object(
                key     = Config['Key'],
                headers = Config['Header'],
                params  = Config['Param']
            )
            Response['Key'] = [Config['Key']]
        else:
            Response['Key'].extend(Bucket.batch_delete_objects(
                key_list = Config['Key'],
                headers  = Config['Header']
            ).deleted_keys)
    except Exception as ErrorMsg:
        Response['ErrorCode'] = 50002
        Response['ErrorMsg']  = f'Failed to delete object, {str(ErrorMsg).lower()}'
        return Response

    return Response
