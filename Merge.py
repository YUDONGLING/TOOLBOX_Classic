def MergeCfg(BasicCfg: dict, AppendCfg: dict):
    if AppendCfg == None:
        return BasicCfg
    for _Key, _Value in AppendCfg.items():
        if _Key in BasicCfg:
            if type(BasicCfg[_Key]) == type(_Value) == dict:
                BasicCfg[_Key].update(_Value)
            elif type(BasicCfg[_Key]) == type(_Value) or BasicCfg[_Key] == None:
                BasicCfg[_Key] = _Value
        else:
            BasicCfg[_Key] = _Value
    return BasicCfg
