<template>
  <div class="model-tester">
    <div class="row q-col-gutter-md">
      <!-- 测试控制区域 -->
      <div class="col-12 col-md-4">
        <!-- 选择模型区域 -->
        <div v-if="!selectedModel" class="select-model-card">
          <q-icon name="photo_camera" size="3em" color="primary" />
          <div class="text-h6 q-mt-md">{{ t('modelTester.selectModel.title') }}</div>
          <div class="text-body2 q-mt-sm text-grey">
            {{ t('modelTester.selectModel.hint') }}
          </div>
        </div>

        <!-- 控制面板 -->
        <div v-else class="control-panel">
          <div class="text-h6 q-mb-sm">{{ selectedModel.name }}</div>
          <div class="text-caption q-mb-md">{{ t('modelTester.model.id') }}: {{ selectedModel.id }}</div>

          <q-separator class="q-my-md" />

          <!-- 参数设置 -->
          <div class="text-subtitle1 q-mb-sm">{{ t('modelTester.params.title') }}</div>

          <div class="text-caption text-grey q-mb-xs">{{ t('modelTester.params.preprocessing') }}</div>
          <q-input
            v-model.number="imgSize"
            type="number"
            :label="t('modelTester.params.imageSize')"
            outlined
            dense
            min="320"
            max="1280"
            step="32"
          />

          <div class="text-caption text-grey q-mt-md q-mb-xs">{{ t('modelTester.params.postprocessing') }}</div>
          <q-input
            v-model.number="confThreshold"
            type="number"
            :label="`${t('modelTester.params.confThreshold')} (conf)`"
            outlined
            dense
            min="0"
            max="1"
            step="0.05"
          />
          <q-input
            v-model.number="iouThreshold"
            type="number"
            :label="`${t('modelTester.params.iouThreshold')} (NMS)`"
            outlined
            dense
            min="0"
            max="1"
            step="0.05"
            class="q-mt-sm"
          />
          <q-input
            v-model.number="maxDet"
            type="number"
            :label="t('modelTester.params.maxDetections')"
            outlined
            dense
            min="1"
            max="1000"
            step="10"
            class="q-mt-sm"
          />
          <q-toggle
            v-model="agnosticNms"
            :label="t('modelTester.params.classAgnosticNms')"
            class="q-mt-sm"
            color="primary"
          />
          <q-toggle
            v-model="autoRetest"
            :label="t('modelTester.params.autoRetest')"
            class="q-mt-sm"
            color="primary"
          />

          <q-separator class="q-my-md" />

          <!-- 图像上传 -->
          <div class="text-subtitle1 q-mb-sm">{{ t('modelTester.image.title') }}</div>
          <q-file
            v-model="imageFile"
            :label="t('modelTester.image.select')"
            outlined
            dense
            accept=".jpg,.jpeg,.png"
            @update:model-value="handleImageSelected"
          >
            <template v-slot:prepend>
              <q-icon name="attach_file" />
            </template>
          </q-file>

          <q-btn
            :label="t('modelTester.image.cameraCapture')"
            color="amber"
            icon="camera_alt"
            class="q-mt-sm full-width"
            unelevated
            @click="captureFromCamera"
            :loading="capturing"
          />

          <div class="q-mt-md">
            <q-btn
              :label="t('modelTester.image.test')"
              color="primary"
              icon="science"
              @click="testModel"
              :loading="loading"
              :disable="!previewUrl || loading"
              class="full-width"
            />
          </div>
        </div>
      </div>

      <!-- 测试结果区域 -->
      <div class="col-12 col-md-8">
        <q-card class="result-card">
          <q-card-section>
            <div class="text-h6">{{ t('modelTester.result.title') }}</div>

            <!-- 无图像时显示提示 -->
            <div v-if="!previewUrl && !resultImage" class="no-image-container">
              <q-icon name="insert_photo" size="4em" color="grey-5" />
              <div class="text-body1 q-mt-sm text-grey-7">
                {{ t('modelTester.result.noImage') }}
              </div>
            </div>

            <!-- 预览上传的图像 -->
            <div v-else-if="previewUrl && !resultImage" class="image-preview">
              <img :src="previewUrl" :alt="t('modelTester.result.preview')" />
            </div>

            <!-- 显示检测结果 -->
            <div v-else-if="resultImage" class="result-preview">
              <img :src="resultImage" :alt="t('modelTester.result.detectionResult')" />
              
              <div class="detection-list q-mt-md" v-if="detections && detections.length > 0">
                <div class="text-subtitle1 q-mb-sm">{{ t('modelTester.result.detectedObjects') }}</div>
                <q-list bordered separator class="rounded-borders">
                  <q-item v-for="(detection, index) in detections" :key="index">
                    <q-item-section avatar>
                      <q-avatar color="primary" text-color="white">
                        {{ index + 1 }}
                      </q-avatar>
                    </q-item-section>
                    <q-item-section>
                      <q-item-label>{{ detection.class_name }}</q-item-label>
                      <q-item-label caption>
                        {{ t('modelTester.result.confidence') }}: {{ (detection.confidence * 100).toFixed(1) }}%
                      </q-item-label>
                    </q-item-section>
                    <q-item-section side>
                      <q-badge color="primary">
                        {{ detection.class_id }}
                      </q-badge>
                    </q-item-section>
                  </q-item>
                </q-list>
              </div>
              
              <div class="no-detection q-mt-md" v-else>
                <q-icon name="info" color="info" />
                <span class="q-ml-sm">{{ t('modelTester.result.noDetection') }}</span>
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, defineProps, defineEmits, watch, onUnmounted } from 'vue';
import { useQuasar } from 'quasar';
import { useI18n } from 'vue-i18n';
import { modelService, Model } from '../../services/model';

const { t } = useI18n();
const $q = useQuasar();

interface Props {
  selectedModel: Model | null;
}

const props = defineProps<Props>();
const emit = defineEmits<{
  'update:selectedModel': [model: Model | null]
}>();

// 状态变量
const imageFile = ref<File | null>(null);
const previewUrl = ref<string | null>(null);
const loading = ref(false);
const capturing = ref(false);
const confThreshold = ref(0.5);
const iouThreshold = ref(0.7);
const maxDet = ref(300);
const agnosticNms = ref(false);
const imgSize = ref(640);
const autoRetest = ref(false);
const resultImage = ref<string | null>(null);
const detections = ref<any[] | null>(null);
const error = ref<string | null>(null);

// 跨类别去重：同一物体（IOU > 阈值）只保留置信度最高的框
function dedupBoxes(dets: any[], iouThreshold = 0.5): any[] {
  if (!dets || dets.length === 0) return [];
  // 按置信度从高到低排序
  const sorted = [...dets].sort((a, b) => b.confidence - a.confidence);
  const kept: any[] = [];
  for (const det of sorted) {
    let overlap = false;
    for (const k of kept) {
      const iou = calcIou(det.bbox, k.bbox);
      if (iou > iouThreshold) {
        overlap = true;
        break;
      }
    }
    if (!overlap) kept.push(det);
  }
  return kept;
}

function calcIou(box1: number[], box2: number[]): number {
  const [x1, y1, x2, y2] = box1;
  const [x1b, y1b, x2b, y2b] = box2;
  const ix1 = Math.max(x1, x1b);
  const iy1 = Math.max(y1, y1b);
  const ix2 = Math.min(x2, x2b);
  const iy2 = Math.min(y2, y2b);
  const iw = Math.max(0, ix2 - ix1);
  const ih = Math.max(0, iy2 - iy1);
  const inter = iw * ih;
  const area1 = (x2 - x1) * (y2 - y1);
  const area2 = (x2b - x1b) * (y2b - y1b);
  const union = area1 + area2 - inter;
  return union > 0 ? inter / union : 0;
}

// 在图片上画检测框，返回 dataURL
function drawBoxesOnImage(imageUrl: string, dets: any[]): Promise<string> {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.crossOrigin = 'anonymous';
    img.onload = () => {
      const canvas = document.createElement('canvas');
      canvas.width = img.width;
      canvas.height = img.height;
      const ctx = canvas.getContext('2d');
      if (!ctx) { resolve(imageUrl); return; }
      ctx.drawImage(img, 0, 0);
      // 画框
      for (const det of dets) {
        const [x1, y1, x2, y2] = det.bbox;
        ctx.strokeStyle = '#00ff00';
        ctx.lineWidth = 3;
        ctx.strokeRect(x1, y1, x2 - x1, y2 - y1);
        // 标签背景
        const label = `${det.class_name}`;
        ctx.font = 'bold 18px Arial';
        const tw = ctx.measureText(label).width;
        ctx.fillStyle = '#00ff00';
        ctx.fillRect(x1, Math.max(y1 - 25, 0), tw + 10, 22);
        ctx.fillStyle = '#000000';
        ctx.fillText(label, x1 + 5, Math.max(y1 - 8, 16));
      }
      resolve(canvas.toDataURL('image/jpeg', 0.9));
    };
    img.onerror = () => resolve(imageUrl);
    img.src = imageUrl;
  });
}

// 图像选择处理
const handleImageSelected = (file: File | null) => {
  if (!file) {
    previewUrl.value = null;
    return;
  }

  // 创建图像预览
  const reader = new FileReader();
  reader.onload = (e) => {
    previewUrl.value = e.target?.result as string;
  };
  reader.readAsDataURL(file);
  
  // 重置测试结果
  resultImage.value = null;
  detections.value = null;
  error.value = null;
};

// 摄像头抓拍
const captureFromCamera = async () => {
  capturing.value = true;
  try {
    const resp = await fetch('/api/cameras/0/snapshot?return_json=true');
    const data = await resp.json();
    if (data.image) {
      previewUrl.value = data.image;
      resultImage.value = null;
      detections.value = null;
      imageFile.value = null;
      $q.notify({ type: 'positive', message: t('modelTester.notifications.captureSuccess'), position: 'top' });
    } else {
      $q.notify({ type: 'negative', message: t('modelTester.notifications.captureFailed'), position: 'top' });
    }
  } catch (e: any) {
    $q.notify({
      type: 'negative',
      message: t('modelTester.notifications.cameraCaptureFailed', { error: e.message }),
      position: 'top'
    });
  } finally {
    capturing.value = false;
  }
};

// 测试模型
const testModel = async () => {
  if (!props.selectedModel || !previewUrl.value) {
    return;
  }

  loading.value = true;
  error.value = null;

  try {
    const imageBase64 = previewUrl.value;
    if (!imageBase64) {
      throw new Error(t('modelTester.notifications.noImageData'));
    }

    const result = await modelService.testModelWithBase64(props.selectedModel.id, imageBase64, {
      conf_thres: confThreshold.value,
      iou_thres: iouThreshold.value,
      max_det: maxDet.value,
      agnostic_nms: agnosticNms.value,
      imgsz: imgSize.value
    });

    if (result.success && result.image) {
      // 列表显示原始所有检测结果
      const rawDets = result.detections || [];
      detections.value = rawDets;
      // 图片里：先按置信度阈值过滤，再去重，只画每个硬币置信度最高的那个
      const filtered = rawDets.filter(d => d.confidence >= confThreshold.value);
      const deduped = dedupBoxes(filtered, 0.5);
      resultImage.value = await drawBoxesOnImage(previewUrl.value, deduped);
      
      if (rawDets.length === 0) {
        $q.notify({
          type: 'info',
          message: t('modelTester.notifications.noObjectsDetected'),
          position: 'top'
        });
      } else {
        $q.notify({
          type: 'positive',
          message: t('modelTester.notifications.detectionCount', { count: detections.value.length }),
          position: 'top'
        });
      }
    } else {
      error.value = result.error || t('modelTester.notifications.testFailed', { error: '' });
      $q.notify({
        type: 'negative',
        message: t('modelTester.notifications.testFailed', { error: error.value }),
        position: 'top'
      });
    }
  } catch (err: any) {
    error.value = err.message || t('modelTester.notifications.testError', { error: '' });
    $q.notify({
      type: 'negative',
      message: t('modelTester.notifications.testError', { error: error.value }),
      position: 'top'
    });
  } finally {
    loading.value = false;
  }
};

// 当模型改变时重置状态
watch(() => props.selectedModel, () => {
  imageFile.value = null;
  previewUrl.value = null;
  resultImage.value = null;
  detections.value = null;
  error.value = null;
  
  // 如果有模型，从模型参数中获取默认阈值
  if (props.selectedModel?.parameters) {
    confThreshold.value = props.selectedModel.parameters.conf_thres || 0.5;
    iouThreshold.value = props.selectedModel.parameters.iou_thres || 0.6;
  }
});

// 调参数自动重新推理（如果已经测试过且开关打开）
let debounceTimer: any = null;
watch([confThreshold, iouThreshold, maxDet, agnosticNms, imgSize], () => {
  if (!autoRetest.value) return;
  if (!previewUrl.value || !resultImage.value) return;
  if (loading.value) return;
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => {
    testModel();
  }, 500);
});
</script>

<style lang="scss" scoped>
.model-tester {
  padding: 8px;
}

.select-model-card,
.control-panel {
  background: var(--dark-card);
  border-radius: 8px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 250px;
  text-align: center;
}

.control-panel {
  align-items: stretch;
  text-align: left;
  justify-content: flex-start;
}

.result-card {
  background: var(--dark-card);
  border-radius: 8px;
  min-height: 450px;
}

.no-image-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 350px;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 4px;
}

.image-preview,
.result-preview {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 16px;
  
  img {
    max-width: 100%;
    max-height: 350px;
    object-fit: contain;
    border-radius: 4px;
  }
}

.detection-list {
  width: 100%;
}

.no-detection {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 12px;
  background: rgba(var(--q-info-rgb), 0.1);
  border-radius: 4px;
}
</style> 