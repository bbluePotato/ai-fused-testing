"""
环境配置管理模块
"""
import os
import yaml
from typing import Dict, Any

# 配置文件路径
CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_CONFIG_FILE = os.path.join(CONFIG_DIR, 'env_config.yaml')

# 缓存配置
_config_cache = None


def load_yaml_config(file_path: str) -> Dict[str, Any]:
    """加载YAML配置文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def get_env_config(env: str = None) -> Dict[str, Any]:
    """
    获取环境配置
    
    Args:
        env: 环境名称(test/staging/production), 为None时使用默认环境
        
    Returns:
        环境配置字典
    """
    global _config_cache
    
    if _config_cache is None:
        _config_cache = load_yaml_config(ENV_CONFIG_FILE)
    
    # 如果没有指定环境，使用默认环境
    if env is None:
        env = _config_cache.get('default_env', 'test')
        # 也可以从环境变量读取
        env = os.environ.get('TEST_ENV', env)
    
    # 获取指定环境的配置
    env_config = _config_cache.get(env, {})
    if not env_config:
        raise ValueError(f"未找到环境配置: {env}")
    
    # 添加环境名称
    env_config['env_name'] = env
    
    return env_config


def decrypt_password(encrypted_password: str) -> str:
    """
    解密密码(示例实现，实际应使用更安全的加密方式)
    
    Args:
        encrypted_password: 加密后的密码
        
    Returns:
        解密后的密码
    """
    import base64
    try:
        return base64.b64decode(encrypted_password).decode('utf-8')
    except Exception:
        return encrypted_password


def get_env_url(env: str = None) -> str:
    """获取环境URL

    Args:
        env: 环境名称，为None时使用默认环境

    Returns:
        环境URL字符串，如果未配置则返回空字符串
    """
    try:
        config = get_env_config(env)
        return config.get('base_url', '')
    except ValueError:
        # 如果环境未配置，返回空字符串而不是抛出异常
        return ''


def get_env_credentials(env: str = None) -> Dict[str, str]:
    """获取环境登录凭证"""
    config = get_env_config(env)
    password = config.get('password_encrypted', '')
    return {
        'username': config.get('username', ''),
        'password': decrypt_password(password)
    }
