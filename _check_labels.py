import os, yaml

base = r"I:\git\industrial-computer-vision-platform\data\datasets\dataset_4"
with open(os.path.join(base, "dataset.yaml")) as f:
    d = yaml.safe_load(f)
print("yaml:", d)

# 统计训练集
a_count = b_count = 0
train_labels = os.path.join(base, "train", "labels")
for f in os.listdir(train_labels):
    if not f.endswith(".txt"): continue
    for line in open(os.path.join(train_labels, f)):
        cls = line.strip().split()[0]
        if cls == "0": a_count += 1
        elif cls == "1": b_count += 1
print(f"训练集: A(类0)={a_count}, B(类1)={b_count}")

# 列出几个 A 和 B 的文件名
print("\nA类文件:")
for f in os.listdir(train_labels):
    if not f.endswith(".txt"): continue
    for line in open(os.path.join(train_labels, f)):
        cls = line.strip().split()[0]
        if cls == "0":
            print(f"  {f}")
            break
print("\nB类文件:")
for f in os.listdir(train_labels):
    if not f.endswith(".txt"): continue
    for line in open(os.path.join(train_labels, f)):
        cls = line.strip().split()[0]
        if cls == "1":
            print(f"  {f}")
            break
