import execjs


with open('utf.js','r') as f:
    ctx = execjs.compile(f.read())
    result = ctx.call('this.URLdecode','%3c%61%20%68%72%65%66%3d%22%68%74%74%70%3a%2f%2f%77%77%77%2e%66%72%65%65%70%72%6f%78%79%6c%69%73%74%73%2e%6e%65%74%2f%7a%68%2f%31%32%33%2e%37%2e%38%32%2e%32%30%2e%68%74%6d%6c%22%3e%31%32%33%2e%37%2e%38%32%2e%32%30%3c%2f%61%3e')
    print(result)

