"""
浏览器配置管理模块
"""
import os
import yaml
from typing import Dict, Any, List

# 配置文件路径
CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
BROWSER_CONFIG_FILE = os.path.join(CONFIG_DIR, 'browser_config.yaml')

# 缓存配置
_browser_config_cache = None


def load_yaml_config(file_path: str) -> Dict[str, Any]:
    """加载YAML配置文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def get_browser_config(config_name: str = None) -> Dict[str, Any]:
    """
    获取浏览器配置
    
    Args:
        config_name: 配置名称(default/chromium/firefox/edge/ci), 为None时使用默认配置
        
    Returns:
        浏览器配置字典
    """
    global _browser_config_cache
    
    if _browser_config_cache is None:
        _browser_config_cache = load_yaml_config(BROWSER_CONFIG_FILE)
    
    # 如果没有指定配置，使用默认配置
    if config_name is None:
        config_name = 'default'
        # 也可以从环境变量读取
        config_name = os.environ.get('BROWSER_CONFIG', config_name)
    
    # 获取指定配置
    config = _browser_config_cache.get(config_name, {})
    if not config:
        raise ValueError(f"未找到浏览器配置: {config_name}")
    
    return config


def get_browser_type(config_name: str = None) -> str:
    """获取浏览器类型"""
    config = get_browser_config(config_name)
    return config.get('browser', 'chromium')


def is_headless(config_name: str = None) -> bool:
    """是否无头模式"""
    config = get_browser_config(config_name)
    return config.get('headless', False)


def get_viewport(config_name: str = None) -> Dict[str, int]:
    """获取视口大小"""
    config = get_browser_config(config_name)
    return config.get('viewport', {'width': 1920, 'height': 1080})


def get_browser_args(config_name: str = None) -> List[str]:
    """获取浏览器启动参数"""
    config = get_browser_config(config_name)
    return config.get('args', [])


def get_launch_options(config_name: str = None) -> Dict[str, Any]:
    """
    获取Playwright启动选项
    
    Returns:
        Playwright启动选项字典
    """
    config = get_browser_config(config_name)
    
    options = {
        'headless': config.get('headless', False),
        'slow_mo': config.get('slow_mo', 0),
    }
    
    # 添加args参数
    if 'args' in config:
        options['args'] = config['args']
    
    # 添加channel参数(用于Edge)
    if 'channel' in config:
        options['channel'] = config['channel']
    
    return options
