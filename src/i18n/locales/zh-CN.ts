export default {
  common: {
    save: '保存',
    cancel: '取消',
    delete: '删除',
    edit: '编辑',
    add: '添加',
    confirm: '确认',
    minutes: '分钟',
    loading: '加载中...',
    success: '成功',
    error: '错误',
    warning: '警告',
    info: '信息',
    menu: '菜单',
    systemName: '工业监控系统',
    unknownError: '未知错误',
    to: '至',
  },
  settings: {
    system: {
      title: '系统参数配置',
      language: '系统语言',
      autoSaveInterval: '自动保存间隔',
      dataRetention: '数据保留时间',
      dataRetentionDays: '{count}天',
      alarmThreshold: '告警阈值'
    },
    mes: {
      title: 'MES集成',
      serverUrl: '服务器地址',
      apiKey: 'API密钥',
      testConnection: '测试连接'
    },
    devices: {
      title: '设备管理',
      all: '全部',
      camera: '相机',
      light: '光源',
      plc: '控制器',
      disableAutoCheck: '禁用自动检测',
      refreshStatus: '刷新设备状态',
      addDevice: '添加设备',
      status: {
        online: '在线',
        offline: '离线',
        error: '故障',
        unknown: '未知'
      },
      preview: {
        setOnline: '设为在线',
        setOffline: '设为离线',
        edit: '编辑设备',
        delete: '删除设备',
        title: '{name} 预览',
        status: '摄像头状态',
        streamUrl: '流地址',
        notConfigured: '未配置'
      },
      form: {
        title: {
          add: '添加设备',
          edit: '编辑设备'
        },
        name: '设备名称',
        nameRequired: '请输入设备名称',
        type: '设备类型',
        model: '设备型号',
        config: '设备配置',
        camera: {
          type: '摄像头类型',
          types: {
            local: '本地摄像头',
            ip: 'IP摄像头',
            rtsp: 'RTSP流',
            http: 'HTTP流'
          },
          deviceId: '设备ID',
          streamUrl: '摄像头URL'
        },
        light: {
          port: '串口',
          mode: '工作模式',
          modes: {
            continuous: '连续',
            flash: '闪烁',
            trigger: '触发'
          }
        },
        plc: {
          ip: 'IP地址',
          rack: '机架号',
          slot: '插槽号'
        }
      },
      noDevices: '暂无{type}设备',
      deleteConfirm: '确定要删除设备 "{name}" 吗？',
      type: {
        camera: '摄像头',
        light: '光源',
        plc: '控制器'
      }
    },
    notifications: {
      savingSettings: '正在保存系统设置...',
      settingsSaved: '系统设置已保存',
      savingFailed: '保存系统设置失败',
      savingMes: '正在保存MES设置...',
      mesSaved: 'MES设置已保存',
      mesSavingFailed: '保存MES设置失败',
      loadDevicesFailed: '加载设备列表失败',
      deviceUpdated: '设备已更新',
      deviceAdded: '设备已添加',
      deviceDeleted: '设备已删除',
      deviceSaveFailed: '保存设备失败',
      deviceDeleteFailed: '删除设备失败',
      cameraIdError: '无法获取摄像头ID，请检查配置',
      deviceStatusChanged: '{name} 已{status}',
      deviceStatusUpdateFailed: '更新设备状态失败',
      loadSettingsFailed: '加载系统设置失败',
      loadMesFailed: '加载MES设置失败',
      languageChanged: '语言已切换'
    }
  },
  status: {
    cameraList: '相机列表',
    noCameras: '没有配置相机设备',
    camera: '相机',
    modelList: '模型列表',
    noModels: '没有加载任何模型',
    model: '模型',
    deviceList: '设备列表',
    noDevices: '没有配置控制设备',
    device: '设备',
    online: '在线',
    offline: '离线',
    error: '错误',
    connected: '已连接',
    disconnected: '未连接',
    partiallyConnected: '部分在线',
    loaded: '已加载',
    notLoaded: '未加载'
  },
  emergencyStop: {
    title: '紧急停止',
    message: '确认执行紧急停止操作？这将停止所有设备运行。',
    confirm: '确认停止',
    executed: '已执行紧急停止操作'
  },
  routes: {
    dashboard: '仪表盘',
    realtime: '实时监控',
    history: '历史记录',
    annotation: '数据标注',
    model: '模型训练',
    modelTest: '模型测试',
    cvOperations: '流水线操作',
    settings: '系统设置',
    notFound: '页面未找到'
  },
  dashboard: {
    invalidDate: '无效日期',
    systemStatus: {
      title: '系统状态',
      uptime: '运行时间',
      memory: '内存',
      disk: '磁盘',
      systemNormal: '系统运行正常',
      systemLoadHigh: '系统负载较高',
      systemResourceStress: '系统资源紧张',
      systemStatusError: '无法获取系统状态',
      days: '天',
      hours: '小时',
      minutes: '分钟',
      seconds: '秒',
      unknown:'未知'
    },
    deviceStatus: {
      title: '设备状态',
      onlineRate: '在线率',
      total: '总设备',
      online: '在线',
      offline: '离线',
      error: '故障',
      cameras: '摄像头'
    },
    detectionStats: {
      title: '今日检测统计',
      comparedToYesterday: '比昨日 ({count}) {change}',
      increase: '增加',
      decrease: '减少'
    },
    defectStats: {
      title: '今日缺陷统计',
      comparedToYesterday: '比昨日 ({count}) {change}',
      increase: '增加',
      decrease: '减少'
    },
    accuracy: {
      title: '检测准确率',
      comparedToYesterday: '比昨日 ({value}%) {change}',
      improve: '提高',
      decrease: '降低',
      rate: '准确率'
    },
    alerts: {
      title: '最近告警',
      new: '新',
      noAlerts: '暂无告警'
    },
    trend: {
      title: '过去7天检测趋势',
      total: '检测总数',
      pass: '通过',
      fail: '失败'
    }
  },
  history: {
    searchText: '搜索文字',
    status: {
      title: '检测结果',
      all: '全部',
      pass: '合格',
      fail: '不合格',
      unknown: '未知'
    },
    dateRange: '时间范围',
    notifications: {
      loadFailed: '加载历史记录失败',
      deleteSuccess: '记录已删除',
      deleteFailed: '删除记录失败'
    },
    search: '搜索',
    export_excel: '导出',
    noData: '无历史记录数据',
    detail: {
      title: '检测记录详情',
      originalImage: '原始图像',
      processedImage: '处理后图像',
      noImage: '无图像',
      timestamp: '检测时间',
      status: '检测结果',
      text: '识别文字',
      noText: '无法识别',
      confidence: '置信度',
      device: '使用设备'
    },
    columns: {
      timestamp: '检测时间',
      text: '识别文字',
      confidence: '置信度',
      status: '检测结果',
      device: '使用设备',
      actions: '操作'
    },
    delete: {
      confirm: '确定要删除此检测记录吗?'
    },
    export: {
      loading: '正在准备导出数据...',
      noData: '没有符合条件的记录可导出',
      success: '成功导出 {count} 条记录',
      failed: '导出失败',
      fileName: '检测历史记录',
      columns: {
        timestamp: '检测时间',
        text: '识别文字',
        confidence: '置信度',
        status: '检测结果',
        device: '使用设备',
        imageUrl: '图像URL',
        processedImageUrl: '处理后图像URL'
      }
    }
  },
  annotation: {
    datasets: {
      title: '数据集',
      create: '新建数据集',
      count: '{count} 个数据集',
      imageCount: '{count} 张图片'
    },
    selectDataset: '请选择数据集',
    selectImage: '请选择图片',
    selectImageHint: '从左侧图片列表中选择一张图片进行标注',
    actions: {
      deleteSelected: '删除选中',
      upload: '上传图片',
      rename: '重命名',
      gridView: '网格视图',
      annotationView: '标注视图',
      export: '导出标注数据集',
      import: '导入标注数据集',
      generate: '合成数据',
      more: '更多',
      deleteDataset: '删除数据集'
    },
    trash: {
      title: '垃圾箱',
      imageCount: '{count} 张图片',
      empty: '垃圾箱为空',
      hint: '删除的图片会先移到这里，可随时恢复。',
      restore: '恢复',
      deletePermanently: '永久删除',
      confirmDeleteTitle: '删除图片',
      confirmDelete: '确定删除「{name}」吗？删除后将移入垃圾箱，可随时恢复。',
      confirmPermanentlyTitle: '永久删除',
      confirmPermanently: '确定永久删除「{name}」吗？此操作不可恢复，将同时删除文件与标注。',
      moved: '已移入垃圾箱',
      restored: '已恢复「{name}」',
      restoreFailed: '恢复图片失败',
      deleted: '已永久删除',
      deleteFailed: '永久删除失败'
    },
    camera: {
      captureAndUpload: '摄像头拍摄并上传',
      starting: '正在启动摄像头…',
      takePhotoAndUpload: '拍照并上传',
      notSupported: '当前浏览器不支持摄像头访问，请使用 Chrome/Edge。',
      inUseTitle: '摄像头被占用',
      inUse: '检测到摄像头正被其他程序使用，是否强制切换？这将关闭占用摄像头的应用（如 Windows 相机、Teams、Zoom 或 OBS）。',
      forceSwitch: '强制切换',
      forceSwitchFailed: '强制切换失败，请手动关闭占用摄像头的程序。',
      accessFailed: '无法访问摄像头，请检查摄像头是否被占用。',
      photoFailed: '拍照失败',
      photoSuccess: '拍照并上传成功',
      photoUploadFailed: '拍照上传失败，请重试。'
    },
    dialogs: {
      upload: {
        title: '上传图片',
        selectFiles: '选择图片',
        upload: '上传'
      },
      create: {
        title: '新建数据集',
        name: '数据集名称',
        nameRequired: '请输入数据集名称',
        type: '数据集类型',
        create: '创建'
      },
      rename: {
        title: '重命名数据集',
        name: '数据集名称',
        nameRequired: '请输入数据集名称'
      },
      delete: {
        title: '确认删除',
        confirmImages: '确定要删除选中的 {count} 张图片吗？此操作不可恢复。',
        confirmDataset: '确定要删除数据集 "{name}" 吗？此操作不可恢复。'
      }
    },
    datasetTypes: {
      textRegion: '文本区域数据集',
      ocr: 'OCR数据集'
    },
    notifications: {
      loadDatasetsFailed: '加载数据集失败，请重试',
      createDatasetSuccess: '创建数据集成功',
      createDatasetFailed: '创建数据集失败，请重试',
      renameSuccess: '重命名成功',
      renameFailed: '重命名失败，请重试',
      deleteDatasetSuccess: '删除数据集成功',
      deleteDatasetFailed: '删除数据集失败，请重试',
      deleteImageSuccess: '删除图片成功',
      deleteImageFailed: '删除图片失败，请重试',
      loadImagesFailed: '加载图片失败，请重试',
      uploadSuccess: '上传图片成功',
      uploadFailed: '上传图片失败，请重试',
      selectDataset: '请先选择一个数据集',
      importProgress: '正在导入标注数据...',
      exportProgress: '正在导出标注数据集...',
      importComplete: '导入完成：{success} 个成功，{failed} 个失败',
      importSuccess: '成功导入 {count} 条标注数据',
      importFailed: '导入失败',
      exportSuccess: '标注数据集导出成功',
      exportFailed: '导出标注数据集失败，请重试',
      importFileTooLarge: '文件大小不能超过 10 MB',
      importFileType: '只支持 .xlsx 格式的文件',
      importMissingField: '导入文件格式不正确，缺少必要的标注数据字段',
      invalidAnnotationData: '标注数据格式不正确',
      importItemFailed: '导入第 {index} 条标注数据失败：{error}'
    }
  },
  annotator: {
    controls: {
      zoomIn: '放大',
      zoomOut: '缩小',
      save: '保存标注',
      reload: '重新加载',
      deleteSelectedChar: '删除选中 ({char})',
      cancelDrawing: '取消绘制',
      closeDetails: '关闭详情',
      enterFullscreen: '全屏预览',
      exitFullscreen: '退出全屏',
      deleteSelected: '删除选中'
    },
    tools: {
      textRegion: '文本区域 (多边形)',
      character: '字符标注 (矩形)',
      wheelText: '带字轮毂 (矩形)'
    },
    ocr: {
      currentChar: '当前字符',
      selectChar: '选择字符',
      commonChars: '常用字符',
      more: '更多',
      char: '字符',
      position: '位置',
      selectCharTitle: '选择标注字符',
      inputChar: '输入字符',
      singleCharRequired: '请输入单个字符',
      commonCharSets: '常用字符集',
      recentlyUsed: '最近使用',
      selectCharFirst: '请先选择一个字符'
    },
    preview: {
      toggleAnnotations: '显示/隐藏标注',
      toggleLabels: '显示/隐藏标签',
      label: '标签',
      position: '位置',
      clickToViewDetails: '点击查看详情',
      loading: '加载中...'
    },
    notifications: {
      loadFailed: '加载标注失败',
      saveSuccess: '标注已保存',
      saveFailed: '保存标注失败',
      deleteFailed: '删除标注失败'
    }
  },
  notFound: {
    message: '页面未找到',
    backToHome: '返回首页'
  },
  generateData: {
    title: '数据生成',
    nameSuffix: '_生成',
    sourceDataset: {
      title: '源数据集信息',
      name: '数据集名称',
      imageCount: '{count} 张图片',
      annotatedCount: '{count} 张已标注',
      operation: '操作'
    },
    targetDataset: {
      title: '目标数据集',
      newOption: '创建新数据集',
      existingOption: '使用已有数据集',
      sourceOption: '使用源数据集',
      type: '数据集类型',
      select: '选择数据集',
      new: {
        name: {
          label: '新数据集名称',
          required: '请输入数据集名称'
        }
      },
      existing: {
        select: '请选择目标数据集'
      }
    },
    generateOptions: {
      title: '生成选项',
      includeAnnotations: '包含标注',
      includeAnnotationsHint: '如果选中，将同时复制原始图片的标注数据'
    },
    operations: {
      title: '操作选择',
      available: '可用操作',
      selected: '已选操作',
      configure: '配置参数',
      duplicate: '复制操作',
      remove: '移除操作',
      single: '单步',
      pipeline: '流水线'
    },
    preview: {
      title: '预览',
      sourceImage: '源图片',
      imageId: 'ID: {id}',
      originalImage: '原始图片',
      operationResult: {
        single: '单步',
        pipeline: '流水线'
      }
    },
    actions: {
      preview: '生成预览',
      generate: '开始生成'
    },
    progress: {
      title: '生成进度',
      cancel: '取消生成',
      close: '关闭',
      preparing: '正在准备数据...',
      processed: '已处理 {count} / {total} 个操作',
      generating: '正在生成: {name} ({count}/{total})',
      creatingTarget: '正在创建目标数据集...'
    },
    configuration: {
      title: '{name} 参数配置',
      sections: {
        input: '输入参数',
        output: '输出参数'
      },
      params: {
        required: '必填参数',
        optional: '可选参数',
        defaultValue: '默认值: {value}',
        yes: '是',
        no: '否'
      },
      imageParam: {
        hint: '选择图片输入来源',
        useDataset: '使用数据集图片',
        upload: '上传自定义图片'
      },
      annotationParam: {
        hint: '选择标注数据来源',
        useDataset: '使用数据集标注',
        custom: '自定义标注数据',
        customHint: '请输入有效的JSON格式标注数据'
      },
      output: {
        hint: '选择要保存的输出结果',
        image: {
          title: '图片输出',
          noOutput: '此操作没有图片输出'
        },
        annotation: {
          title: '标注输出',
          noOutput: '此操作没有标注输出'
        }
      },
      actions: {
        reset: '重置参数',
        close: '关闭'
      }
    },
    notifications: {
      loadError: '加载数据失败',
      previewError: '生成预览失败',
      generateSuccess: '数据生成完成',
      generateError: '数据生成失败',
      cancelConfirm: {
        title: '取消确认',
        message: '确定要取消当前的生成任务吗？',
        canceled: '已取消生成任务'
      }
    }
  },
  modelTester: {
    selectModel: {
      title: '请先选择模型',
      hint: '在模型列表中选择一个已训练完成的模型来测试'
    },
    model: {
      id: '模型ID'
    },
    params: {
      title: '参数设置',
      confThreshold: '置信度阈值',
      iouThreshold: 'IOU阈值',
      preprocessing: '前级（预处理）',
      imageSize: '推理图像尺寸 (imgsz)',
      postprocessing: '后级（后处理 / NMS）',
      maxDetections: '最大检测数 (max_det)',
      classAgnosticNms: '类别无关 NMS (agnostic)',
      autoRetest: '自动重新推理（调参后自动重测）'
    },
    image: {
      title: '测试图像',
      select: '选择图像',
      test: '测试模型',
      cameraCapture: '摄像头抓拍'
    },
    result: {
      title: '测试结果',
      noImage: '请上传图像进行测试',
      preview: '预览图像',
      detectionResult: '检测结果',
      detectedObjects: '检测到的对象：',
      confidence: '置信度',
      noDetection: '未检测到任何对象'
    },
    notifications: {
      noImageData: '未能获取图像数据',
      noObjectsDetected: '未检测到任何对象',
      detectionCount: '检测到 {count} 个对象',
      testFailed: '测试失败: {error}',
      testError: '测试出错: {error}',
      captureSuccess: '抓拍成功',
      captureFailed: '抓拍失败',
      cameraCaptureFailed: '摄像头抓拍失败: {error}'
    }
  },
  alarmPanel: {
    title: {
      info: '系统通知',
      warning: '系统警告',
      error: '系统错误',
      critical: '严重故障',
      default: '系统告警'
    },
    actions: {
      acknowledgeAll: '确认所有',
      close: '关闭'
    },
    status: {
      alarmCount: '共 {count} 条告警',
      emergencyStop: '紧急停止'
    },
    notifications: {
      alarmAcknowledged: '告警已确认',
      allAlarmsAcknowledged: '所有告警已确认'
    }
  },
  cameraPreview: {
    loading: '加载摄像头...',
    error: {
      connection: '无法连接到摄像头',
      status: '获取摄像头状态出错:'
    },
    stream: {
      alt: '摄像头画面'
    }
  },
  model: {
    list: {
      title: '模型列表',
      empty: '暂无模型',
      create: '新建模型',
      refresh: '刷新列表',
      architecture: '模型架构',
      actions: {
        test: '测试模型',
        delete: '删除模型'
      }
    },
    training: {
      title: '训练参数',
      params: {
        architecture: '模型架构',
        device: '训练设备',
        deviceAuto: '自动（检测 CUDA GPU）',
        epochs: '训练轮数',
        batchSize: '批次大小',
        imgSize: '图像尺寸',
        confThres: '置信度阈值',
        iouThres: 'IOU阈值'
      },
      start: '开始训练',
      stop: '停止训练',
      modes: {
        config: '配置训练',
        test: '测试模型',
        logs: '训练日志',
        files: '训练文件'
      },
      actions: {
        startTraining: '开始训练',
        stopTraining: '停止训练',
        testModel: '测试模型',
        viewLogs: '查看日志',
        viewFiles: '查看文件'
      },
      status: {
        notStarted: '未开始',
        training: '训练中',
        completed: '已完成',
        failed: '失败',
        trainingWithDots: '训练中{dots}'
      },
      timeUnits: {
        hours: '{count}小时',
        minutes: '{count}分钟',
        seconds: '{count}秒'
      }
    },
    progress: {
      title: '训练进度',
      refresh: '刷新进度',
      epoch: '当前轮数',
      loss: '损失值',
      eta: '预计剩余时间'
    },
    logs: {
      title: '训练日志',
      refresh: '刷新日志',
      copy: '复制日志',
      scrollToBottom: '滚动到底部',
      empty: '暂无日志'
    },
    files: {
      title: '模型文件',
      refresh: '刷新文件',
      root: '返回根目录',
      download: '下载文件',
      preview: '预览文件',
      empty: '暂无文件',
      directory: '目录',
      previewImageAlt: '文件预览',
      unableToLoadContent: '无法加载文件内容：{name}',
      upLevel: '上级目录',
      previewDialog: {
        unsupported: '此文件类型暂不支持预览',
        actions: {
          download: '下载',
          close: '关闭'
        }
      },
      actions: {
        root: '返回根目录'
      }
    },
    dialogs: {
      create: {
        title: '新建模型',
        name: '模型名称',
        nameRequired: '请输入模型名称',
        dataset: '训练数据集',
        datasetRequired: '请选择训练数据集'
      },
      delete: {
        message: '确定要删除模型 {name} 吗？此操作不可恢复。'
      }
    },
    notifications: {
      createSuccess: '创建模型成功',
      createFailed: '创建模型失败：{error}',
      deleteSuccess: '删除模型成功',
      deleteFailed: '删除模型失败：{error}',
      trainStarted: '开始训练模型',
      trainFailed: '启动训练失败：{error}',
      updateParamsFailed: '更新参数失败：{error}',
      loadDatasetsFailed: '加载数据集失败',
      copyModelId: '已复制模型ID',
      copyModelIdFailed: '复制模型ID失败',
      copyLogs: '已复制日志',
      copyLogsFailed: '复制日志失败',
      downloadStarted: '开始下载 {name}',
      trainingStopped: '训练已停止',
      stopTrainingFailed: '停止训练失败',
      exportSuccess: '模型导出成功：{path}',
      exportFailed: '导出模型失败：{error}',
      loadModelsFailed: '加载模型列表失败',
      loadFilesFailed: '获取模型文件列表失败'
    },
    status: {
      empty: '请选择一个模型',
      emptyHint: '从左侧模型列表中选择一个模型，或者创建新的模型',
      notTraining: '模型当前未处于训练状态，没有训练日志',
      notCompleted: '此模型未完成训练，无法进行测试',
      selectFeature: '请选择功能或操作'
    },
  },
  realtime: {
    title: '实时监控',
    camera: {
      select: '选择相机',
      video: '相机视频',
      processed: '处理后视频',
      processing: '处理中...',
      streamActive: '处理流已激活',
      streamWaiting: '等待处理流...'
    },
    operation: {
      title: '操作选择',
      select: '选择图像处理操作',
      selectRequired: '请选择操作',
      none: '无操作',
      unknown: '未知操作',
      noSuitable: '没有找到合适的图像处理操作，请确保操作有图像输入',
      noValid: '未找到有效的图像处理操作，请检查系统配置',
      pleaseSelect: '请先选择一个操作，再进行图像处理',
      types: {
        single: '单步',
        pipeline: '流水线'
      },
      testOnce: '单次测试',
      apply: '应用操作',
      startStream: '实时处理流',
      stopStream: '停止处理流',
      detection: '检测'
    },
    batch: {
      title: '批量识别结果',
      count: '共 {count} 张图片',
      processing: '处理中',
      done: '处理完成',
      originalImage: '原始图像',
      resultImage: '处理结果',
      failed: '处理失败: {error}',
      filename: '文件名',
      status: '识别状态',
      passed: '通过',
      failedStatus: '失败',
      text: '识别文本',
      noText: '未识别到文本',
      confidence: '置信度',
      summary: {
        total: '总计',
        totalUnit: '图片数量',
        pass: '通过',
        passUnit: '识别成功',
        fail: '失败',
        failUnit: '识别失败'
      },
      progress: '正在批量处理图片 ({current}/{total})...',
      complete: '批量处理完成，共处理 {count} 张图片',
      failedGeneric: '批量处理失败: {error}'
    },
    result: {
      title: '检测结果',
      waiting: '等待检测结果...',
      status: {
        pass: '合格',
        fail: '不合格'
      },
      details: {
        time: '检测时间',
        source: '图像来源',
        text: '识别文字',
        confidence: '置信度',
        error: '错误原因',
        filename: '文件名',
        noText: '无法识别'
      }
    },
    control: {
      title: '相机控制',
      autoDetect: {
        start: '开始自动检测',
        stop: '停止自动检测'
      },
      capture: '单次采集',
      exposure: '曝光时间',
      gain: '增益'
    },
    notifications: {
      selectCamera: '请先选择一个相机',
      selectOperation: '请先选择一个操作',
      cameraUnavailable: '选择的相机当前不可用',
      startProcessing: '正在启动视频处理...',
      invalidOperation: '无效的操作信息',
      streamStarted: '实时处理已启动',
      streamStartFailed: '启动处理流失败: {error}',
      stopProcessing: '正在停止视频处理...',
      streamStopped: '实时处理已停止',
      streamError: '处理流加载失败，请检查相机和网络连接',
      retrying: '处理流加载中，正在重试...',
      streamConnected: '处理流已连接',
      autoDetectStarted: '自动检测已开启',
      autoDetectStopped: '自动检测已停止',
      processingComplete: '图像处理完成',
      processingFailed: '处理图像失败: {error}',
      uploadImage: '没有活动的相机流，请上传一张图片',
      noCameraControl: '找不到相机控件',
      cameraSelected: '已选择相机: {name}',
      stopStreamWarning: '停止处理时遇到问题，请检查后端服务状态',
      stopStreamFailed: '停止处理流失败: {error}',
      sourceUploaded: '上传的图片',
      sourceCamera: '相机捕获',
      processingSource: '正在处理{source}...',
      invalidOperationId: '无效的操作ID',
      noCameraSelected: '未选择摄像头',
      loadOperationsFailed: '加载操作列表失败',
      loadCamerasFailed: '获取相机列表失败',
      updateSettingsFailed: '更新相机设置失败',
      getOriginalImageFailed: '获取原始图像失败',
      processFailed: '处理失败',
      unknownError: '未知错误',
      batchUpload: '批量上传',
      cameraStreamFailed: '相机流连接失败，请检查相机状态',
      cameraError: '相机错误: {error}'
    },
    status: {
      online: '在线',
      offline: '离线',
      error: '故障',
      unknown: '未知'
    }
  },
  cvOperation: {
    tabs: {
      single: '单步处理',
      pipeline: '流水线处理'
    }
  },
  camera: {
    capture: {
      loading: '加载摄像头...',
      error: '处理流加载失败，请检查相机和网络连接',
      noCamera: '无可用相机，请上传图片',
      uploadedImage: '已上传图片，等待处理',
      videoStream: '视频流',
      streamStatus: '视频流状态:',
      streaming: '正在监控',
      stopped: '已停止',
      useUploadedImage: '使用此图片处理',
      reupload: '重新上传',
      capture: '拍照',
      uploadImage: '上传图片',
      stopMonitoring: '停止监控',
      startMonitoring: '开始监控',
      messages: {
        noStreamUrl: '未提供视频流地址',
        videoElementMissing: '未找到视频元素',
        processingWait: '正在处理中，请等待完成',
        cameraNotReady: '摄像头未就绪',
        captureFailed: '捕获图像失败',
        noUploadedImage: '没有上传的图片',
        readyForProcessing: '图片准备好进行处理',
        imageOnly: '请只上传图片文件',
        preparingImages: '正在准备处理 {count} 张图片',
        imageReadFailed: '图片读取失败',
        unknownError: '未知错误',
        unableToReadImage: '无法读取图片数据',
        batchFailed: '批量处理图片失败',
        uploadFailed: '处理上传文件失败'
      }
    }
  },
  cv: {
    parameter: {
      name: '参数名称',
      nameRequired: '请输入参数名称',
      type: '参数类型',
      typeRequired: '请选择参数类型',
      description: '描述',
      defaultValue: '默认值',
      required: '必需参数'
    },
    operation: {
      new: '新建操作',
      import: '导入',
      importTooltip: '导入操作配置',
      export: '导出',
      exportTooltip: '导出操作配置',
      delete: '删除',
      deleteSelected: '删除 ({count})',
      deleteTooltip: '批量删除选中的操作',
      operationCount: '{count} 个操作',
      search: '搜索操作名称或描述',
      refresh: '刷新列表',
      columns: {
        name: '操作名称',
        description: '描述',
        createdAt: '创建时间',
        actions: '操作'
      },
      actions: {
        edit: '编辑',
        test: '测试',
        delete: '删除'
      },
      deleteConfirm: {
        title: '删除确认',
        singleMessage: '确定要删除操作 "{name}" 吗？',
        batchMessage: '确定要删除选中的 {count} 个操作吗？',
        cancel: '取消',
        confirm: '删除'
      },
      validation: {
        nameRequired: '操作名称不能为空',
        invalidCode: '代码格式不正确',
        fileSizeLimit: '文件大小不能超过 10MB',
        fileTypeError: '只支持 .xlsx 格式的文件',
        missingField: '缺少必需字段: {field}'
      },
      importExport: {
        importErrorDetails: '导入错误详情',
        exportColumns: {
          name: '操作名称',
          description: '描述',
          code: '代码',
          inputParams: '输入参数',
          outputParams: '输出参数',
          createdAt: '创建时间',
          updatedAt: '更新时间'
        },
        exportSheetName: '操作列表',
        exportFileName: 'cv_operations'
      },
      notifications: {
        loadError: '加载操作失败',
        saveSuccess: '保存成功',
        saveError: '保存失败',
        deleteSuccess: '删除成功',
        batchDeleteSuccess: '批量删除成功',
        deleteError: '删除失败',
        importFailed: '导入操作 "{name}" 失败',
        importPartialSuccess: '导入完成: {success}个成功, {failed}个失败',
        importSuccess: '成功导入 {count} 个操作',
        importError: '导入失败',
        exportSuccess: '成功导出 {count} 个操作',
        exportError: '导出失败'
      },

    },
    operationEditor: {
      title: {
        edit: '编辑操作',
        new: '新建操作'
      },
      actions: {
        test: '运行',
        save: '保存',
        close: '关闭'
      },
      basicInfo: {
        title: '基本信息',
        name: '操作名称',
        nameRequired: '请输入操作名称',
        description: '描述'
      },
      parameters: {
        title: '参数配置',
        tabs: {
          input: '输入参数',
          output: '输出参数'
        },
        param: '参数 {index}',
        addInput: '添加输入参数',
        addOutput: '添加输出参数'
      },
      codeEditor: {
        title: 'Python 代码编辑器'
      },
      notifications: {
        initError: '初始化编辑器失败',
        extractError: '提取用户代码失败',
        updateError: '更新代码模板失败',
        editorError: '获取编辑器内容失败',
        setContentError: '设置编辑器内容失败'
      }
    },
    pipeline: {
      new: '新建流水线',
      import: '导入',
      importTooltip: '导入流水线配置',
      export: '导出',
      exportTooltip: '导出流水线配置',
      delete: '删除',
      deleteSelected: '删除 ({count})',
      deleteTooltip: '批量删除选中的流水线',
      pipelineCount: '{count} 个流水线',
      nodeCount: '{count} 个节点',
      search: '搜索流水线名称或描述',
      refresh: '刷新列表',
      columns: {
        name: '流水线名称',
        description: '描述',
        nodes: '节点数',
        createdAt: '创建时间',
        actions: '操作'
      },
      actions: {
        edit: '编辑',
        test: '测试',
        delete: '删除'
      },
      deleteConfirm: {
        title: '删除确认',
        singleMessage: '确定要删除流水线 "{name}" 吗？',
        batchMessage: '确定要删除选中的 {count} 个流水线吗？',
        cancel: '取消',
        confirm: '删除'
      },
      validation: {
        nameRequired: '流水线名称不能为空',
        metadataRequired: '流水线元数据不能为空',
        invalidMetadata: '流水线配置无效',
        fileSizeLimit: '文件大小不能超过10MB',
        fileTypeError: '只支持.xlsx格式的文件',
        missingField: '缺少必需字段: {field}'
      },
      importExport: {
        errorDetails: '导入错误详情',
        columns: {
          name: '流水线名称',
          description: '描述',
          metadata: '元数据',
          inputParams: '输入参数',
          outputParams: '输出参数',
          createdAt: '创建时间',
          updatedAt: '更新时间'
        },
        sheetName: '流水线列表',
        fileName: 'pipelines'
      },
      notifications: {
        loadError: '加载流水线失败',
        saveSuccess: '保存成功',
        saveError: '保存失败',
        deleteSuccess: '删除成功',
        batchDeleteSuccess: '批量删除成功',
        deleteError: '删除失败',
        importFailed: '导入流水线 "{name}" 失败：{error}',
        importPartialSuccess: '导入完成：{success} 个成功，{failed} 个失败',
        importSuccess: '成功导入 {count} 个流水线',
        importError: '导入失败',
        exportSuccess: '成功导出 {count} 个流水线',
        exportError: '导出失败',
        testPanelError: '无法打开测试面板：流水线不存在',
        jsonParseError: 'JSON解析失败'
      },
    },
    pipelineEditor: {
        title: {
          new: '新建流水线',
          edit: '编辑流水线'
        },
        actions: {
          run: '运行',
          save: '保存',
          close: '关闭'
        },
        basicInfo: {
          title: '基本信息',
          name: '流水线名称',
          nameRequired: '请输入流水线名称',
          description: '描述'
        },
        nodeToolbox: {
          title: '节点工具箱'
        },
        nodeTypes: {
          start: '开始',
          end: '结束',
          operation: '操作',
          parallel: '并行',
          merge: '合并',
          condition: '条件',
          unknown: '未知'
        },
        parameters: {
          inputTitle: '输入参数配置',
          outputTitle: '输出参数配置',
          item: '参数 {index}',
          addInput: '添加输入参数',
          addOutput: '添加输出参数',
          mapOutput: '映射到节点输出',
          noMatchingOutput: '没有找到匹配类型的节点输出',
          noTrainedModels: '没有找到已训练的模型，请先训练模型',
          noDescription: '无描述',
          pipelineInput: '流水线输入: {name}',
          nodeOutput: '{node} 输出: {name}',
          valueSource: '值来源',
          customValue: '自定义值',
          customValueJson: '自定义值 (JSON格式)',
          condition: '条件表达式',
          conditionHint: '使用 JavaScript 表达式，例如: input.value > 10'
        },
        nodeProperties: {
          title: '节点属性',
          name: '节点名称',
          operation: '选择操作',
          noOperationFound: '没有找到匹配的操作',
          noDescription: '无描述',
          parameters: {
            title: '参数配置',
            valueSource: '值来源',
            customValue: '自定义值',
            customValueJson: '自定义值 (JSON格式)'
          }
        },
        flowEditor: {
          title: '流水线设计器',
          undo: '撤销 (Ctrl+Z)',
          redo: '重做 (Ctrl+Y)',
          delete: '删除选中元素 (Delete)',
          clear: '清空画布',
          clearConfirmTitle: '确认清空',
          clearConfirmMessage: '确定要清空流水线设计吗？此操作不可恢复。',
          center: '居中视图',
          zoomIn: '放大',
          zoomOut: '缩小',
          yes: '是',
          no: '否'
        },
        notifications: {
          cannotDeleteStartEnd: '不能删除开始和结束节点',
          initFailed: '初始化流水线设计器失败',
          operationLoadFailed: '加载操作详情失败',
          operationLoadError: '获取操作详情失败',
          operationNotSelected: '操作节点“{name}”尚未选择操作',
          invalidOperationInputCount: '操作节点只能有一个入度',
          invalidOperationOutputCount: '操作节点只能有一个出度',
          invalidConditionInputCount: '条件节点只能有一个入度',
          invalidConditionOutputCount: '条件节点只能有两个出度',
          invalidParallelInputCount: '并行节点只能有一个入度，可以有多个出度',
          invalidMergeOutputCount: '合并节点只能有一个出度，可以有多个入度',
          invalidStartEdges: '开始节点只能有出度，不能有入度',
          invalidEndEdges: '结束节点只能有入度，不能有出度',
          invalidCanvas: '初始化画布失败',
          operationOnlyEdge: '操作节点只能有一个入度',
          operationOnlyOutgoingEdge: '操作节点只能有一个出度'
        }
      },
    pipelineTestPanel: {
        title: '流水线测试',
        actions: {
          run: '运行',
          close: '关闭',
          clearLogs: '清空日志'
        },
        input: {
          title: '输入参数',
          required: '必填项',
          cameraCapture: '摄像头抓拍',
          jsonFormat: ' (JSON格式)',
          invalidJson: '请输入有效的JSON格式'
        },
        output: {
          title: '输出结果',
          noData: '无数据',
          imagePreview: '图像数据预览',
          image: '[图像数据]'
        },
        log: {
          title: '执行日志',
          empty: '尚无执行日志，请运行流水线'
        },
        notifications: {
          captureSuccess: '摄像头抓拍成功',
          captureNoImage: '抓拍失败：未获取到图片',
          captureFailed: '抓拍失败: {error}',
          required: '{name} 是必填项',
          invalidJson: '{name} 的值不是有效的 JSON 格式',
          ready: '准备执行流水线',
          inputsReady: '输入参数准备完成: {names}',
          output: '输出参数 {name}: {value}',
          success: '流水线执行成功',
          failed: '执行失败: {error}'
        }
    },
    operationTestPanel: {
      title: '操作测试',
      actions: {
        run: '运行',
        close: '关闭'
      },
      input: {
        title: '输入参数',
        jsonFormat: ' (JSON格式)'
      },
      output: {
        title: '输出结果'
      },
      validation: {
        required: '必填项',
        invalidJson: '请输入有效的JSON格式'
      },
      notifications: {
        required: '{name} 是必填项',
        invalidJson: '{name} 的值不是有效的 JSON 格式',
        saveFirst: '请先保存操作',
        success: '测试运行成功',
        failed: '测试运行失败'
      }
    }
  }
} 