"""
BasePage基类 - 封装所有页面的公共操作
基于Playwright实现
"""
import os
import allure
from typing import Optional, List, Union
from playwright.sync_api import Page, Locator, expect

from common.log_utils import get_logger

logger = get_logger(__name__)


class BasePage:
    """
    页面基类
    所有Page类都应继承此类
    """
    
    def __init__(self, page: Page, base_url: str = None):
        """
        初始化
        
        Args:
            page: Playwright页面对象
            base_url: 基础URL
        """
        self.page = page
        self.base_url = base_url
        self.logger = logger
        
    def open(self, url: str = None):
        """
        打开页面

        Args:
            url: 页面URL，为None时使用base_url
        """
        if url is None:
            url = self.base_url

        if not url:
            raise ValueError("URL不能为空")

        # 处理相对路径（以 / 开头的路径）
        if url.startswith('/') and self.base_url:
            # 移除 base_url 末尾的斜杠，避免双斜杠
            base = self.base_url.rstrip('/')
            url = base + url
        # 确保URL格式正确
        elif not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        self.logger.info(f"打开页面: {url}")
        with allure.step(f"打开页面: {url}"):
            try:
                response = self.page.goto(url, wait_until='domcontentloaded', timeout=5000)
                if response:
                    self.logger.info(f"页面状态码: {response.status}")
                # 等待网络空闲，但忽略超时
                try:
                    self.page.wait_for_load_state('networkidle', timeout=5000)
                except:
                    pass
            except Exception as e:
                self.logger.error(f"打开页面失败: {e}")
                raise
    
    def wait_for_page_load(self, timeout: int = 5000):
        """
        等待页面加载完成
        
        Args:
            timeout: 超时时间(毫秒)
        """
        self.page.wait_for_load_state('networkidle', timeout=timeout)
        self.logger.debug("页面加载完成")
    
    def find_element(self, locator: Union[str, tuple, Locator],
                    selector: str = None) -> Locator:
        """
        查找元素

        Args:
            locator: 定位器字符串、元组(selector, type)或Locator对象
            selector: 选择器(当locator为字符串时使用)

        Returns:
            Locator对象
        """
        if isinstance(locator, Locator):
            return locator

        # 处理元组格式 (selector, type)
        if isinstance(locator, tuple) and len(locator) == 2:
            selector_value, selector_type = locator
            if selector_type == "css":
                return self.page.locator(f"css={selector_value}")
            elif selector_type == "xpath":
                return self.page.locator(f"xpath={selector_value}")
            elif selector_type == "text":
                return self.page.get_by_text(selector_value)
            else:
                return self.page.locator(selector_value)

        if selector:
            return self.page.locator(f"{locator}={selector}")

        # 支持多种定位方式
        if isinstance(locator, str):
            if locator.startswith('//'):
                return self.page.locator(f"xpath={locator}")
            elif locator.startswith('#'):
                return self.page.locator(f"id={locator[1:]}")
            elif locator.startswith('.'):
                return self.page.locator(f"css={locator}")
            else:
                return self.page.locator(locator)

        return self.page.locator(str(locator))
    
    def click(self, locator: Union[str, Locator], 
              selector: str = None, 
              timeout: int = 5000):
        """
        点击元素
        
        Args:
            locator: 定位器
            selector: 选择器
            timeout: 超时时间(毫秒)
        """
        element = self.find_element(locator, selector)
        self.logger.debug(f"点击元素: {locator}")
        with allure.step(f"点击元素: {locator}"):
            element.click(timeout=timeout)
    
    def input_text(self, locator: Union[str, Locator], 
                   text: str, 
                   selector: str = None,
                   clear_first: bool = True,
                   timeout: int = 5000):
        """
        输入文本
        
        Args:
            locator: 定位器
            text: 输入文本
            selector: 选择器
            clear_first: 是否先清空
            timeout: 超时时间(毫秒)
        """
        element = self.find_element(locator, selector)
        self.logger.debug(f"输入文本到元素: {locator}, 内容: {text}")
        with allure.step(f"输入文本: {text}"):
            if clear_first:
                element.clear(timeout=timeout)
            element.fill(text, timeout=timeout)
    
    def get_text(self, locator: Union[str, Locator], 
                 selector: str = None,
                 timeout: int = 5000) -> str:
        """
        获取元素文本
        
        Args:
            locator: 定位器
            selector: 选择器
            timeout: 超时时间(毫秒)
            
        Returns:
            元素文本
        """
        element = self.find_element(locator, selector)
        text = element.inner_text(timeout=timeout)
        self.logger.debug(f"获取元素文本: {locator}, 内容: {text}")
        return text
    
    def get_attribute(self, locator: Union[str, Locator], 
                      attribute: str,
                      selector: str = None,
                      timeout: int = 5000) -> str:
        """
        获取元素属性
        
        Args:
            locator: 定位器
            attribute: 属性名
            selector: 选择器
            timeout: 超时时间(毫秒)
            
        Returns:
            属性值
        """
        element = self.find_element(locator, selector)
        value = element.get_attribute(attribute, timeout=timeout)
        self.logger.debug(f"获取元素属性: {locator}, {attribute}={value}")
        return value
    
    def wait_for_element(self, locator: Union[str, Locator], 
                         selector: str = None,
                         state: str = 'visible',
                         timeout: int = 5000) -> Locator:
        """
        等待元素
        
        Args:
            locator: 定位器
            selector: 选择器
            state: 状态(visible/hidden/attached/detached)
            timeout: 超时时间(毫秒)
            
        Returns:
            Locator对象
        """
        element = self.find_element(locator, selector)
        self.logger.debug(f"等待元素: {locator}, 状态: {state}")
        element.wait_for(state=state, timeout=timeout)
        return element
    
    def is_element_visible(self, locator: Union[str, Locator], 
                           selector: str = None,
                           timeout: int = 5000) -> bool:
        """
        判断元素是否可见
        
        Args:
            locator: 定位器
            selector: 选择器
            timeout: 超时时间(毫秒)
            
        Returns:
            是否可见
        """
        try:
            element = self.find_element(locator, selector)
            return element.is_visible(timeout=timeout)
        except Exception:
            return False
    
    def is_element_exist(self, locator: Union[str, Locator], 
                         selector: str = None) -> bool:
        """
        判断元素是否存在
        
        Args:
            locator: 定位器
            selector: 选择器
            
        Returns:
            是否存在
        """
        try:
            element = self.find_element(locator, selector)
            return element.count() > 0
        except Exception:
            return False
    
    def select_dropdown(self, locator: Union[str, Locator], 
                        option: str,
                        selector: str = None,
                        by: str = 'value',
                        timeout: int = 5000):
        """
        选择下拉框选项
        
        Args:
            locator: 定位器
            option: 选项值
            selector: 选择器
            by: 选择方式(value/label/index)
            timeout: 超时时间(毫秒)
        """
        element = self.find_element(locator, selector)
        self.logger.debug(f"选择下拉框: {locator}, 选项: {option}")
        with allure.step(f"选择下拉框选项: {option}"):
            if by == 'label':
                element.select_option(label=option, timeout=timeout)
            elif by == 'index':
                element.select_option(index=int(option), timeout=timeout)
            else:
                element.select_option(value=option, timeout=timeout)
    
    def switch_to_frame(self, locator: Union[str, Locator], 
                        selector: str = None):
        """
        切换到iframe
        
        Args:
            locator: 定位器
            selector: 选择器
        """
        element = self.find_element(locator, selector)
        self.logger.debug(f"切换到iframe: {locator}")
        self.page = element.content_frame()
    
    def switch_to_default_content(self):
        """切换回主文档"""
        self.logger.debug("切换回主文档")
        # Playwright中需要重新获取page对象
        # 这里需要在子类中根据具体情况实现
    
    def refresh(self):
        """刷新页面"""
        self.logger.info("刷新页面")
        with allure.step("刷新页面"):
            self.page.reload()
            self.wait_for_page_load()
    
    def go_back(self):
        """返回上一页"""
        self.logger.info("返回上一页")
        with allure.step("返回上一页"):
            self.page.go_back()
            self.wait_for_page_load()
    
    def take_screenshot(self, name: str = None) -> str:
        """
        截图
        
        Args:
            name: 截图名称
            
        Returns:
            截图文件路径
        """
        from datetime import datetime
        import os
        
        if name is None:
            name = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        screenshot_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                      'reports', 'screenshots')
        os.makedirs(screenshot_dir, exist_ok=True)
        
        screenshot_path = os.path.join(screenshot_dir, f"{name}.png")
        self.page.screenshot(path=screenshot_path, full_page=True)
        self.logger.info(f"截图保存: {screenshot_path}")
        
        # 添加到Allure报告
        allure.attach.file(screenshot_path, name=name, 
                          attachment_type=allure.attachment_type.PNG)
        
        return screenshot_path
    
    def get_page_title(self) -> str:
        """
        获取页面标题
        
        Returns:
            页面标题
        """
        return self.page.title()
    
    def get_page_url(self) -> str:
        """
        获取当前URL

        Returns:
            当前URL
        """
        return self.page.url

    def wait_for_timeout(self, timeout: int):
        """
        等待指定时间（毫秒）

        Args:
            timeout: 等待时间（毫秒）
        """
        self.page.wait_for_timeout(timeout)

    def scroll_to_element(self, locator: Union[str, tuple, Locator]):
        """
        滚动到指定元素

        Args:
            locator: 元素定位器
        """
        element = self.find_element(locator)
        element.scroll_into_view_if_needed()

    # ==================== 断言方法 ====================
    
    def assert_element_exist(self, locator: Union[str, Locator], 
                            selector: str = None,
                            message: str = None):
        """
        断言元素存在
        
        Args:
            locator: 定位器
            selector: 选择器
            message: 断言失败消息
        """
        with allure.step(f"断言元素存在: {locator}"):
            element = self.find_element(locator, selector)
            expect(element).to_be_visible(timeout=5000)
    
    def assert_text_contains(self, locator: Union[str, Locator], 
                            expected_text: str,
                            selector: str = None,
                            message: str = None):
        """
        断言元素文本包含指定内容
        
        Args:
            locator: 定位器
            expected_text: 期望文本
            selector: 选择器
            message: 断言失败消息
        """
        with allure.step(f"断言元素文本包含: {expected_text}"):
            element = self.find_element(locator, selector)
            actual_text = element.inner_text()
            assert expected_text in actual_text, message or \
                f"期望文本 '{expected_text}' 不在实际文本 '{actual_text}' 中"
    
    def assert_title_contains(self, expected_title: str, message: str = None):
        """
        断言页面标题包含指定内容
        
        Args:
            expected_title: 期望标题
            message: 断言失败消息
        """
        with allure.step(f"断言页面标题包含: {expected_title}"):
            actual_title = self.page.title()
            assert expected_title in actual_title, message or \
                f"期望标题 '{expected_title}' 不在实际标题 '{actual_title}' 中"
    
    def assert_url_contains(self, expected_url: str, message: str = None):
        """
        断言当前URL包含指定内容
        
        Args:
            expected_url: 期望URL
            message: 断言失败消息
        """
        with allure.step(f"断言URL包含: {expected_url}"):
            actual_url = self.page.url
            assert expected_url in actual_url, message or \
                f"期望URL '{expected_url}' 不在实际URL '{actual_url}' 中"
