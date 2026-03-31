"""
断言工具类
封装常用的断言方法
"""
import allure
from typing import Any, Optional


class AssertUtils:
    """断言工具类"""
    
    @staticmethod
    def assert_equal(actual: Any, expected: Any, message: str = None):
        """
        断言相等
        
        Args:
            actual: 实际值
            expected: 期望值
            message: 断言失败消息
        """
        with allure.step(f"断言相等: 期望={expected}, 实际={actual}"):
            assert actual == expected, message or \
                f"断言失败: 期望 '{expected}', 实际 '{actual}'"
    
    @staticmethod
    def assert_not_equal(actual: Any, expected: Any, message: str = None):
        """
        断言不相等
        
        Args:
            actual: 实际值
            expected: 期望值
            message: 断言失败消息
        """
        with allure.step(f"断言不相等: 期望不等于{expected}, 实际={actual}"):
            assert actual != expected, message or \
                f"断言失败: 期望不等于 '{expected}', 实际 '{actual}'"
    
    @staticmethod
    def assert_true(condition: bool, message: str = None):
        """
        断言为真
        
        Args:
            condition: 条件
            message: 断言失败消息
        """
        with allure.step(f"断言为真: {condition}"):
            assert condition, message or f"断言失败: 期望为真，实际为假"
    
    @staticmethod
    def assert_false(condition: bool, message: str = None):
        """
        断言为假
        
        Args:
            condition: 条件
            message: 断言失败消息
        """
        with allure.step(f"断言为假: {condition}"):
            assert not condition, message or f"断言失败: 期望为假，实际为真"
    
    @staticmethod
    def assert_contains(container: Any, item: Any, message: str = None):
        """
        断言包含
        
        Args:
            container: 容器
            item: 元素
            message: 断言失败消息
        """
        with allure.step(f"断言包含: {item} 在 {container}"):
            assert item in container, message or \
                f"断言失败: '{item}' 不在 '{container}' 中"
    
    @staticmethod
    def assert_not_contains(container: Any, item: Any, message: str = None):
        """
        断言不包含
        
        Args:
            container: 容器
            item: 元素
            message: 断言失败消息
        """
        with allure.step(f"断言不包含: {item} 不在 {container}"):
            assert item not in container, message or \
                f"断言失败: '{item}' 在 '{container}' 中"
    
    @staticmethod
    def assert_is_none(value: Any, message: str = None):
        """
        断言为None
        
        Args:
            value: 值
            message: 断言失败消息
        """
        with allure.step(f"断言为None: {value}"):
            assert value is None, message or \
                f"断言失败: 期望为None，实际为 '{value}'"
    
    @staticmethod
    def assert_is_not_none(value: Any, message: str = None):
        """
        断言不为None
        
        Args:
            value: 值
            message: 断言失败消息
        """
        with allure.step(f"断言不为None: {value}"):
            assert value is not None, message or \
                f"断言失败: 期望不为None，实际为None"
    
    @staticmethod
    def assert_in_range(value: Any, min_val: Any, max_val: Any, message: str = None):
        """
        断言在范围内
        
        Args:
            value: 值
            min_val: 最小值
            max_val: 最大值
            message: 断言失败消息
        """
        with allure.step(f"断言在范围内: {min_val} <= {value} <= {max_val}"):
            assert min_val <= value <= max_val, message or \
                f"断言失败: '{value}' 不在范围 [{min_val}, {max_val}] 内"
    
    @staticmethod
    def assert_list_not_empty(lst: list, message: str = None):
        """
        断言列表不为空
        
        Args:
            lst: 列表
            message: 断言失败消息
        """
        with allure.step(f"断言列表不为空"):
            assert len(lst) > 0, message or \
                f"断言失败: 列表为空"
    
    @staticmethod
    def assert_dict_has_key(dct: dict, key: str, message: str = None):
        """
        断言字典包含指定键
        
        Args:
            dct: 字典
            key: 键
            message: 断言失败消息
        """
        with allure.step(f"断言字典包含键: {key}"):
            assert key in dct, message or \
                f"断言失败: 字典不包含键 '{key}'"
    
    @staticmethod
    def assert_string_starts_with(text: str, prefix: str, message: str = None):
        """
        断言字符串以指定前缀开头
        
        Args:
            text: 字符串
            prefix: 前缀
            message: 断言失败消息
        """
        with allure.step(f"断言字符串以 {prefix} 开头"):
            assert text.startswith(prefix), message or \
                f"断言失败: '{text}' 不以 '{prefix}' 开头"
    
    @staticmethod
    def assert_string_ends_with(text: str, suffix: str, message: str = None):
        """
        断言字符串以指定后缀结尾
        
        Args:
            text: 字符串
            suffix: 后缀
            message: 断言失败消息
        """
        with allure.step(f"断言字符串以 {suffix} 结尾"):
            assert text.endswith(suffix), message or \
                f"断言失败: '{text}' 不以 '{suffix}' 结尾"
