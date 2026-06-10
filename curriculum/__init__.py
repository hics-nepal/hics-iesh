from .modules.activities import MODULES

def get_module(module_id):
    return MODULES.get(module_id)

def get_activity(module_id, activity_id):
    m = get_module(module_id)
    if not m:
        return None, None
    for a in m['activities']:
        if a['id'] == activity_id:
            return m, a
    return m, None

def all_modules():
    return list(MODULES.values())
