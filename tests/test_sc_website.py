"""
SC Technology 网站测试用例
包含 15 个测试用例，使用类级别 fixture 共享浏览器会话
"""
import pytest
import allure
import uuid
from pages.sc_website_page import SCWebsitePage


@pytest.fixture(scope="class")
def website_page(class_page):
    """创建网站页面对象"""
    return SCWebsitePage(class_page, "https://bbluepotato.github.io/SCtechnology/")


@allure.feature("SC Technology 网站功能测试")
@allure.story("网站核心功能验证")
class TestSCWebsite:
    """SC Technology 网站测试类 - 所有用例共享一个浏览器会话"""

    # ========== 用例 1：首页加载 ==========
    @allure.title("用例 1：正常加载网页首页")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("验证网站首页能够正常加载")
    def test_01_home_page_load(self, class_page, website_page):
        """用例 1：能够正常加载网页首页"""
        with allure.step("步骤 1：打开首页"):
            website_page.open_home_page()

        with allure.step("步骤 2：验证页面加载成功"):
            assert website_page.verify_page_title_contains("SC_Technology"), \
                "页面标题不包含预期文本"
            assert website_page.verify_url_contains("SCtechnology"), \
                "当前 URL 不正确"

    # ========== 用例 2：产品页面 ==========
    @allure.title("用例 2：点击【产品】，产品页面加载正常")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("验证点击产品导航后，产品页面能够正常加载")
    def test_02_products_page(self, class_page, website_page):
        """用例 2：点击【产品】，产品页面加载正常"""
        with allure.step("步骤 1：确保在首页"):
            if not website_page.verify_url_contains("index.html"):
                website_page.open_home_page()

        with allure.step("步骤 2：点击【产品】导航"):
            website_page.click_products_nav()

        with allure.step("步骤 3：验证产品页面加载成功"):
            assert website_page.verify_products_page_loaded(), \
                "产品页面未正确加载"

    # ========== 用例 3：联系我们页面 ==========
    @allure.title("用例 3：点击【联系我们】，联系我们页面加载正常")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("验证点击联系我们导航后，联系我们页面能够正常加载")
    def test_03_contact_page(self, class_page, website_page):
        """用例 3：点击【联系我们】，联系我们页面加载正常"""
        with allure.step("步骤 1：确保在首页"):
            if not website_page.verify_url_contains("index.html"):
                website_page.open_home_page()

        with allure.step("步骤 2：点击【联系我们】导航"):
            website_page.click_contact_nav()

        with allure.step("步骤 3：验证联系页面加载成功"):
            assert website_page.verify_contact_page_loaded(), \
                "联系我们页面未正确加载"

    # ========== 用例 4：测试平台页面 ==========
    @allure.title("用例 4：点击【测试平台】，测试平台页面加载正常")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("验证点击测试平台导航后，测试平台页面能够正常加载")
    def test_04_test_platform_page(self, class_page, website_page):
        """用例 4：点击【测试平台】，测试平台页面加载正常"""
        with allure.step("步骤 1：点击【测试平台】导航"):
            website_page.click_test_platform_nav()

        with allure.step("步骤 2：验证测试平台页面加载成功"):
            assert website_page.verify_url_contains("test-platform"), \
                "未跳转到测试平台页面"

    # ========== 用例 5：接口测试页面 ==========
    @allure.title("用例 5：在测试平台页面，点击【接口测试】，接口测试页面加载正常")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("验证在测试平台页面点击接口测试菜单后，接口测试页面能够正常加载")
    def test_05_api_test_page(self, class_page, website_page):
        """用例 5：在测试平台页面，点击【接口测试】，接口测试页面加载正常"""
        with allure.step("步骤 1：导航到测试平台页面"):
            website_page.open("/test-platform.html")
            website_page.wait_for_timeout(2000)

        with allure.step("步骤 2：点击【接口测试】菜单"):
            website_page.click_api_test_menu()

        with allure.step("步骤 3：验证接口测试页面加载成功"):
            assert website_page.verify_api_test_page_visible(), \
                "接口测试页面未显示"

    # ========== 用例 6：用例管理页面 ==========
    @allure.title("用例 6：在测试平台页面，点击【用例管理】，用例管理页面加载正常")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("验证在测试平台页面点击用例管理菜单后，用例管理页面能够正常加载")
    def test_06_case_management_page(self, class_page, website_page):
        """用例 6：在测试平台页面，点击【用例管理】，用例管理页面加载正常"""
        with allure.step("步骤 1：导航到测试平台页面"):
            website_page.open("/test-platform.html")
            website_page.wait_for_timeout(2000)

        with allure.step("步骤 2：点击【用例管理】菜单"):
            website_page.click_case_management_menu()

        with allure.step("步骤 3：验证用例管理页面加载成功"):
            assert website_page.verify_case_management_page_visible(), \
                "用例管理页面未显示"

    # ========== 用例 7：测试报告页面 ==========
    @allure.title("用例 7：在测试平台页面，点击【测试报告】，测试报告页面加载正常")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("验证在测试平台页面点击测试报告菜单后，测试报告页面能够正常加载")
    def test_07_test_report_page(self, class_page, website_page):
        """用例 7：在测试平台页面，点击【测试报告】，测试报告页面加载正常"""
        with allure.step("步骤 1：导航到测试平台页面"):
            website_page.open("/test-platform.html")
            website_page.wait_for_timeout(2000)

        with allure.step("步骤 2：点击【测试报告】菜单"):
            website_page.click_test_report_menu()

        with allure.step("步骤 3：验证测试报告页面加载成功"):
            assert website_page.verify_test_report_page_visible(), \
                "测试报告页面未显示"

    # ========== 用例 8：环境管理页面 ==========
    @allure.title("用例 8：在测试平台页面，点击【环境管理】，环境管理页面加载正常")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("验证在测试平台页面点击环境管理菜单后，环境管理页面能够正常加载")
    def test_08_env_management_page(self, class_page, website_page):
        """用例 8：在测试平台页面，点击【环境管理】，环境管理页面加载正常"""
        with allure.step("步骤 1：导航到测试平台页面"):
            website_page.open("/test-platform.html")
            website_page.wait_for_timeout(2000)

        with allure.step("步骤 2：点击【环境管理】菜单"):
            website_page.click_env_management_menu()

        with allure.step("步骤 3：验证环境管理页面加载成功"):
            assert website_page.verify_env_management_page_visible(), \
                "环境管理页面未显示"

    # ========== 用例 9：变量管理页面 ==========
    @allure.title("用例 9：在测试平台页面，点击【变量管理】，变量管理页面加载正常")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("验证在测试平台页面点击变量管理菜单后，变量管理页面能够正常加载")
    def test_09_var_management_page(self, class_page, website_page):
        """用例 9：在测试平台页面，点击【变量管理】，变量管理页面加载正常"""
        with allure.step("步骤 1：导航到测试平台页面"):
            website_page.open("/test-platform.html")
            website_page.wait_for_timeout(2000)

        with allure.step("步骤 2：点击【变量管理】菜单"):
            website_page.click_var_management_menu()

        with allure.step("步骤 3：验证变量管理页面加载成功"):
            assert website_page.verify_var_management_page_visible(), \
                "变量管理页面未显示"

    # ========== 用例 10：数据驱动页面 ==========
    @allure.title("用例 10：在测试平台页面，点击【数据驱动】，数据驱动页面加载正常")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("验证在测试平台页面点击数据驱动菜单后，数据驱动页面能够正常加载")
    def test_10_data_driven_page(self, class_page, website_page):
        """用例 10：在测试平台页面，点击【数据驱动】，数据驱动页面加载正常"""
        with allure.step("步骤 1：导航到测试平台页面"):
            website_page.open("/test-platform.html")
            website_page.wait_for_timeout(2000)

        with allure.step("步骤 2：点击【数据驱动】菜单"):
            website_page.click_data_driven_menu()

        with allure.step("步骤 3：验证数据驱动页面加载成功"):
            assert website_page.is_element_visible("#data-driven"), \
                "数据驱动页面未显示"

    # ========== 用例 11：Mock 服务页面 ==========
    @allure.title("用例 11：在测试平台页面，点击【Mock 服务】，Mock 服务页面加载正常")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("验证在测试平台页面点击 Mock 服务菜单后，Mock 服务页面能够正常加载")
    def test_11_mock_service_page(self, class_page, website_page):
        """用例 11：在测试平台页面，点击【Mock 服务】，Mock 服务页面加载正常"""
        with allure.step("步骤 1：导航到测试平台页面"):
            website_page.open("/test-platform.html")
            website_page.wait_for_timeout(2000)

        with allure.step("步骤 2：点击【Mock 服务】菜单"):
            website_page.click_mock_service_menu()

        with allure.step("步骤 3：验证 Mock 服务页面加载成功"):
            assert website_page.verify_mock_service_page_visible(), \
                "Mock 服务页面未显示"

    # ========== 用例 12：定时任务页面 ==========
    @allure.title("用例 12：在测试平台页面，点击【定时任务】，定时任务页面加载正常")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("验证在测试平台页面点击定时任务菜单后，定时任务页面能够正常加载")
    def test_12_scheduled_task_page(self, class_page, website_page):
        """用例 12：在测试平台页面，点击【定时任务】，定时任务页面加载正常"""
        with allure.step("步骤 1：导航到测试平台页面"):
            website_page.open("/test-platform.html")
            website_page.wait_for_timeout(2000)

        with allure.step("步骤 2：点击【定时任务】菜单"):
            website_page.click_scheduled_task_menu()

        with allure.step("步骤 3：验证定时任务页面加载成功"):
            assert website_page.verify_scheduled_task_page_visible(), \
                "定时任务页面未显示"

    # ========== 用例 13：接口测试完整流程 ==========
    @allure.title("用例 13：接口测试 - 创建用例完整流程")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("验证接口测试完整流程：选择 GET 请求，输入 URL，发送请求，保存用例，在用例管理中查看")
    def test_13_api_test_full_workflow(self, class_page, website_page):
        """用例 15：接口测试完整流程"""
        # 生成随机用例名称
        random_case_name = f"测试用例_{uuid.uuid4().hex[:8]}"
        allure.attach(random_case_name, "生成的随机用例名称")

        with allure.step("步骤 1：进入测试平台 - 接口测试页面"):
            website_page.open("/test-platform.html")
            website_page.wait_for_timeout(2000)
            website_page.click_api_test_menu()
            assert website_page.verify_api_test_page_visible(), \
                "接口测试页面未显示"

        with allure.step("步骤 2：选择 GET 请求方法"):
            website_page.select_method("GET")

        with allure.step("步骤 3：输入测试 URL"):
            test_url = "https://bbluepotato.github.io/SCtechnology/test-platform.html"
            website_page.input_url(test_url)

        with allure.step("步骤 4：点击发送请求按钮"):
            website_page.click_send_button()

        with allure.step("步骤 5：验证响应状态为 200"):
            website_page.wait_for_timeout(1000)
            response_visible = website_page.is_element_visible(
                website_page.RESPONSE_STATUS
            )
            assert response_visible, "响应结果未显示"

        with allure.step("步骤 6：点击保存为测试用例"):
            website_page.click_save_case_button()

        with allure.step("步骤 7：输入用例名称"):
            website_page.input_case_name(random_case_name)

        with allure.step("步骤 8：点击确定按钮"):
            website_page.click_confirm_button()

        with allure.step("步骤 9：进入用例管理页面查看"):
            website_page.click_case_management_menu()
            website_page.wait_for_timeout(1000)

        with allure.step("步骤 10：验证用例存在于默认分组"):
            case_exists = website_page.verify_case_exists_in_default_group(
                random_case_name
            )
            assert case_exists, f"用例 '{random_case_name}' 未在用例管理中找到"
