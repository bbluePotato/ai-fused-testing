"""
SC Technology 网站页面对象
包含首页、产品页、测试平台等所有页面元素和操作方法
"""
import allure
from playwright.sync_api import Page
from base.base_page import BasePage
from common.log_utils import get_logger

logger = get_logger(__name__)


class SCWebsitePage(BasePage):
    """SC Technology 网站页面对象"""

    # ==================== 导航栏元素 ====================
    NAV_HOME = ".navbar a[href='index.html']"  # 首页导航（导航栏内）
    NAV_PRODUCTS = ".navbar a[href='products.html']"  # 产品导航（导航栏内）
    NAV_CONTACT = ".navbar a[href='contact.html']"  # 联系我们导航（导航栏内）
    NAV_TEST_PLATFORM = ".navbar a[href='test-platform.html']"  # 测试平台导航（导航栏内）
    
    # ==================== 主题切换 ====================
    THEME_TOGGLE = "#theme-toggle"  # 主题切换按钮
    
    # ==================== 测试平台页面菜单元素 (使用 data-tab 属性) ====================
    API_TEST_MENU = ".sidebar-menu li.menu-item[data-tab='api-test']"  # 接口测试菜单
    CASE_MANAGEMENT_MENU = ".sidebar-menu li.menu-item[data-tab='case-manage']"  # 用例管理菜单
    TEST_REPORT_MENU = ".sidebar-menu li.menu-item[data-tab='report']"  # 测试报告菜单
    ENV_MANAGEMENT_MENU = ".sidebar-menu li.menu-item[data-tab='env-manage']"  # 环境管理菜单
    VAR_MANAGEMENT_MENU = ".sidebar-menu li.menu-item[data-tab='variables']"  # 变量管理菜单
    DATA_DRIVEN_MENU = ".sidebar-menu li.menu-item[data-tab='data-driven']"  # 数据驱动菜单
    MOCK_SERVICE_MENU = ".sidebar-menu li.menu-item[data-tab='mock']"  # Mock 服务菜单
    SCHEDULED_TASK_MENU = ".sidebar-menu li.menu-item[data-tab='scheduler']"  # 定时任务菜单

    # ==================== 接口测试页面元素 ====================
    METHOD_SELECT = "select#requestMethod"  # 请求方法选择
    URL_INPUT = "input#requestUrl"  # URL 输入框
    SEND_BUTTON = "button#sendRequest"  # 发送请求按钮
    RESPONSE_STATUS = "#responseMeta"  # 响应状态
    SAVE_CASE_BUTTON = "button#saveAsCase"  # 保存为测试用例按钮
    CASE_NAME_INPUT = "input#caseName"  # 用例名称输入框
    CONFIRM_BUTTON = "button#confirmCaseModal"  # 确定按钮（保存用例弹窗）

    # ==================== 页面内容区域 ====================
    PAGE_CONTENT = "main.content"  # 主内容区
    PRODUCTS_SECTION = "#products"  # 产品区域
    CONTACT_SECTION = "#contact"  # 联系区域
    TEST_PLATFORM_CONTENT = "#api-test, #case-management, #test-report"  # 测试平台内容

    def __init__(self, page: Page, base_url: str = None):
        """初始化"""
        super().__init__(page, base_url)
        self.logger = logger

    @allure.step("打开首页")
    def open_home_page(self):
        """打开网站首页"""
        self.open("/index.html")
        self.wait_for_timeout(1000)

    @allure.step("点击【产品】导航")
    def click_products_nav(self):
        """点击产品导航"""
        self.click(self.NAV_PRODUCTS)
        self.wait_for_timeout(1500)

    @allure.step("点击【联系我们】导航")
    def click_contact_nav(self):
        """点击联系我们导航"""
        self.click(self.NAV_CONTACT)
        self.wait_for_timeout(1500)

    @allure.step("点击【测试平台】导航")
    def click_test_platform_nav(self):
        """点击测试平台导航"""
        self.click(self.NAV_TEST_PLATFORM)
        self.wait_for_timeout(2000)

    @allure.step("点击【接口测试】菜单")
    def click_api_test_menu(self):
        """点击接口测试菜单"""
        self.click(self.API_TEST_MENU)
        self.wait_for_timeout(1000)

    @allure.step("点击【用例管理】菜单")
    def click_case_management_menu(self):
        """点击用例管理菜单"""
        self.click(self.CASE_MANAGEMENT_MENU)
        self.wait_for_timeout(1000)

    @allure.step("点击【测试报告】菜单")
    def click_test_report_menu(self):
        """点击测试报告菜单"""
        self.click(self.TEST_REPORT_MENU)
        self.wait_for_timeout(1000)

    @allure.step("点击【环境管理】菜单")
    def click_env_management_menu(self):
        """点击环境管理菜单"""
        self.click(self.ENV_MANAGEMENT_MENU)
        self.wait_for_timeout(1000)

    @allure.step("点击【变量管理】菜单")
    def click_var_management_menu(self):
        """点击变量管理菜单"""
        self.click(self.VAR_MANAGEMENT_MENU)
        self.wait_for_timeout(1000)

    @allure.step("点击【数据驱动】菜单")
    def click_data_driven_menu(self):
        """点击数据驱动菜单"""
        self.click(self.DATA_DRIVEN_MENU)
        self.wait_for_timeout(1000)

    @allure.step("点击【Mock 服务】菜单")
    def click_mock_service_menu(self):
        """点击 Mock 服务菜单"""
        self.click(self.MOCK_SERVICE_MENU)
        self.wait_for_timeout(1000)

    @allure.step("点击【定时任务】菜单")
    def click_scheduled_task_menu(self):
        """点击定时任务菜单"""
        self.click(self.SCHEDULED_TASK_MENU)
        self.wait_for_timeout(1000)

    @allure.step("点击主题切换按钮")
    def click_theme_toggle(self):
        """点击主题切换按钮"""
        self.click(self.THEME_TOGGLE)
        self.wait_for_timeout(1000)

    @allure.step("选择请求方法：{method}")
    def select_method(self, method: str):
        """选择请求方法"""
        self.select_dropdown(self.METHOD_SELECT, method, by='value')
        self.wait_for_timeout(500)

    @allure.step("输入 URL: {url}")
    def input_url(self, url: str):
        """输入 URL"""
        self.input_text(self.URL_INPUT, url)
        self.wait_for_timeout(500)

    @allure.step("点击发送请求按钮")
    def click_send_button(self):
        """点击发送请求按钮"""
        self.click(self.SEND_BUTTON)
        self.wait_for_timeout(2000)

    @allure.step("点击保存为测试用例按钮")
    def click_save_case_button(self):
        """点击保存为测试用例按钮"""
        self.click(self.SAVE_CASE_BUTTON)
        self.wait_for_timeout(500)

    @allure.step("输入用例名称：{case_name}")
    def input_case_name(self, case_name: str):
        """输入用例名称"""
        self.input_text(self.CASE_NAME_INPUT, case_name)
        self.wait_for_timeout(500)

    @allure.step("点击确定按钮")
    def click_confirm_button(self):
        """点击确定按钮"""
        self.click(self.CONFIRM_BUTTON)
        self.wait_for_timeout(1000)

    # ==================== 验证方法 ====================

    @allure.step("验证页面标题包含：{expected_title}")
    def verify_page_title_contains(self, expected_title: str) -> bool:
        """验证页面标题包含指定文本"""
        title = self.get_page_title()
        return expected_title in title

    @allure.step("验证当前 URL 包含：{expected_url}")
    def verify_url_contains(self, expected_url: str) -> bool:
        """验证当前 URL 包含指定文本"""
        url = self.get_page_url()
        return expected_url in url

    @allure.step("验证产品页面加载成功")
    def verify_products_page_loaded(self) -> bool:
        """验证产品页面加载成功"""
        return self.verify_url_contains("products.html")

    @allure.step("验证联系页面加载成功")
    def verify_contact_page_loaded(self) -> bool:
        """验证联系页面加载成功"""
        return self.verify_url_contains("contact.html")

    @allure.step("验证测试平台内容可见")
    def verify_test_platform_content_visible(self) -> bool:
        """验证测试平台内容可见"""
        return self.is_element_visible(self.TEST_PLATFORM_CONTENT)

    @allure.step("验证接口测试页面可见")
    def verify_api_test_page_visible(self) -> bool:
        """验证接口测试页面可见"""
        # 检查接口测试 tab 是否激活
        api_test_tab = self.page.locator("#api-test.tab-content.active")
        return api_test_tab.count() > 0 and api_test_tab.is_visible()

    @allure.step("验证用例管理页面可见")
    def verify_case_management_page_visible(self) -> bool:
        """验证用例管理页面可见"""
        case_tab = self.page.locator("#case-manage.tab-content.active")
        return case_tab.count() > 0 and case_tab.is_visible()

    @allure.step("验证测试报告页面可见")
    def verify_test_report_page_visible(self) -> bool:
        """验证测试报告页面可见"""
        report_tab = self.page.locator("#report.tab-content.active")
        return report_tab.count() > 0 and report_tab.is_visible()

    @allure.step("验证环境管理页面可见")
    def verify_env_management_page_visible(self) -> bool:
        """验证环境管理页面可见"""
        env_tab = self.page.locator("#env-manage.tab-content.active")
        return env_tab.count() > 0 and env_tab.is_visible()

    @allure.step("验证变量管理页面可见")
    def verify_var_management_page_visible(self) -> bool:
        """验证变量管理页面可见"""
        var_tab = self.page.locator("#variables.tab-content.active")
        return var_tab.count() > 0 and var_tab.is_visible()

    @allure.step("验证数据驱动页面可见")
    def verify_data_driven_page_visible(self) -> bool:
        """验证数据驱动页面可见"""
        data_tab = self.page.locator("#data-driven.tab-content.active")
        return data_tab.count() > 0 and data_tab.is_visible()

    @allure.step("验证 Mock 服务页面可见")
    def verify_mock_service_page_visible(self) -> bool:
        """验证 Mock 服务页面可见"""
        mock_tab = self.page.locator("#mock.tab-content.active")
        return mock_tab.count() > 0 and mock_tab.is_visible()

    @allure.step("验证定时任务页面可见")
    def verify_scheduled_task_page_visible(self) -> bool:
        """验证定时任务页面可见"""
        task_tab = self.page.locator("#scheduler.tab-content.active")
        return task_tab.count() > 0 and task_tab.is_visible()

    @allure.step("验证响应状态为：{expected_status}")
    def verify_response_status(self, expected_status: str) -> bool:
        """验证响应状态"""
        status_text = self.get_text(self.RESPONSE_STATUS)
        return expected_status in status_text

    @allure.step("验证页面为深色模式")
    def verify_dark_mode(self) -> bool:
        """验证页面为深色模式"""
        try:
            body_class = self.page.locator("body").get_attribute("class")
            html_class = self.page.locator("html").get_attribute("class")
            return "dark" in (body_class or "") or "dark" in (html_class or "")
        except:
            return False

    @allure.step("验证页面为浅色模式")
    def verify_light_mode(self) -> bool:
        """验证页面为浅色模式"""
        try:
            body_class = self.page.locator("body").get_attribute("class")
            html_class = self.page.locator("html").get_attribute("class")
            return "dark" not in (body_class or "") and "dark" not in (html_class or "")
        except:
            return True

    @allure.step("验证用例存在于默认分组：{case_name}")
    def verify_case_exists_in_default_group(self, case_name: str) -> bool:
        """验证用例存在于默认分组中"""
        # 在用例列表区域查找用例名称
        case_locator = self.page.locator("#caseList .case-name", has_text=case_name)
        return case_locator.count() > 0 and case_locator.is_visible()
