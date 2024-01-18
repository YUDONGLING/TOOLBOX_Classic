def GetUuid1Name(Cfg = None):
    from uuid import uuid1

    if __name__ == '__main__':
        from  Merge import MergeCfg
    else:
        from .Merge import MergeCfg

    Config = {
        'Count': 1
    }
    Config = MergeCfg(Config, Cfg)

    Response = {
        'ErrorCode': 0,
        'ErrorMsg' : '',
        'Uuid'     : [],
        'Count'    : 0
    }

    try:
        for _ in range(Config['Count']):
            Response['Uuid'].append(str(uuid1()).lower().replace('-', '_'))
            Response['Count'] += 1
    except Exception as errorMsg:
        Response['ErrorCode'] = 50000
        Response['ErrorMsg']  = f'Fail to generate uuid1 name, {str(errorMsg).lower().rstrip(".")}'
    return Response


def GetUuid3Name(Cfg = None):
    from uuid import uuid3
    from uuid import NAMESPACE_DNS

    if __name__ == '__main__':
        from  Merge import MergeCfg
    else:
        from .Merge import MergeCfg

    Config = {
        'Count' : 1,
        'Domain': 'localhost'
    }
    Config = MergeCfg(Config, Cfg)

    Response = {
        'ErrorCode': 0,
        'ErrorMsg' : '',
        'Uuid'     : [],
        'Count'    : 0
    }

    try:
        for _ in range(Config['Count']):
            Response['Uuid'].append(str(uuid3(NAMESPACE_DNS, Config['Domain'])).lower().replace('-', '_'))
            Response['Count'] += 1
    except Exception as errorMsg:
        Response['ErrorCode'] = 50000
        Response['ErrorMsg']  = f'Fail to generate uuid3 name, {str(errorMsg).lower().rstrip(".")}'
    return Response


def GetUuid4Name(Cfg = None):
    from uuid import uuid4

    if __name__ == '__main__':
        from  Merge import MergeCfg
    else:
        from .Merge import MergeCfg

    Config = {
        'Count': 1
    }
    Config = MergeCfg(Config, Cfg)

    Response = {
        'ErrorCode': 0,
        'ErrorMsg' : '',
        'Uuid'     : [],
        'Count'    : 0
    }

    try:
        for _ in range(Config['Count']):
            Response['Uuid'].append(str(uuid4()).lower().replace('-', '_'))
            Response['Count'] += 1
    except Exception as errorMsg:
        Response['ErrorCode'] = 50000
        Response['ErrorMsg']  = f'Fail to generate uuid4 name, {str(errorMsg).lower().rstrip(".")}'
    return Response


def GetUuid5Name(Cfg = None):
    from uuid import uuid5
    from uuid import NAMESPACE_DNS

    if __name__ == '__main__':
        from  Merge import MergeCfg
    else:
        from .Merge import MergeCfg

    Config = {
        'Count' : 1,
        'Domain': 'localhost'
    }
    Config = MergeCfg(Config, Cfg)

    Response = {
        'ErrorCode': 0,
        'ErrorMsg' : '',
        'Uuid'     : [],
        'Count'    : 0
    }

    try:
        for _ in range(Config['Count']):
            Response['Uuid'].append(str(uuid5(NAMESPACE_DNS, Config['Domain'])).lower().replace('-', '_'))
            Response['Count'] += 1
    except Exception as errorMsg:
        Response['ErrorCode'] = 50000
        Response['ErrorMsg']  = f'Fail to generate uuid5 name, {str(errorMsg).lower().rstrip(".")}'
    return Response
