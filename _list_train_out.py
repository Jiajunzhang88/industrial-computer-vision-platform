import os, glob, json

for d in [r"runs\detect\models\model_2", r"models\model_2", r"models\model_2\weights"]:
    print("== dir:", d)
    if os.path.exists(d):
        for f in os.listdir(d):
            p = os.path.join(d, f)
            print("   ", f, os.path.getsize(p) if os.path.isfile(p) else "(dir)")
    else:
        print("   MISSING")

# 读 args.yaml names
for y in [r"runs\detect\models\model_2\args.yaml", r"models\model_2\args.yaml"]:
    if os.path.exists(y):
        print("== args.yaml:", y)
        with open(y) as f:
            print(f.read()[:2000])
