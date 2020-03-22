import base64
# ico
with open("asset.py","w") as f:
    f.write('class Icon(object):\n')
    f.write('\tdef __init__(self):\n')
    f.write("\t\tself.img='")
with open("icon2.ico","rb") as i:
    b64str = base64.b64encode(i.read())
    with open("asset.py","ab+") as f:
        f.write(b64str)
with open("asset.py","a") as f:
    f.write("'\n")

# lianxi.png
with open("asset.py","a") as f:
    f.write('class Lianxi(object):\n')
    f.write('\tdef __init__(self):\n')
    f.write("\t\tself.img='")
with open("lianxi.png","rb") as i:
    b64str = base64.b64encode(i.read())
    with open("asset.py","ab+") as f:
        f.write(b64str)
with open("asset.py","a") as f:
    f.write("'\n")

# shequ.png
with open("asset.py","a") as f:
    f.write('class Shequ(object):\n')
    f.write('\tdef __init__(self):\n')
    f.write("\t\tself.img='")
with open("shequ.png","rb") as i:
    b64str = base64.b64encode(i.read())
    with open("asset.py","ab+") as f:
        f.write(b64str)
with open("asset.py","a") as f:
    f.write("'\n")