import execjs
import os
from . import dir_path


def decode_ip_ref(rawip):
    with open(os.path.join(dir_path,'utf.js'), 'r') as f:
        ctx = execjs.compile(f.read())
    result = ctx.call('this.URLdecode',rawip)
    return result