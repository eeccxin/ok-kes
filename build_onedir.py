#!/usr/bin/env python3
"""
文件夹模式打包脚本 - 不生成临时文件
"""

import subprocess
import sys
import os
import shutil
import zipfile
from datetime import datetime

def clean_output_directory():
    """清理输出目录"""
    output_dir = "dist/ok-script-app"
    if os.path.exists(output_dir):
        print(f"🧹 清理现有目录: {output_dir}")
        shutil.rmtree(output_dir)
        print("✅ 目录清理完成")
    else:
        print(f"📁 输出目录不存在，无需清理: {output_dir}")

def create_zip_archive():
    """创建zip压缩文件"""
    source_dir = "dist/ok-script-app"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"dist/ok-script-app_{timestamp}.zip"
    
    if not os.path.exists(source_dir):
        print(f"❌ 源目录不存在: {source_dir}")
        return False
    
    print(f"📦 创建压缩文件: {zip_filename}")
    
    try:
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(source_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    # 计算在zip中的相对路径
                    arcname = os.path.relpath(file_path, source_dir)
                    zipf.write(file_path, arcname)
                    print(f"  📄 添加文件: {arcname}")
        
        # 显示压缩文件信息
        file_size = os.path.getsize(zip_filename) / (1024 * 1024)  # MB
        print(f"✅ 压缩完成！文件大小: {file_size:.2f} MB")
        print(f"📍 压缩文件位置: {zip_filename}")
        return True
        
    except Exception as e:
        print(f"❌ 压缩失败: {e}")
        return False

def create_runtime_hook():
    """创建运行时钩子文件，禁用 Tkinter 自动检测"""
    hook_content = '''# runtime-hook.py
# 禁用 Tkinter 运行时钩子，因为我们使用的是 PySide6
import sys
import os

# 防止 PyInstaller 自动包含 Tkinter 运行时钩子
if hasattr(sys, '_MEIPASS'):
    # 在打包环境中，设置 TCL_LIBRARY 和 TK_LIBRARY 环境变量
    tcl_dir = os.path.join(sys._MEIPASS, '_internal', 'tcl')
    tk_dir = os.path.join(sys._MEIPASS, '_internal', 'tk')
    
    if os.path.exists(tcl_dir):
        os.environ['TCL_LIBRARY'] = tcl_dir
    if os.path.exists(tk_dir):
        os.environ['TK_LIBRARY'] = tk_dir
'''
    
    hook_file = "runtime-hook.py"
    with open(hook_file, 'w', encoding='utf-8') as f:
        f.write(hook_content)
    print(f"✅ 创建运行时钩子文件: {hook_file}")
    return hook_file

def build_onedir():
    """执行文件夹模式打包"""
    
    # 先清理输出目录
    clean_output_directory()
    
    # 创建运行时钩子文件
    hook_file = create_runtime_hook()
    
    # 构建 PyInstaller 命令
    cmd = [
        "pyinstaller",
        "--onedir",           # 文件夹模式，不生成临时文件
        "--noconsole",        # 无控制台窗口
        "--uac-admin",        # 请求管理员权限
        "--name", "ok-script-app",
        "--add-data", "assets;assets",
        "--add-data", "i18n;i18n", 
        "--add-data", "ok_tasks;ok_tasks",
        "--runtime-hook", hook_file,  # 添加运行时钩子
        "--exclude-module", "tkinter",  # 排除 tkinter 模块
        "--exclude-module", "_tkinter",  # 排除 _tkinter 模块
        "--hidden-import", "ok_tasks.SortieMode",
        "--hidden-import", "ok_tasks.ChaosMode",
        "--hidden-import", "utils_sortie",
        "--hidden-import", "utils_chaos",
        "--hidden-import", "src.globals",
        "--hidden-import", "src.tasks.MyOneTimeTask",
        "--hidden-import", "onnxocr",
        "--hidden-import", "onnxocr_ppocrv5",
        "--collect-all", "onnxocr",
        "--collect-all", "openvino",
        "--collect-all", "pyappify",
        "main.py"
    ]
    
    print("开始文件夹模式打包...")
    print(f"命令: {' '.join(cmd)}")
    
    try:
        # 执行打包命令
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("✅ 打包成功！")
        print("\n输出目录: dist/ok-script-app/")
        print("可执行文件: dist/ok-script-app/ok-script-app.exe")
        
        # 清理运行时钩子文件
        if os.path.exists(hook_file):
            os.remove(hook_file)
            print(f"🧹 清理临时文件: {hook_file}")
        
        # 创建压缩文件
        print("\n📦 开始创建压缩文件...")
        if create_zip_archive():
            print("\n🎉 全流程完成！")
            print("✅ 打包 + 压缩 = 一键分发准备就绪")
        
        print("\n文件夹模式特点:")
        print("- 不会生成临时文件")
        print("- 所有文件都在 dist/ok-script-app/ 目录下")
        print("- 启动速度更快")
        print("- 便于调试和文件管理")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 打包失败: {e}")
        print(f"错误输出: {e.stderr}")
        # 清理运行时钩子文件
        if os.path.exists(hook_file):
            os.remove(hook_file)
        return False
    except FileNotFoundError:
        print("❌ 未找到 pyinstaller，请先安装: pip install pyinstaller")
        # 清理运行时钩子文件
        if os.path.exists(hook_file):
            os.remove(hook_file)
        return False
    
    return True

if __name__ == "__main__":
    if build_onedir():
        print("\n🚀 现在您可以：")
        print("1. 直接分发压缩文件给用户")
        print("2. 用户解压后运行 ok-script-app.exe")
        print("3. 零临时文件，快速启动！")
    else:
        sys.exit(1)