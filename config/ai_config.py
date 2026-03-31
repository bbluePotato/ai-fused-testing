"""
AI配置管理模块
"""
import os
import yaml
import re
from typing import Dict, Any

# 配置文件路径
CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
AI_CONFIG_FILE = os.path.join(CONFIG_DIR, 'ai_config.yaml')

# 缓存配置
_ai_config_cache = None


def load_yaml_config(file_path: str) -> Dict[str, Any]:
    """加载YAML配置文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def resolve_env_variables(config: Any) -> Any:
    """解析配置中的环境变量 ${VAR_NAME}"""
    if isinstance(config, dict):
        return {k: resolve_env_variables(v) for k, v in config.items()}
    elif isinstance(config, list):
        return [resolve_env_variables(item) for item in config]
    elif isinstance(config, str):
        # 匹配 ${VAR_NAME} 格式
        pattern = r'\$\{([^}]+)\}'
        def replace_env_var(match):
            var_name = match.group(1)
            return os.environ.get(var_name, match.group(0))
        return re.sub(pattern, replace_env_var, config)
    return config


def get_ai_config() -> Dict[str, Any]:
    """
    获取AI配置
    
    Returns:
        AI配置字典
    """
    global _ai_config_cache
    
    if _ai_config_cache is None:
        config = load_yaml_config(AI_CONFIG_FILE)
        _ai_config_cache = resolve_env_variables(config)
    
    return _ai_config_cache


def get_model_config() -> Dict[str, Any]:
    """获取模型配置"""
    config = get_ai_config()
    return config.get('model', {})


def get_model_provider() -> str:
    """获取模型提供商"""
    config = get_model_config()
    return config.get('provider', 'zhipu')


def get_model_name() -> str:
    """获取模型名称"""
    config = get_model_config()
    return config.get('model_name', 'glm-4')


def get_api_key() -> str:
    """获取API密钥"""
    config = get_model_config()
    api_key = config.get('api_key', '')
    # 如果配置中是环境变量格式但未被解析，直接从环境变量读取
    if api_key.startswith('${') and api_key.endswith('}'):
        var_name = api_key[2:-1]
        api_key = os.environ.get(var_name, '')
    return api_key


def get_features_config() -> Dict[str, bool]:
    """获取功能开关配置"""
    config = get_ai_config()
    return config.get('features', {})


def is_feature_enabled(feature_name: str) -> bool:
    """检查功能是否启用"""
    features = get_features_config()
    return features.get(feature_name, False)


def get_generation_config() -> Dict[str, Any]:
    """获取生成配置"""
    config = get_ai_config()
    return config.get('generation', {})
