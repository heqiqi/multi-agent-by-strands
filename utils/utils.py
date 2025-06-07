import os
import logging
from logging.handlers import RotatingFileHandler

from utils.constants import APP_NAME

def setup_logger(name, log_file, level=logging.INFO, max_size=10*1024*1024, backup_count=5):
    # 创建日志目录（如果不存在）
    log_dir = os.path.dirname(log_file)
    os.makedirs(log_dir, exist_ok=True)
    
    # 创建日志记录器
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # 避免重复添加处理器
    if not logger.handlers:
        # 创建文件处理器
        file_handler = RotatingFileHandler(
            log_file, maxBytes=max_size, backupCount=backup_count
        )
        file_handler.setLevel(level)
        
        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        
        # 定义日志格式
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # 添加处理器到日志记录器
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger

# 示例：创建应用程序全局日志记录器
app_logger = setup_logger('app', f'logs/{APP_NAME}.log')

# 示例：创建数据库操作专用日志记录器
tools_logger = setup_logger('database', 'logs/{APP_NAME}-tools.log')    