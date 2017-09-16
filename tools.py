import execjs

with open('utf.js','r') as f:
    ctx = execjs.compile(f.read())

def decode_ip_ref(rawip):
    result = ctx.call('this.URLdecode',rawip)
    return result