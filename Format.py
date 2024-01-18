def FileNameSafer(Cfg = None):
    import re

    if __name__ == '__main__':
        from Merge import MergeCfg
    else:
        from .Merge import MergeCfg

    Config = {
        'Name'        : '',
        'MaxLength'   : 50,
        'ForceReplace': []
    }
    Config = MergeCfg(Config, Cfg)

    Response = {
        'ErrorCode': 0,
        'ErrorMsg' : '',
        'Name'     : ''
    }

    try:
        _ = Config['Name']
        for Rule in Config['ForceReplace']:
            if len(Rule) == 2: _ = _.replace(Rule[0], Rule[1])
        Response['Name']   = re.sub(r'\s+', ' ', re.sub(r'[\\/:*?\"<>|\n]', ' ', _)).lstrip()[:Config['MaxLength']].rstrip()
    except Exception as errorMsg:
        Response['ErrorCode'] = 50000
        Response['ErrorMsg']  = f'Fail to safety given name, {str(errorMsg).lower().rstrip(".")}'
    return Response


def StorageUnitProcesser(Cfg = None):
    if __name__ == '__main__':
        from Merge import MergeCfg
    else:
        from .Merge import MergeCfg

    Config = {
        'Size'         : -1,
        'Unit'         : 'B',
        'TargetDecimal': 2,
        'TargetUnit'   : 'AUTO',
        'TargetFormat' : '{Size} {Unit}'
    }
    Config = MergeCfg(Config, Cfg)

    Response = {
        'ErrorCode': 0,
        'ErrorMsg' : '',
        'Size'     : ''
    }

    Unit_List   = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    Unit_Weight = {'B': 0, 'KB': 1, 'MB': 2, 'GB': 3, 'TB': 4, 'PB': 5, 'EB': 6, 'ZB': 7, 'YB': 8}

    if Config['Size'] < 0:
        Response['ErrorCode'] = 50001
        Response['ErrorMsg']  = f'Value error, size must be positive'
        return Response

    if Config['Unit'].upper() not in Unit_List:
        Response['ErrorCode'] = 50002
        Response['ErrorMsg']  = f'Units error, unit must in B, KB, MB, GB, TB, PB, EB, ZB or YB'
        return Response

    if Config['TargetUnit'].upper() == 'AUTO':
        _InputExponent = _OutputExponent = Unit_Weight[Config['Unit'].upper()]

        _Size = Config['Size']
        if _Size >= 1:
            while _Size >= 1024 and _OutputExponent < 8:
                _OutputExponent += 1
                _Size /= 1024
        else:
            while _Size < 1 and _OutputExponent > 0:
                _OutputExponent -= 1
                _Size *= 1024

        _Size = '{:.{}f}'.format(_Size, Config['TargetDecimal'])
        _Unit = Unit_List[_OutputExponent]
    else:
        _InputExponent  = Unit_Weight[Config['Unit'].upper()]
        _OutputExponent = Unit_Weight[Config['TargetUnit'].upper()]

        _Size = '{:.{}f}'.format(Config['Size'] * 1.00000000001 * (1024 ** (_InputExponent - _OutputExponent)), Config['TargetDecimal'])
        _Unit = Config['TargetUnit']

    Response['Size'] = Config['TargetFormat'].replace('{Size}', str(_Size)).replace('{Unit}', _Unit)
    return Response
