import os, urllib.request

# dist 结构
d = "dist"
print("== dist ==")
for f in sorted(os.listdir(d)):
    print("  ", f)
assets = os.path.join(d, "assets")
if os.path.isdir(assets):
    print("== dist/assets ==")
    for f in sorted(os.listdir(assets)):
        print("  ", f)

# 根页面
try:
    r = urllib.request.urlopen("http://127.0.0.1:8000/", timeout=10)
    html = r.read().decode()
    print("== root status", r.status, "len", len(html))
    # 提取引用的资源
    import re
    for m in re.findall(r'(src|href)="([^"]+)"', html):
        print("   ref:", m[0], m[1])
except Exception as e:
    print("root err:", e)
