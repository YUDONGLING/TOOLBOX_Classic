def AppendLog(Cfg = None):
    import os
    import time

    if __name__ == '__main__':
        from  Merge import MergeCfg
    else:
        from .Merge import MergeCfg

    Config = {
        'Data'        : None,
        'Folder'      : 'Log',
        'FolderPerfix': '',
        'FolderSuffix': '',
        'File'        : None,
        'FilePerfix'  : '',
        'FileSuffix'  : ''
    }
    Config = MergeCfg(Config, Cfg)

    Response = {
        'ErrorCode': 0,
        'ErrorMsg' : '',
        'Folder'   : '',
        'File'     : '',
        'Path'     : '',
        'Size'     : -1
    }

    Date_ISO = time.strftime('%Y-%m-%d', time.localtime()) # YYYY-MM-DD
    Date_USA = time.strftime('%Y/%m/%d', time.localtime()) # YYYY/MM/DD
    Hour     = time.strftime('%H:%M:%S', time.localtime()) # HH:MM:SS

    # MAKE FOLDER
    try:
        Folder = Config['FolderPerfix'] + Config['Folder'] + Config['FolderSuffix']
        Folder = Folder if Folder != '' else '.'
        os.makedirs(Folder, exist_ok = True)
    except Exception as errorMsg:
        Response['ErrorCode'] = 50001
        Response['ErrorMsg']  = f'Fail to make folder, {str(errorMsg).lower().rstrip(".")}'
        return Response

    # APPEND LOG
    try:
        File = Config['FilePerfix'] + (Config['File'] if Config['File'] else Date_ISO) + Config['FileSuffix'] + '.txt'
        Path = os.path.join(Folder, File)

        with open(Path, 'a', encoding = 'utf-8') as _: _.write(f'@{Date_USA} {Hour} | {Config["Data"]}\n')

        Response['Folder'] = Folder
        Response['File']   = File
        Response['Path']   = Path
        Response['Size']   = os.path.getsize(Path)
    except Exception as errorMsg:
        Response['ErrorCode'] = 50002
        Response['ErrorMsg']  = f'Fail to append log, {str(errorMsg).lower().rstrip(".")}'
        return Response

    return Response
