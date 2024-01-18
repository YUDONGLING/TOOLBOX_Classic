def CreateDB(Cfg = None):
    import os
    import sqlite3

    if __name__ == '__main__':
        from  Merge import MergeCfg
    else:
        from .Merge import MergeCfg

    Config = {
        'Folder': '',
        'DB'    : ''
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

    # MAKE FOLDER
    try:
        Folder = Config['Folder'] if Config['Folder'] != '' else '.'
        os.makedirs(Folder, exist_ok = True)
    except Exception as errorMsg:
        Response['ErrorCode'] = 50001
        Response['ErrorMsg']  = f'Fail to make folder, {str(errorMsg).lower().rstrip(".")}'
        return Response

    # CREATE DB
    try:
        File = Config['DB']
        Path = os.path.join(Folder, File)

        _ = sqlite3.connect(Path)
        _.close()

        Response['Folder'] = Folder
        Response['File']   = File
        Response['Path']   = Path
        Response['Size']   = os.path.getsize(Path)
    except Exception as errorMsg:
        Response['ErrorCode'] = 50002
        Response['ErrorMsg']  = f'Fail to create database, {str(errorMsg).lower().rstrip(".")}'
        return Response

    return Response


def ExecuteDB(Cfg = None):
    import os
    import sqlite3

    if __name__ == '__main__':
        from  Merge import MergeCfg
    else:
        from .Merge import MergeCfg

    Config = {
        'Folder': '',
        'DB'    : '',
        'Query' : '',
        'Param' : ()
    }
    Config = MergeCfg(Config, Cfg)

    Response = {
        'ErrorCode': 0,
        'ErrorMsg' : '',
        'Data'     : []
    }

    try:
        DB = sqlite3.connect(os.path.join(Config['Folder'] if Config['Folder'] != '' else '.', Config['DB']))
        CR = DB.cursor(); CR.execute(Config['Query'], Config['Param'])
        Response['Data'] = CR.fetchall()
        DB.commit(); DB.close()
    except Exception as errorMsg:
        Response['ErrorCode'] = 50000
        Response['ErrorMsg']  = f'Fail to operate database, {str(errorMsg).lower().rstrip(".")}'
    return Response
