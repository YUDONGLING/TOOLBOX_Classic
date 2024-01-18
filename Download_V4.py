_CONFIG_C4181A5B_97E4_2B30_D2CD_0C739E8F0F19_ = {
    'requestHeader'  : {
        'Accept'     : '*/*',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.41'
    },
    'requestParams'  : {},
    'requestCookie'  : {},
}


def headURL(URL, customHeader = None, customParams = None, customCookie = None, allowRedirects = True):
    import copy
    import requests

    headInfo = {
        'statusCode'    : -1,
        'locationURL'   : '',
        'contentType'   : '',
        'contentLength' : -1,
        'cookie'        : {}
        }

    requestHeader = copy.deepcopy(_CONFIG_C4181A5B_97E4_2B30_D2CD_0C739E8F0F19_['requestHeader'])
    requestHeader.update({'Range' : 'bytes=0-'})
    requestHeader.update(customHeader or {})

    requestParams = copy.deepcopy(_CONFIG_C4181A5B_97E4_2B30_D2CD_0C739E8F0F19_['requestParams'])
    requestParams.update(customParams or {})

    requestCookie = copy.deepcopy(_CONFIG_C4181A5B_97E4_2B30_D2CD_0C739E8F0F19_['requestCookie'])
    requestCookie.update(customCookie or {})

    try:
        HEAD = requests.head(URL, headers = requestHeader, params = requestParams, cookies = requestCookie, allow_redirects = allowRedirects, timeout = 10)
    except Exception as errorMsg:
        return (False, str(errorMsg)), headInfo

    if HEAD.status_code == 405:
        try:
            HEAD = requests.get(URL, headers = requestHeader, params = requestParams, cookies = requestCookie, allow_redirects = allowRedirects, timeout = 10)
        except Exception as errorMsg:
            return (False, str(errorMsg)), headInfo

    headInfo.update({
        'statusCode'    : HEAD.status_code,
        'locationURL'   : HEAD.url,
        'contentType'   : HEAD.headers.get('Content-Type', ''),
        'contentLength' : int(HEAD.headers.get('Content-Length', '-1')),
        'cookie'        : dict(HEAD.cookies)
    })
    return (True, ''), headInfo


def getFile(URL, fileFolder, fileName, customHeader = None, customParams = None, customCookie = None, customModifiedTime = None, allowRedirects = True):
    import os, copy, time, requests
    
    getInfo = {
        'URL'               : URL,
        'fileFolder'        : '',
        'fileName'          : '',
        'fileSize'          : -1,
        'responseData'      : {
            'statusCode'    : -1,
            'locationURL'   : '',
            'contentType'   : '',
            'contentLength' : -1,
            'cookie'        : {}
            }
        }

    fileFolder = fileFolder.strip() if fileFolder.strip() != '' else '.'
    fileName   = fileName.strip()
    filePath   = os.path.join(fileFolder, fileName)

    try:
        os.makedirs(fileFolder, exist_ok = True); getInfo['fileFolder'] = fileFolder
    except Exception as errorMsg:
        return (False, str(errorMsg)), getInfo

    requestHeader = copy.deepcopy(_CONFIG_C4181A5B_97E4_2B30_D2CD_0C739E8F0F19_['requestHeader'])
    requestHeader.update(customHeader or {})

    requestParams = copy.deepcopy(_CONFIG_C4181A5B_97E4_2B30_D2CD_0C739E8F0F19_['requestParams'])
    requestParams.update(customParams or {})

    requestCookie = copy.deepcopy(_CONFIG_C4181A5B_97E4_2B30_D2CD_0C739E8F0F19_['requestCookie'])
    requestCookie.update(customCookie or {})

    try:
        GET = requests.get(URL, headers = requestHeader, params = requestParams, cookies = requestCookie, allow_redirects = allowRedirects, timeout = 10)
    except Exception as errorMsg:
        return (False, str(errorMsg)), getInfo

    getInfo['responseData'].update({
        'statusCode'    : GET.status_code,
        'locationURL'   : GET.url,
        'contentType'   : GET.headers.get('Content-Type', ''),
        'contentLength' : int(GET.headers.get('Content-Length', '-1')),
        'cookie'        : dict(GET.cookies)
    })

    if 200 <= GET.status_code < 300 and (getInfo['responseData']['contentLength'] > 1024 or getInfo['responseData']['contentLength'] == -1):
        try:
            with open(filePath, 'wb') as F:
                F.write(GET.content)
        except Exception as errorMsg:
            return (False, str(errorMsg)), getInfo
        GET.close()
        getInfo.update({
            'fileName' : fileName,
            'fileSize' : os.path.getsize(filePath)
        })
    else:
        GET.close()
        return (False, f'response status_code is {getInfo["responseData"]["statusCode"]}, content_length is {getInfo["responseData"]["contentLength"]}'), getInfo

    if not customModifiedTime is None:
        try:
            os.utime(filePath, (customModifiedTime, customModifiedTime))
        except:
            pass
    elif 'Last-Modified' in GET.headers:
        try:
            serverModifiedTime = int(time.mktime(time.strptime(GET.headers['Last-Modified'], '%a, %d %b %Y %H:%M:%S %Z')))
            os.utime(filePath, (serverModifiedTime, serverModifiedTime))
        except:
            pass

    return (True, ''), getInfo


def getFileByDownloadKit(URL, fileFolder, fileName, customHeader = None, customParams = None, customCookie = None, customModifiedTime = None, allowRedirects = True, showDLing = False, showDLNotice = ('', '')):
    import os, copy, time

    from DownloadKit import DownloadKit
    
    getInfo = {
        'URL'               : URL,
        'fileFolder'        : '',
        'fileName'          : '',
        'fileSize'          : -1,
        'responseData'      : {
            'statusCode'    : -1,
            'locationURL'   : '',
            'contentType'   : '',
            'contentLength' : -1,
            'cookie'        : {}
            }
        }

    fileFolder = fileFolder.strip() if fileFolder.strip() != '' else '.'
    fileName   = fileName.strip()
    filePath   = os.path.join(fileFolder, fileName)

    try:
        os.makedirs(fileFolder, exist_ok = True); getInfo['fileFolder'] = fileFolder
    except Exception as errorMsg:
        return (False, str(errorMsg)), getInfo

    requestHeader = copy.deepcopy(_CONFIG_C4181A5B_97E4_2B30_D2CD_0C739E8F0F19_['requestHeader'])
    requestHeader.update(customHeader or {})

    requestParams = copy.deepcopy(_CONFIG_C4181A5B_97E4_2B30_D2CD_0C739E8F0F19_['requestParams'])
    requestParams.update(customParams or {})

    requestCookie = copy.deepcopy(_CONFIG_C4181A5B_97E4_2B30_D2CD_0C739E8F0F19_['requestCookie'])
    requestCookie.update(customCookie or {})

    try:
        DLer = DownloadKit()
        DLer.block_size = '4M'

        DLtask = DLer.add(URL, fileFolder, fileName, file_exists = 'overwrite', split = True, headers = requestHeader, params = requestParams, cookies = requestCookie)

        Tcount = 0

        if showDLing:
            print(f'\r{showDLNotice[0]}0.00 %{showDLNotice[1]}', end = '')

            while DLtask.rate == None or DLtask.rate == 0.0:
                if Tcount >= 20:
                    if DLtask.rate == None or DLtask.rate == 0.0:
                        DLtask.cancel()
                        return (False, 'Connect Time Out! '), getInfo
                Tcount += 1
                time.sleep(0.5)

            while True:
                print(f'\r{showDLNotice[0]}{DLtask.rate} %{showDLNotice[1]}', end = '     ')
                if DLtask.is_done:
                    break
                else:
                    time.sleep(0.025)
        else:
            while DLtask.rate == None or DLtask.rate == 0.0:
                if Tcount >= 20:
                    if DLtask.rate == None or DLtask.rate == 0.0:
                        DLtask.cancel()
                        return (False, 'Connect Time Out! '), getInfo
                Tcount += 1
                time.sleep(0.5)
            DLtask.wait(show = False)            

        if not DLtask.result == 'success':
            DLer = None
            return (False, str(DLtask.info)), getInfo
        else:
            DLer = None
            getInfo.update({'fileName': fileName, 'fileSize': os.path.getsize(filePath)})
    except Exception as errorMsg:
        try:
            DLer = None
        except:
            pass
        return (False, str(errorMsg)), getInfo

    if not customModifiedTime is None:
        try:
            os.utime(filePath, (customModifiedTime, customModifiedTime))
        except:
            pass

    return (True, ''), getInfo


if __name__ == '__main__':
    import os

    print(f'[headFile(URL, ***)]: {headURL("http://dl.hdslb.com/mobile/fixed/bili_win/bili_win-install.exe?v=1.9.2")}')

    print(f'[getFile(URL, ***)]: {getFile("http://dl.hdslb.com/mobile/fixed/bili_win/bili_win-install.exe?v=1.9.2", "", "TEST")}')
    os.remove('TEST')

#   print(f'[getFileByDownloadKit(URL, ***)]: {getFileByDownloadKit("http://dl.hdslb.com/mobile/fixed/bili_win/bili_win-install.exe?v=1.9.2", "", "TEST")}')
#   os.remove('TEST')

    STATE, INFO = getFileByDownloadKit('http://dl.hdslb.com/mobile/fixed/bili_win/bili_win-install.exe?v=1.9.2', '', 'TEST.BIN', showDLing = True, showDLNotice = ('     下载进度前测试文字     ', '     下载进度后测试文字     '))
    print(f'')
    print(f'[getFileByDownloadKit(URL, ***)]: ', end = '')
    print(f'{STATE}, {INFO}')
    os.remove('TEST.BIN')