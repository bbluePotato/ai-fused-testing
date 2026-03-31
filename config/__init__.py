"""
配置模块初始化
"""
from .env_config import get_env_config
from .browser_config import get_browser_config
from .ai_config import get_ai_config

__all__ = ['get_env_config', 'get_browser_config', 'get_ai_config']
