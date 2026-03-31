"""
日志工具模块
支持分级日志、日志滚动、控制台和文件双输出
"""
import os
import sys
import logging
import logging.handlers
from datetime import datetime
from typing import Optional

# 日志格式
LOG_FORMAT = '[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] [%(funcName)s] %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# 日志级别映射
LOG_LEVELS = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}

# 默认日志目录
DEFAULT_LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')

# 日志实例缓存
_loggers = {}


def init_logger(
    name: str = None,
    log_dir: str = None,
    log_level: str = 'INFO',
    console_level: str = 'INFO',
    file_level: str = 'DEBUG',
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 7
) -> logging.Logger:
    """
    初始化日志记录器
    
    Args:
        name: 日志名称
        log_dir: 日志目录
        log_level: 日志级别
        console_level: 控制台日志级别
        file_level: 文件日志级别
        max_bytes: 单个日志文件最大字节数
        backup_count: 备份文件数量
        
    Returns:
        日志记录器
    """
    if name is None:
        name = 'ui_automation'
    
    # 如果已经存在，直接返回
    if name in _loggers:
        return _loggers[name]
    
    # 创建日志记录器
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVELS.get(log_level.upper(), logging.INFO))
    
    # 清除已有的处理器
    logger.handlers.clear()
    
    # 设置日志目录
    if log_dir is None:
        log_dir = DEFAULT_LOG_DIR
    os.makedirs(log_dir, exist_ok=True)
    
    # 创建格式化器
    formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(LOG_LEVELS.get(console_level.upper(), logging.INFO))
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 文件处理器(按天滚动)
    log_file = os.path.join(log_dir, f'log_{datetime.now().strftime("%Y%m%d")}.log')
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding='utf-8'
    )
    file_handler.setLevel(LOG_LEVELS.get(file_level.upper(), logging.DEBUG))
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # 缓存日志记录器
    _loggers[name] = logger
    
    return logger


def get_logger(name: str = None) -> logging.Logger:
    """
    获取日志记录器
    
    Args:
        name: 日志名称
        
    Returns:
        日志记录器
    """
    if name in _loggers:
        return _loggers[name]
    
    return init_logger(name)


def clean_old_logs(log_dir: str = None, days: int = 7):
    """
    清理过期日志文件
    
    Args:
        log_dir: 日志目录
        days: 保留天数
    """
    import time
    
    if log_dir is None:
        log_dir = DEFAULT_LOG_DIR
    
    if not os.path.exists(log_dir):
        return
    
    now = time.time()
    cutoff = now - (days * 86400)  # 天数转换为秒
    
    for filename in os.listdir(log_dir):
        file_path = os.path.join(log_dir, filename)
        if os.path.isfile(file_path):
            # 检查文件修改时间
            if os.path.getmtime(file_path) < cutoff:
                try:
                    os.remove(file_path)
                    print(f"删除过期日志: {file_path}")
                except Exception as e:
                    print(f"删除日志失败 {file_path}: {e}")


class LoggerMixin:
    """
    日志混入类
    为类提供日志功能
    """
    
    @property
    def logger(self) -> logging.Logger:
        """获取日志记录器"""
        if not hasattr(self, '_logger'):
            self._logger = get_logger(self.__class__.__name__)
        return self._logger
