"""
AI Test Agent模块
基于LangChain封装，集成国产大模型(智谱GLM-4)
实现用例生成、PO代码生成、测试脚本生成、失败分析、智能维护等功能
"""
import os
import json
from typing import Dict, List, Any, Optional
from datetime import datetime

from config.ai_config import get_model_config, get_api_key, get_generation_config
from common.log_utils import get_logger

logger = get_logger(__name__)


class AITestAgent:
    """
    AI测试代理
    提供AI驱动的测试相关功能
    """
    
    def __init__(self):
        """初始化AI Agent"""
        self.model_config = get_model_config()
        self.generation_config = get_generation_config()
        self.api_key = get_api_key()
        self.provider = self.model_config.get('provider', 'zhipu')
        self.model_name = self.model_config.get('model_name', 'glm-4')
        self.temperature = self.model_config.get('temperature', 0.3)
        self.max_tokens = self.model_config.get('max_tokens', 4096)
        
        # 初始化LLM客户端
        self._init_llm()
    
    def _init_llm(self):
        """初始化大语言模型客户端"""
        try:
            if self.provider == 'zhipu':
                from langchain_community.chat_models import ChatZhipuAI
                self.llm = ChatZhipuAI(
                    api_key=self.api_key,
                    model=self.model_name,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens
                )
            elif self.provider == 'openai':
                from langchain_openai import ChatOpenAI
                self.llm = ChatOpenAI(
                    api_key=self.api_key,
                    model=self.model_name,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                    base_url=self.model_config.get('base_url')
                )
            else:
                raise ValueError(f"不支持的模型提供商: {self.provider}")
            
            logger.info(f"AI Agent初始化成功: {self.provider}/{self.model_name}")
        except Exception as e:
            logger.error(f"AI Agent初始化失败: {e}")
            self.llm = None
    
    def _call_llm(self, prompt: str, system_prompt: str = None) -> str:
        """
        调用大语言模型
        
        Args:
            prompt: 提示词
            system_prompt: 系统提示词
            
        Returns:
            模型响应
        """
        if self.llm is None:
            logger.error("LLM未初始化，无法调用")
            return ""
        
        try:
            from langchain.schema import HumanMessage, SystemMessage
            
            messages = []
            if system_prompt:
                messages.append(SystemMessage(content=system_prompt))
            messages.append(HumanMessage(content=prompt))
            
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            logger.error(f"LLM调用失败: {e}")
            return ""
    
    def generate_test_cases(self, page_description: str, 
                           module_name: str = None) -> List[Dict[str, Any]]:
        """
        AI智能生成测试用例
        
        Args:
            page_description: 页面描述
            module_name: 模块名称
            
        Returns:
            测试用例列表
        """
        logger.info(f"AI生成测试用例: {module_name or '未命名模块'}")
        
        system_prompt = """你是一位资深的UI测试专家，擅长编写高质量的测试用例。
请根据页面描述生成符合企业规范的UI测试用例，包括正常场景、异常场景和边界场景。"""
        
        prompt = f"""请根据以下页面描述生成测试用例：

页面描述：
{page_description}

要求：
1. 生成至少5个测试用例，覆盖正常场景、异常场景和边界场景
2. 每个用例包含：用例ID、用例名称、前置条件、测试步骤、预期结果
3. 用例ID格式：TC_{module_name or 'MODULE'}_001
4. 输出JSON格式，便于程序解析

请直接输出JSON格式的测试用例列表，不要包含其他说明文字。
"""
        
        response = self._call_llm(prompt, system_prompt)
        
        try:
            # 提取JSON内容
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                test_cases = json.loads(json_str)
                logger.info(f"成功生成 {len(test_cases)} 个测试用例")
                return test_cases
            else:
                logger.error("无法从响应中提取JSON")
                return []
        except json.JSONDecodeError as e:
            logger.error(f"JSON解析失败: {e}")
            return []
    
    def generate_po_code(self, page_url: str, 
                        page_description: str,
                        page_name: str = None) -> str:
        """
        AI自动生成PO代码
        
        Args:
            page_url: 页面URL
            page_description: 页面描述
            page_name: 页面名称
            
        Returns:
            PO类代码
        """
        logger.info(f"AI生成PO代码: {page_name or page_url}")
        
        system_prompt = """你是一位资深的Python自动化测试开发工程师，擅长使用Playwright和Page Object模式。
请生成符合企业代码规范的PO类代码，包含元素定位和页面行为方法。"""
        
        prompt = f"""请根据以下信息生成PO类代码：

页面URL：{page_url}
页面名称：{page_name or '未命名页面'}
页面描述：
{page_description}

要求：
1. 继承BasePage基类
2. 使用Playwright的locator方式进行元素定位
3. 优先使用ID、name、data-testid等稳定属性
4. 包含页面元素定位和页面行为方法
5. 添加适当的注释和文档字符串
6. 遵循PEP8代码规范
7. 类名格式：{page_name or 'PageName'}Page

BasePage基类已提供以下方法：
- click(locator): 点击元素
- input_text(locator, text): 输入文本
- get_text(locator): 获取文本
- wait_for_element(locator): 等待元素
- is_element_visible(locator): 判断元素是否可见

请直接输出完整的Python代码，不要包含其他说明文字。
"""
        
        code = self._call_llm(prompt, system_prompt)
        logger.info("PO代码生成完成")
        return code
    
    def generate_test_script(self, po_code: str, 
                            test_cases: List[Dict[str, Any]],
                            module_name: str = None) -> str:
        """
        AI自动生成测试脚本
        
        Args:
            po_code: PO类代码
            test_cases: 测试用例列表
            module_name: 模块名称
            
        Returns:
            测试脚本代码
        """
        logger.info(f"AI生成测试脚本: {module_name or '未命名模块'}")
        
        system_prompt = """你是一位资深的Python自动化测试开发工程师，擅长使用Pytest编写测试脚本。
请生成符合企业代码规范的Pytest测试脚本，包含Allure装饰器。"""
        
        test_cases_json = json.dumps(test_cases, ensure_ascii=False, indent=2)
        
        prompt = f"""请根据以下PO代码和测试用例生成Pytest测试脚本：

PO类代码：
```python
{po_code}
```

测试用例：
```json
{test_cases_json}
```

要求：
1. 使用Pytest框架
2. 添加Allure装饰器(@allure.feature, @allure.story, @allure.step)
3. 使用参数化实现多组数据测试
4. 包含前置条件和断言
5. 遵循PEP8代码规范
6. 文件名格式：test_{module_name or 'module'}.py

请直接输出完整的Python测试脚本代码，不要包含其他说明文字。
"""
        
        code = self._call_llm(prompt, system_prompt)
        logger.info("测试脚本生成完成")
        return code
    
    def analyze_failure(self, error_message: str, 
                       screenshot_path: str = None,
                       page_source: str = None,
                       test_step: str = None) -> Dict[str, Any]:
        """
        AI智能失败分析
        
        Args:
            error_message: 错误信息
            screenshot_path: 截图路径
            page_source: 页面源码
            test_step: 测试步骤
            
        Returns:
            分析结果
        """
        logger.info("AI分析测试失败原因")
        
        system_prompt = """你是一位资深的自动化测试专家，擅长分析测试失败原因。
请根据错误信息分析失败原因，并给出具体的修复建议。"""
        
        prompt = f"""请分析以下测试失败原因：

测试步骤：{test_step or '未知'}
错误信息：
{error_message}

页面源码片段：
{page_source[:2000] if page_source else '未提供'}

请分析：
1. 失败类型（定位器失效/页面结构变更/业务逻辑变更/环境问题/用例逻辑错误）
2. 失败原因
3. 修复建议
4. 是否需要更新PO代码

输出JSON格式：
{{
    "failure_type": "定位器失效",
    "reason": "...",
    "suggestion": "...",
    "need_update_po": true,
    "new_locator": "..."
}}
"""
        
        response = self._call_llm(prompt, system_prompt)
        
        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                result = json.loads(json_str)
                logger.info(f"失败分析完成: {result.get('failure_type')}")
                return result
            else:
                return {
                    "failure_type": "未知",
                    "reason": "无法解析AI响应",
                    "suggestion": "请人工分析",
                    "need_update_po": False
                }
        except json.JSONDecodeError:
            return {
                "failure_type": "未知",
                "reason": "JSON解析失败",
                "suggestion": "请人工分析",
                "need_update_po": False
            }
    
    def update_locator(self, old_locator: str, 
                      page_source: str,
                      element_description: str) -> str:
        """
        AI智能更新定位器
        
        Args:
            old_locator: 旧定位器
            page_source: 页面源码
            element_description: 元素描述
            
        Returns:
            新定位器
        """
        logger.info(f"AI更新定位器: {old_locator}")
        
        system_prompt = """你是一位资深的自动化测试专家，擅长编写稳定的元素定位器。
请根据页面源码和元素描述，生成新的、稳定的定位器。"""
        
        prompt = f"""请根据以下信息生成新的元素定位器：

旧定位器：{old_locator}
元素描述：{element_description}

页面源码片段：
```html
{page_source[:3000]}
```

要求：
1. 使用Playwright的locator语法
2. 优先选择稳定的属性（id, name, data-testid）
3. 避免使用动态生成的class或xpath
4. 如果可能，使用文本定位
5. 返回格式：locator_type=selector

请直接输出新的定位器，不要包含其他说明。
"""
        
        new_locator = self._call_llm(prompt, system_prompt)
        logger.info(f"定位器更新完成: {new_locator}")
        return new_locator.strip()
    
    def optimize_test_case(self, test_case_code: str, 
                          failure_history: List[str]) -> str:
        """
        AI优化测试用例
        
        Args:
            test_case_code: 测试用例代码
            failure_history: 失败历史记录
            
        Returns:
            优化后的代码
        """
        logger.info("AI优化测试用例")
        
        system_prompt = """你是一位资深的自动化测试专家，擅长优化不稳定的测试用例。
请根据失败历史给出优化建议，并生成优化后的代码。"""
        
        failure_history_text = "\n".join(failure_history) if failure_history else "无"
        
        prompt = f"""请优化以下测试用例：

当前测试用例代码：
```python
{test_case_code}
```

失败历史：
{failure_history_text}

请分析：
1. 不稳定原因
2. 优化建议
3. 优化后的代码

请直接输出优化后的Python代码，不要包含其他说明。
"""
        
        optimized_code = self._call_llm(prompt, system_prompt)
        logger.info("测试用例优化完成")
        return optimized_code


# 单例模式
_ai_agent_instance = None


def get_ai_agent() -> AITestAgent:
    """
    获取AI Agent实例(单例)
    
    Returns:
        AITestAgent实例
    """
    global _ai_agent_instance
    if _ai_agent_instance is None:
        _ai_agent_instance = AITestAgent()
    return _ai_agent_instance
