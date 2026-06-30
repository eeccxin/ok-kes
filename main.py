import ok
import sys
import os
from src.config import config

if __name__ == '__main__':
    # PyInstaller 打包模式适配
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
    config = config
    ok = ok.OK(config)
    ok.start()
