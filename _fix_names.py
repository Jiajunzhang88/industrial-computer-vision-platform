from ultralytics import YOLO
import shutil

src = r"models\model_2\weights\best.pt"
model = YOLO(src)
print("before names:", model.names)

# 修正类别名
model.model.names = {0: 'obverse', 1: 'reverse'}
# 保存到临时文件
tmp = r"models\model_2\weights\best_fixed.pt"
model.save(tmp)
print("saved", tmp)

# 验证
m2 = YOLO(tmp)
print("after names:", m2.names)
