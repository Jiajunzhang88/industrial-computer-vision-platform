import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from src.backend.dependencies import get_db
from src.backend.services.model import ModelService
from src.backend.models import Model

db = next(get_db())
service = ModelService(db)
model = db.query(Model).filter(Model.id == 1).first()
print(f"模型: id={model.id} name={model.name} arch={model.architecture} status={model.status}")
print(f"参数: {model.parameters}")
print(f"数据集ID: {model.dataset_id}")
try:
    result = service.train_model(model)
    print(f"训练结果: {result}")
except Exception as e:
    import traceback
    traceback.print_exc()
