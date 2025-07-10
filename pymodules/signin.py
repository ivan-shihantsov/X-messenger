from .common import do_auth


# main func
def sign_in(content):
    user_id = content['user_id']
    key = content['key']
    authKey = "dummy" # content['authKey']
    
    if do_auth(user_id, key, authKey) == "ok":
        return "<p>access allowed</p>"
    else:
        return "<p>access denied</p>"
