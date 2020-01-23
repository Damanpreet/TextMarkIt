'''
    Version - 1.0
    Date - 16/01/2020
    
    Script function -
    This script is used to dynamically load the modules.
'''
#utils/helper.py

import importlib

def load_modules(module_path):
    module = __import__(module_path)
    # module = importlib.import_module(module_path)
    components = module_path.split('.')
    module = getattr(module, components[1:])
    return module