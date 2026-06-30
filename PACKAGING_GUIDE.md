# 打包模式选择指南

## 两种打包模式对比

| 特性 | `--onefile`（单文件） | `--onedir`（文件夹） |
|------|---------------------|---------------------|
| **临时文件** | ✅ 每次运行都生成 | ❌ **不生成临时文件** |
| **启动速度** | ⚠️ 较慢（需要解压） | ✅ 快速（直接运行） |
| **文件结构** | 单个 .exe 文件 | 包含所有文件的文件夹 |
| **调试便利性** | ❌ 困难 | ✅ 容易查看和修改文件 |
| **分发方式** | 单个文件 | 压缩整个文件夹 |
| **磁盘空间** | 运行时占用临时空间 | 占用固定空间 |

## 推荐方案：文件夹模式（不生成临时文件）

### 打包命令
```bash
# 方法1：直接使用 PyInstaller
pyinstaller --onedir --noconsole --uac-admin --name ok-script-app ^
  --add-data assets;assets ^
  --add-data i18n;i18n ^
  --add-data ok_tasks;ok_tasks ^
  --hidden-import ok_tasks.SortieMode ^
  --hidden-import ok_tasks.ChaosMode ^
  --hidden-import utils_sortie ^
  --hidden-import utils_chaos ^
  --hidden-import src.globals ^
  --hidden-import src.tasks.MyOneTimeTask ^
  --hidden-import onnxocr ^
  --hidden-import onnxocr_ppocrv5 ^
  --collect-all onnxocr ^
  --collect-all openvino ^
  --collect-all pyappify ^
  main.py

# 方法2：使用提供的脚本（推荐）
python build_onedir.py
```

### 生成的目录结构
```
dist/ok-script-app/
├── ok-script-app.exe     # 主程序
├── assets/               # 资源文件
├── i18n/                 # 国际化文件
├── ok_tasks/             # 任务模块
├── _internal/            # Python 运行时和依赖库
└── 其他必要的 DLL 文件
```

### 使用方式
1. 将整个 `dist/ok-script-app/` 文件夹分发给用户
2. 用户直接运行 `ok-script-app.exe` 
3. **不会生成任何临时文件**

## 代码修改说明

`main.py` 已更新为支持两种模式：

```python
if getattr(sys, 'frozen', False):
    if hasattr(sys, '_MEIPASS'):
        # --onefile 模式：切换到临时解压目录
        exe_dir = os.path.dirname(sys.executable)
        os.chdir(sys._MEIPASS)
        config["config_folder"] = os.path.join(exe_dir, "configs")
    else:
        # --onedir 模式：使用 exe 所在目录
        exe_dir = os.path.dirname(sys.executable)
        config["config_folder"] = os.path.join(exe_dir, "configs")
```

## 方案二：优化单文件模式（可选）

如果您仍想要单文件但减少临时文件影响，可以：

1. **使用 SSD**：临时文件解压到 SSD 会快很多
2. **清理脚本**：程序退出时自动清理临时文件
3. **指定临时目录**：使用 `--runtime-tmpdir` 指定固定位置

但**文件夹模式仍然是解决临时文件问题的最佳方案**。