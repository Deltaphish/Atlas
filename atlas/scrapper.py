'''
    Scrapes name of media file with help of plugins

    dynamicaly loads plugins from scrapper_plugins to
    find relevant meta data of file
'''

import importlib.util as imp
from os import walk

def _getDir():
    dir = __file__.split("/")[0:-1]
    res = ""
    for i in dir:
        res += i
        res += "/"
    return res

def scrape(path):
    '''
        Finds plugins, runs path through plugins, and returns a list of tags
        in the format [("scrapper","key","value")..]

        example return: [("std","episode","01")]
    '''
    (_, _, filenames) = next(walk(_getDir()+"scrapper_plugins"))
    results = []

    for f in filenames:
        spec = imp.spec_from_file_location(f[:-3],_getDir()+"scrapper_plugins/"+f)
        mod = imp.module_from_spec(spec)
        loaded_mod = mod.__loader__.load_module()
        results += loaded_mod.scrape(path)

    return results    