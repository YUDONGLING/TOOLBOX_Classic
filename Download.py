def HeadFile(Cfg = None):
    import requests

    if __name__ == '__main__':
        from  Merge import MergeCfg
    else:
        from .Merge import MergeCfg

    Config = {
        'Url'     : '',
        'Header'  : {
            'Accept'    : '*/*',
            'Range'     : 'bytes=0-',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.41'
            },
        'Params'  : {},
        'Cookie'  : None,
        'Timeout' : 10,
        'Redirect': True,
    }
    Config = MergeCfg(Config, Cfg)

    Response = {
        'ErrorCode'    : 0,
        'ErrorMsg'     : '',
        'HttpCode'     : -1,
        'FirstUrl'     : '',
        'FinalUrl'     : '',
        'ContentType'  : '',
        'ContentLength': -1
    }

    try:
        Url                  = Config['Url']
        Response['FirstUrl'] = Url

        _ = requests.head(Url,
                          headers         = Config['Header'],
                          params          = Config['Params'],
                          cookies         = Config['Cookie'],
                          timeout         = Config['Timeout'],
                          allow_redirects = Config['Redirect'])
        
        if _.status_code == 405: _ = requests.get(Url,
                                                  headers         = Config['Header'],
                                                  params          = Config['Params'],
                                                  cookies         = Config['Cookie'],
                                                  timeout         = Config['Timeout'],
                                                  allow_redirects = Config['Redirect'])

        Response['HttpCode']      = _.status_code
        Response['FinalUrl']      = _.url
        Response['ContentType']   = _.headers.get('Content-Type', '')
        Response['ContentLength'] = int(_.headers.get('Content-Length', '-1'))
    except Exception as errorMsg:
        Response['ErrorCode'] = 50000
        Response['ErrorMsg']  = f'Fail to head url, {str(errorMsg).lower().rstrip(".")}'
    return Response


def GetFileViaRequests(Cfg = None):
    import os
    import time
    import requests

    if __name__ == '__main__':
        from  Merge import MergeCfg
    else:
        from .Merge import MergeCfg

    Config = {
        'Url'     : '',
        'Folder'  : '',
        'File'    : '',
        'MinSize' : 1024,      # In Bytes, 1 KB
        'MaxSize' : 1024 ** 5, # In Bytes, 1 PB
        'Time'    : None,
        'Header'  : {
            'Accept'    : '*/*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.41'
            },
        'Params'  : {},
        'Cookie'  : None,
        'Timeout' : 10,
        'Redirect': True,
    }
    Config = MergeCfg(Config, Cfg)

    Response = {
        'ErrorCode'    : 0,
        'ErrorMsg'     : '',
        'HttpCode'     : -1,
        'FirstUrl'     : '',
        'FinalUrl'     : '',
        'ContentType'  : '',
        'ContentLength': -1,
        'Folder'       : '',
        'File'         : '',
        'Path'         : '',
        'Size'         : -1
    }

    # MAKE FOLDER
    try:
        Folder = Config['Folder'] if Config['Folder'] != '' else '.'
        os.makedirs(Folder, exist_ok = True)
    except Exception as errorMsg:
        Response['ErrorCode'] = 50001
        Response['ErrorMsg']  = f'Fail to make folder, {str(errorMsg).lower().rstrip(".")}'
        return Response

    # GET FILE
    try:
        Url                  = Config['Url']
        Response['FirstUrl'] = Url

        _ = requests.get(Url,
                         headers         = Config['Header'],
                         params          = Config['Params'],
                         cookies         = Config['Cookie'],
                         timeout         = Config['Timeout'],
                         allow_redirects = Config['Redirect'])

        Response['HttpCode']      = _.status_code
        Response['FinalUrl']      = _.url
        Response['ContentType']   = _.headers.get('Content-Type', '')
        Response['ContentLength'] = int(_.headers.get('Content-Length', '-1'))

        if 200 <= _.status_code < 300 and Config['MinSize'] <= Response['ContentLength'] <= Config['MaxSize']:
            File = Config['File']
            Path = os.path.join(Folder, File)

            with open(Path, 'wb') as F: F.write(_.content)

            Response['Folder'] = Folder
            Response['File']   = File
            Response['Path']   = Path
            Response['Size']   = os.path.getsize(Path)
        else:
            raise Exception(f'status_code is {Response["HttpCode"]}, content_length is {Response["ContentLength"]}')

        if not Config['Time'] is None:
            os.utime(Path, (Config['Time'], Config['Time']))
        elif 'Last-Modified' in _.headers:
            _ = int(time.mktime(time.strptime(_.headers['Last-Modified'], '%a, %d %b %Y %H:%M:%S %Z')))
            os.utime(Path, (_, _))
    except Exception as errorMsg:
        Response['ErrorCode'] = 50002
        Response['ErrorMsg']  = f'Fail to download file from given url, {str(errorMsg).lower().rstrip(".")}'
        return Response

    return Response


def GetFileViaDownloadKit(Cfg = None):
    import os
    import time
    
    from DownloadKit import DownloadKit

    if __name__ == '__main__':
        from  Merge import MergeCfg
    else:
        from .Merge import MergeCfg

    Config = {
        'Url'             : '',
        'Folder'          : '',
        'File'            : '',
        'Time'            : None,
        'ShowDownloading' : False,
        'CleanDownloading': True,
        'NoticePrefix'    : '',
        'NoticeSuffix'    : '',
        'Header'          : {
            'Accept'    : '*/*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.41'
            },
        'Params'          : {},
        'Cookie'          : None,
        'Timeout'         : 10,
        'Redirect'        : True,
    }
    Config = MergeCfg(Config, Cfg)

    Response = {
        'ErrorCode'    : 0,
        'ErrorMsg'     : '',
        'HttpCode'     : -1,
        'FirstUrl'     : '',
        'FinalUrl'     : '',
        'ContentType'  : '',
        'ContentLength': -1,
        'Folder'       : '',
        'File'         : '',
        'Path'         : '',
        'Size'         : -1
    }

    # MAKE FOLDER
    try:
        Folder = Config['Folder'] if Config['Folder'] != '' else '.'
        os.makedirs(Folder, exist_ok = True)
    except Exception as errorMsg:
        Response['ErrorCode'] = 50001
        Response['ErrorMsg']  = f'Fail to make folder, {str(errorMsg).lower().rstrip(".")}'
        return Response

    # GET FILE
    try:
        Url                  = Config['Url']
        Response['FirstUrl'] = Url

        File = Config['File']
        Path = os.path.join(Folder, File)

        Kit = DownloadKit()
        Tsk = Kit.add(Url, Folder, File,
                      file_exists     = 'overwrite',
                      split           = True,
                      headers         = Config['Header'],
                      params          = Config['Params'],
                      cookies         = Config['Cookie'],
                      timeout         = Config['Timeout'],
                      allow_redirects = Config['Redirect'])

        Timer = 0
        if Config['ShowDownloading']:
            print(f'\r{Config["NoticePrefix"]}0.00 %{Config["NoticeSuffix"]}', end = '')

            while Tsk.rate == None or Tsk.rate == 0.0:
                if Timer >= 10:
                    if Tsk.rate == None or Tsk.rate == 0.0:
                        Tsk.cancel()
                        print(f'\r{" " * os.get_terminal_size().columns}', end = '\r') if Config['CleanDownloading'] else print()
                        raise Exception('connecting timeout')
                Timer += 1
                time.sleep(1)

            while True:
                print(f'\r{Config["NoticePrefix"]}{Tsk.rate} %{Config["NoticeSuffix"]}', end = '     ')
                if Tsk.is_done:
                    print(f'\r{" " * os.get_terminal_size().columns}', end = '\r') if Config['CleanDownloading'] else print()
                    break
                else:
                    time.sleep(0.025)

        else:
            while Tsk.rate == None or Tsk.rate == 0.0:
                if Timer >= 10:
                    if Tsk.rate == None or Tsk.rate == 0.0:
                        Tsk.cancel()
                        raise Exception('connecting timeout')
                Timer += 1
                time.sleep(1)
            Tsk.wait(show = False)
        
        if Tsk.result == 'success':
            Kit = None
            Response['Folder'] = Folder
            Response['File']   = File
            Response['Path']   = Path
            Response['Size']   = os.path.getsize(Path)
        else:
            Kit = None
            raise Exception(f'download result is {Tsk.info}')

        if not Config['Time'] is None:
            os.utime(Path, (Config['Time'], Config['Time']))
    except Exception as errorMsg:
        Response['ErrorCode'] = 50002
        Response['ErrorMsg']  = f'Fail to download file from given url, {str(errorMsg).lower().rstrip(".")}'
        return Response

    return Response
