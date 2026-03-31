"""
AI 融合功能演示脚本
展示框架如何与大模型集成，实现智能化测试
"""
import json
from common.ai_agent import get_ai_agent
from common.log_utils import get_logger

logger = get_logger(__name__)


def demo_ai_generate_test_cases():
    """演示 1: AI 智能生成测试用例"""
    print("\n" + "="*80)
    print("演示 1: AI 智能生成测试用例")
    print("="*80)
    
    page_description = """
    这是一个用户注册页面，包含以下元素：
    1. 用户名输入框（必填，4-20 个字符）
    2. 邮箱输入框（必填，需要验证邮箱格式）
    3. 密码输入框（必填，6-16 位，包含字母和数字）
    4. 确认密码输入框（必填，必须与密码一致）
    5. 手机号码输入框（选填，11 位数字）
    6. 验证码按钮（点击后发送短信验证码）
    7. 同意协议复选框（必选）
    8. 注册按钮
    
    业务规则：
    - 用户名不能包含特殊字符
    - 邮箱必须是有效的 email 格式
    - 密码强度要求：包含字母和数字
    - 手机号可选，但如果填写必须是 11 位数字
    - 必须同意用户协议才能注册
    """
    
    agent = get_ai_agent()
    test_cases = agent.generate_test_cases(page_description, module_name="user_register")
    
    print(f"\n✅ AI 生成了 {len(test_cases)} 个测试用例:")
    print(json.dumps(test_cases[:3], indent=2, ensure_ascii=False))  # 只显示前 3 个
    return test_cases


def demo_ai_generate_po_code():
    """演示 2: AI 自动生成 PO 代码"""
    print("\n" + "="*80)
    print("演示 2: AI 自动生成 PO 代码")
    print("="*80)
    
    page_url = "https://example.com/login"
    page_name = "Login"
    page_description = """
    登录页面包含：
    1. 用户名输入框 - ID: username
    2. 密码输入框 - ID: password
    3. 记住我复选框 - ID: remember
    4. 登录按钮 - CSS: button.btn-login
    5. 忘记密码链接 - CSS: a.forgot-password
    6. 注册账号链接 - CSS: a.register-link
    
    页面行为：
    - 输入用户名和密码后点击登录
    - 登录成功跳转到首页
    - 登录失败显示错误提示
    """
    
    agent = get_ai_agent()
    po_code = agent.generate_po_code(page_url, page_description, page_name)
    
    print(f"\n✅ AI 生成的 PO 代码:")
    print(po_code[:1500])  # 只显示前 1500 字符
    return po_code


def demo_ai_failure_analysis():
    """演示 3: AI 智能失败分析"""
    print("\n" + "="*80)
    print("演示 3: AI 智能失败分析")
    print("="*80)
    
    error_message = """
    TimeoutError: Locator.click: Timeout 5000ms exceeded
    Call log:
      - waiting for locator('#loginButton')
      - locator resolved to 0 elements
      - trying to click after 5000ms timeout
    """
    
    page_source = """
    <html>
    <body>
        <div class="login-form">
            <input id="username" type="text" />
            <input id="password" type="password" />
            <button id="btn-login-submit" class="btn btn-primary">登录</button>
            <a href="/forgot" class="forgot-link">忘记密码？</a>
        </div>
    </body>
    </html>
    """
    
    test_step = "点击登录按钮"
    
    agent = get_ai_agent()
    analysis_result = agent.analyze_failure(
        error_message=error_message,
        page_source=page_source,
        test_step=test_step
    )
    
    print(f"\n✅ AI 失败分析结果:")
    print(json.dumps(analysis_result, indent=2, ensure_ascii=False))
    return analysis_result


def demo_ai_update_locator():
    """演示 4: AI 智能更新定位器"""
    print("\n" + "="*80)
    print("演示 4: AI 智能更新定位器")
    print("="*80)
    
    old_locator = "#loginButton"
    element_description = "登录按钮，位于表单底部"
    
    page_source = """
    <html>
    <body>
        <form class="login-form">
            <input id="username" name="username" type="text" placeholder="用户名" />
            <input id="password" name="password" type="password" placeholder="密码" />
            <div class="form-options">
                <label><input type="checkbox" id="remember" /> 记住我</label>
                <a href="/forgot-password" class="link-secondary">忘记密码？</a>
            </div>
            <button type="submit" id="btn-login-submit" class="btn btn-primary btn-lg">
                立即登录
            </button>
            <p class="help-text">还没有账号？<a href="/register" class="link-primary">立即注册</a></p>
        </form>
    </body>
    </html>
    """
    
    agent = get_ai_agent()
    new_locator = agent.update_locator(
        old_locator=old_locator,
        page_source=page_source,
        element_description=element_description
    )
    
    print(f"\n✅ AI 更新的定位器:")
    print(f"旧定位器：{old_locator}")
    print(f"新定位器：{new_locator}")
    return new_locator


def demo_ai_optimize_test():
    """演示 5: AI 优化测试用例"""
    print("\n" + "="*80)
    print("演示 5: AI 优化测试用例")
    print("="*80)
    
    test_case_code = """
def test_login_success(login_page):
    login_page.open("/login")
    login_page.input_username("testuser")
    login_page.input_password("password123")
    login_page.click_login_button()
    assert login_page.is_logged_in()
    """
    
    failure_history = [
        "TimeoutError: 点击登录按钮超时 - 可能是网络延迟",
        "AssertionError: is_logged_in 返回 False - 登录状态检测过早",
        "TimeoutError: 等待登录页面加载超时 - 页面加载慢"
    ]
    
    agent = get_ai_agent()
    optimized_code = agent.optimize_test_case(
        test_case_code=test_case_code,
        failure_history=failure_history
    )
    
    print(f"\n✅ AI 优化后的测试用例:")
    print(optimized_code[:1500])  # 只显示前 1500 字符
    return optimized_code


def main():
    """运行所有 AI 功能演示"""
    print("\n" + "="*80)
    print("🤖 AI-Fused UI Automation Framework - 功能演示")
    print("="*80)
    print("\n本框架集成了国产大模型（智谱 GLM-4），提供以下 AI 能力：")
    print("1. 📝 AI 智能生成测试用例")
    print("2. 💻 AI 自动生成 PO 代码")
    print("3. 🔍 AI 智能失败分析")
    print("4. 🎯 AI 智能更新定位器")
    print("5. ⚡ AI 优化测试用例")
    print("\n开始演示...\n")
    
    try:
        # 演示各项功能
        demo_ai_generate_test_cases()
        demo_ai_generate_po_code()
        demo_ai_failure_analysis()
        demo_ai_update_locator()
        demo_ai_optimize_test()
        
        print("\n" + "="*80)
        print("✅ 所有 AI 功能演示完成！")
        print("="*80)
        print("\n💡 提示：这些功能可以集成到您的测试工作流中，实现：")
        print("   - 减少手工编写测试用例的时间")
        print("   - 自动修复失败的测试")
        print("   - 智能维护测试脚本")
        print("   - 提高测试覆盖率和质量")
        
    except Exception as e:
        print(f"\n❌ 演示过程中出现错误：{e}")
        logger.error(f"AI 演示失败：{e}", exc_info=True)


if __name__ == "__main__":
    main()
