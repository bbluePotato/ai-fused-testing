"""
Pytest配置文件
定义夹具(Fixture)和钩子函数(Hook)
"""
import os
import pytest
import allure
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext

from config.env_config import get_env_config, get_env_url
from config.browser_config import get_launch_options, get_browser_type
from common.log_utils import get_logger, clean_old_logs
from pages.sc_website_page import SCWebsitePage

logger = get_logger(__name__)


# ==================== 会话级夹具 ====================

@pytest.fixture(scope="session", autouse=True)
def session_setup():
    """会话级设置，整个测试会话只执行一次"""
    logger.info("=" * 50)
    logger.info("测试会话开始")
    logger.info("=" * 50)
    
    # 清理过期日志
    clean_old_logs(days=7)
    
    yield
    
    logger.info("=" * 50)
    logger.info("测试会话结束")
    logger.info("=" * 50)


@pytest.fixture(scope="session")
def playwright():
    """Playwright实例"""
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright):
    """浏览器实例"""
    browser_type = get_browser_type()
    launch_options = get_launch_options()
    
    logger.info(f"启动浏览器: {browser_type}")
    
    if browser_type == "firefox":
        browser = playwright.firefox.launch(**launch_options)
    elif browser_type == "webkit":
        browser = playwright.webkit.launch(**launch_options)
    else:  # 默认chromium
        browser = playwright.chromium.launch(**launch_options)
    
    yield browser
    
    logger.info("关闭浏览器")
    browser.close()


# ==================== 函数级夹具 ====================

@pytest.fixture(scope="function")
def browser_context(browser):
    """浏览器上下文(每个测试函数一个)"""
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        record_video_dir=os.path.join(os.path.dirname(__file__), '..', 'reports', 'recordings') 
        if os.environ.get('RECORD_VIDEO') else None
    )
    
    # 设置默认超时时间（5 秒）
    context.set_default_timeout(5000)
    context.set_default_navigation_timeout(5000)
    
    yield context
    
    context.close()


@pytest.fixture(scope="function")
def page(browser_context):
    """页面实例"""
    page = browser_context.new_page()
    yield page
    page.close()


@pytest.fixture(scope="function")
def env_config():
    """环境配置"""
    return get_env_config()


@pytest.fixture(scope="function")
def site_url(env_config):
    """基础URL"""
    return env_config.get('base_url', '')


@pytest.fixture(scope="function")
def sc_home_page(page, site_url):
    """SC Technology 首页面对象"""
    return SCHomePage(page, site_url)


# ==================== 类级别夹具（同一个类共享一个浏览器页面）====================

@pytest.fixture(scope="class")
def class_browser_context(browser):
    """类级别的浏览器上下文，同一个测试类共享"""
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080}
    )
    context.set_default_timeout(5000)
    context.set_default_navigation_timeout(5000)
    
    logger.info("创建类级别浏览器上下文")
    yield context
    
    logger.info("关闭类级别浏览器上下文")
    context.close()


@pytest.fixture(scope="class")
def class_page(class_browser_context):
    """类级别的页面实例，同一个测试类共享"""
    page = class_browser_context.new_page()
    logger.info("创建类级别页面实例")
    yield page
    logger.info("关闭类级别页面实例")
    page.close()


@pytest.fixture(scope="class")
def class_sc_website_page(class_page):
    """类级别的 SC Technology 网站页面对象"""
    base_url = get_env_url()
    if not base_url:
        base_url = "https://bbluepotato.github.io/SCtechnology/"
    return SCWebsitePage(class_page, base_url)


# ==================== Pytest钩子函数 ====================

def pytest_configure(config):
    """Pytest配置"""
    # 注册自定义标记
    config.addinivalue_line("markers", "smoke: 冒烟测试")
    config.addinivalue_line("markers", "regression: 回归测试")
    config.addinivalue_line("markers", "login: 登录相关测试")
    config.addinivalue_line("markers", "home: 首页相关测试")
    config.addinivalue_line("markers", "ai: AI功能测试")


def pytest_collection_modifyitems(config, items):
    """修改测试项收集"""
    # 可以在这里对测试项进行排序或过滤
    pass


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    测试执行报告钩子
    用于在测试失败时自动截图
    支持 function 级别和 class 级别的 page fixture
    """
    outcome = yield
    report = outcome.get_result()

    # 如果测试失败，截图并保存
    if report.when == "call" and report.failed:
        page = None
        try:
            # 尝试获取 function 级别的 page
            page = item.funcargs.get('page')
            # 如果没有，尝试获取 class 级别的 page
            if page is None:
                class_page = item.funcargs.get('class_page')
                if class_page:
                    page = class_page

            if page:
                # 创建截图目录
                screenshot_dir = os.path.join(os.path.dirname(__file__), '..', 'reports', 'screenshots')
                os.makedirs(screenshot_dir, exist_ok=True)

                # 截图
                screenshot_path = os.path.join(screenshot_dir, f"failed_{item.name}_{call.when}.png")
                page.screenshot(path=screenshot_path, full_page=True)
                logger.info(f"失败截图已保存: {screenshot_path}")

                # 将截图附加到Allure报告
                with open(screenshot_path, 'rb') as f:
                    allure.attach(f.read(), name="失败截图", attachment_type=allure.attachment_type.PNG)

                # 保存页面源码
                source_path = os.path.join(screenshot_dir, f"failed_{item.name}_{call.when}.html")
                with open(source_path, 'w', encoding='utf-8') as f:
                    f.write(page.content())
                logger.info(f"页面源码已保存: {source_path}")

                # 将页面源码附加到Allure报告
                with open(source_path, 'r', encoding='utf-8') as f:
                    allure.attach(f.read(), name="页面源码", attachment_type=allure.attachment_type.HTML)
        except Exception as e:
            logger.error(f"保存失败截图时出错: {e}")


def pytest_addoption(parser):
    """添加命令行选项"""
    parser.addoption(
        "--env",
        action="store",
        default="test",
        help="测试环境: test/staging/production"
    )
    parser.addoption(
        "--record-video",
        action="store_true",
        default=False,
        help="是否录制视频"
    )
