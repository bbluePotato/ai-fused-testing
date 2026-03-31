# AI-Fused UI Automation Testing Framework

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-1.40+-green.svg)](https://playwright.dev/)
[![Pytest](https://img.shields.io/badge/Pytest-7.4+-red.svg)](https://docs.pytest.org/)
[![Allure](https://img.shields.io/badge/Allure-2.13+-orange.svg)](https://allurereport.org/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

**基于 Playwright + Pytest + Allure 的企业级 AI 融合 UI 自动化测试框架**

集成 LangChain 和智谱 GLM-4 大模型，实现 AI 驱动的测试用例生成、智能元素定位和自愈能力

[特性](#-核心特性) • [快速开始](#-快速开始) • [使用文档](#-使用文档) • [项目结构](#-项目结构) • [示例演示](#-示例演示)

</div>

---

## 📖 简介

这是一个现代化的 UI 自动化测试框架，专为解决传统自动化测试痛点而设计：

### 传统测试痛点 vs 我们的解决方案

| 传统测试痛点 | AI-Fused 框架解决方案 |
|------------|---------------------|
| ❌ 维护成本高，UI 变更导致大量脚本失效 | ✅ **AI 自愈能力**：自动分析页面变化，智能修复定位器 |
| ❌ 编写测试用例耗时耗力 | ✅ **AI 生成用例**：基于需求描述自动生成测试代码 |
| ❌ 失败原因难以分析 | ✅ **AI 智能分析**：自动分析失败根因并提供修复建议 |
| ❌ 报告不直观，问题难追溯 | ✅ **Allure 可视化报告**：精美报告 + 失败截图 + HTML 源码 |
| ❌ 执行速度慢 | ✅ **并行执行**：支持多进程并发，大幅提升执行效率 |

---

## ✨ 核心特性

### 🔧 基础能力

- **🎯 Playwright 驱动**
  - 支持 Chromium、Firefox、WebKit、Edge 多种浏览器
  - 自动等待机制，告别不稳定等待时间
  - 强大的选择器引擎，精准定位页面元素

- **🏗️ Page Object 设计模式**
  - 模块化页面对象设计，提高代码复用性
  - 清晰的层次结构：Base → Page → Test
  - 易于维护和扩展

- **🌍 多环境支持**
  - test / staging / production环境灵活切换
  - YAML 配置文件管理，安全便捷
  - 环境变量隔离，互不干扰

- **📊 丰富的报告体系**
  - **Allure 报告**：交互式可视化报告，包含趋势图、分类统计、历史追踪
  - **HTML 报告**：独立 HTML 文件，便于分享和存档
  - **失败截图**：自动捕获失败瞬间的页面截图和 HTML 源码

- **⚡ 高性能执行**
  - 支持多进程并行执行 (`-n auto`)
  - 失败自动重试机制 (`--reruns 2`)
  - 超时控制，防止卡死

### 🤖 AI 增强能力

> 集成 LangChain 和智谱 GLM-4 大模型，为测试注入智能

- **🪄 智能测试用例生成**
  ```python
  # 只需输入需求描述，AI 自动生成测试代码
  python run.py --ai-generate "用户登录功能测试"
  ```

- **🤖 智能 PO 代码生成**
  - 自动分析页面 HTML 结构
  - 生成规范的 Page Object 代码
  - 减少 80% 的重复编码工作

- **🔍 失败智能分析**
  - AI 分析失败日志和截图
  - 提供详细的根因分析
  - 给出可执行的修复建议

- **💊 定位器自愈**
  - 元素定位失败时自动寻找替代方案
  - 基于 AI 分析页面 DOM 变化
  - 大幅降低维护成本

- **🛠️ 脚本智能维护**
  - 批量更新因 UI 变更失效的脚本
  - 智能识别页面结构变化
  - 一键修复多个测试用例

---

## 🚀 快速开始

### 1️⃣ 环境准备

```bash
# 克隆项目
git clone https://github.com/YOUR_USERNAME/ui-ai-automation.git
cd ui-ai-automation

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 安装 Playwright 浏览器
playwright install
```

### 2️⃣ 配置（可选）

如需使用 AI 功能，配置 API 密钥：

```bash
# Windows:
set ZHIPU_API_KEY=your_api_key_here

# macOS/Linux:
export ZHIPU_API_KEY=your_api_key_here

# 或编辑 .env 文件
ZHIPU_API_KEY=your_api_key_here
```

### 3️⃣ 运行测试

```bash
# 运行所有测试（默认生成 Allure 报告并自动打开）
python run.py

# 运行特定测试
python run.py -k "test_01 or test_02"

# 运行冒烟测试
python run.py -m smoke

# 指定浏览器
python run.py --browser firefox

# 有头模式（显示浏览器窗口）
python run.py --headed

# 并行执行（4 个进程）
python run.py -n 4

# 清理旧报告后运行
python run.py --clean
```

### 4️⃣ 查看报告

测试完成后会自动：
1. 清理所有旧报告
2. 生成最新 Allure 报告
3. 在浏览器中自动打开

报告位置：`reports/allure-report/index.html`

---

## 📚 使用文档

### 命令行参数详解

| 参数 | 简写 | 说明 | 示例 |
|------|------|------|------|
| `--marker` | `-m` | 按标记运行测试 | `-m smoke` |
| `--keyword` | `-k` | 按关键字匹配测试名 | `-k login` |
| `--path` | `-p` | 指定测试文件或目录 | `-p tests/test_login.py` |
| `--env` | `-e` | 测试环境 | `-e staging` |
| `--browser` | `-b` | 浏览器类型 | `-b firefox` |
| `--headed` | | 有头模式运行 | `--headed` |
| `--workers` | `-n` | 并行工作进程数 | `-n 4` |
| `--report` | `-r` | 报告类型 | `-r allure html` |
| `--clean` | | 清理历史报告 | `--clean` |
| `--ai-generate` | | 使用 AI 生成测试用例 | `--ai-generate` |
| `--ai-analyze` | | 使用 AI 分析测试结果 | `--ai-analyze` |
| `--verbose` | `-v` | 详细输出级别 | `-vv` |

### 测试标记（Markers）

在测试用例中使用标记进行分类：

```python
@pytest.mark.smoke
def test_login():
    """冒烟测试"""
    pass

@pytest.mark.regression
def test_full_workflow():
    """回归测试"""
    pass
```

运行特定标记的测试：
```bash
# 运行冒烟测试
python run.py -m smoke

# 运行回归测试
python run.py -m regression
```

### 配置管理

#### 环境配置 (`config/env_config.yaml`)

```yaml
test:
  base_url: "https://test.example.com"
  timeout: 5000
  
staging:
  base_url: "https://staging.example.com"
  timeout: 10000
  
production:
  base_url: "https://example.com"
  timeout: 30000
```

#### 浏览器配置 (`config/browser_config.yaml`)

```yaml
default_browser: chromium
headless: true
viewport:
  width: 1920
  height: 1080
slow_mo: 0
```

---

## 🏗️ 项目结构

```
ui-ai-automation/
├── base/                       # 基础层
│   ├── __init__.py
│   └── base_page.py           # 页面对象基类（封装常用操作）
│
├── common/                     # 公共工具层
│   ├── __init__.py
│   ├── ai_agent.py            # AI Agent 模块（智能分析/生成）
│   ├── assert_utils.py        # 断言工具类
│   ├── file_utils.py          # 文件操作工具
│   └── log_utils.py           # 日志工具
│
├── config/                     # 配置管理
│   ├── env_config.yaml        # 环境配置
│   ├── browser_config.yaml    # 浏览器配置
│   ├── ai_config.yaml         # AI 配置
│   └── __init__.py
│
├── pages/                      # 页面对象层
│   ├── __init__.py
│   └── sc_website_page.py     # SC Technology 网站页面对象
│
├── tests/                      # 测试用例层
│   ├── __init__.py
│   ├── conftest.py            # Pytest 夹具配置
│   └── test_sc_website.py     # SC Technology 网站测试用例
│
├── reports/                    # 测试报告（自动生成）
│   ├── allure-results/        # Allure 原始结果
│   ├── allure-report/         # Allure 可视化报告
│   ├── html-reports/          # HTML 报告
│   └── screenshots/           # 失败截图
│
├── logs/                       # 日志文件
│   └── pytest.log
│
├── .env                        # 环境变量配置
├── .env.example                # 环境变量示例
├── pytest.ini                  # Pytest 配置
├── requirements.txt            # Python 依赖
└── run.py                      # 主运行入口
```

---

## 💡 示例演示

### 1. 编写测试用例

```python
import allure
import pytest
from pages.sc_website_page import SCWebsitePage

@allure.feature("用户登录")
@allure.story("正常登录流程")
class TestUserLogin:
    
    @allure.title("用例 1：使用有效凭据成功登录")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_success(self, website_page):
        """验证使用正确的用户名和密码能够成功登录"""
        
        with allure.step("打开登录页面"):
            website_page.open("/login")
        
        with allure.step("输入用户名和密码"):
            website_page.input_username("test_user")
            website_page.input_password("password123")
        
        with allure.step("点击登录按钮"):
            website_page.click_login_button()
        
        with allure.step("验证登录成功"):
            assert website_page.verify_welcome_message_visible(), \
                "欢迎消息未显示，登录可能失败"
```

### 2. 运行测试

```bash
# 运行登录相关测试
python run.py -k "login"

# 运行关键用例（带严重级别筛选）
python run.py -m critical
```

### 3. 查看 Allure 报告

运行完成后会自动打开精美的 Allure 报告，包含：

- 📈 **测试概览**：通过率、失败数、跳过数
- 🏷️ **功能分类**：按 Feature/Story 分组展示
- ⏱️ **执行趋势**：历史执行时间对比
- 🐛 **失败分析**：堆栈跟踪 + 截图 + HTML 源码
- 🔗 **链接追踪**：关联需求/Bug ID

---

## 🎯 最佳实践

### 1. 页面对象编写规范

```python
from base.base_page import BasePage
import allure

class LoginPage(BasePage):
    """登录页面对象"""
    
    # 元素定位器（使用常量定义）
    USERNAME_INPUT = "#username"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "button[type='submit']"
    
    @allure.step("输入用户名：{username}")
    def input_username(self, username: str):
        """输入用户名"""
        self.input_text(self.USERNAME_INPUT, username)
    
    @allure.step("输入密码")
    def input_password(self, password: str):
        """输入密码（不记录明文）"""
        self.input_text(self.PASSWORD_INPUT, password)
    
    @allure.step("点击登录按钮")
    def click_login_button(self):
        """点击登录"""
        self.click(self.LOGIN_BUTTON)
    
    @allure.step("验证欢迎消息可见")
    def verify_welcome_message_visible(self) -> bool:
        """验证登录成功"""
        return self.is_element_visible(".welcome-message")
```

### 2. 测试数据管理

使用 `Faker` 库生成测试数据：

```python
from faker import Faker

fake = Faker('zh_CN')

def test_register_with_random_data():
    """使用随机数据注册"""
    username = fake.user_name()
    email = fake.email()
    phone = fake.phone_number()
    
    # 执行注册逻辑...
```

### 3. 智能等待

避免使用固定等待时间，优先使用智能等待：

```python
# ❌ 不推荐
time.sleep(5)

# ✅ 推荐
self.wait_for_element_visible("#dynamic-content", timeout=5000)
```

---

## 🔧 故障排查

### 常见问题

#### 1. 测试执行超时

**现象**: `TimeoutError: Timeout 5000ms exceeded`

**解决方案**:
```bash
# 增加超时时间
python run.py --timeout 10000

# 或修改 pytest.ini
timeout = 10
```

#### 2. 元素定位失败

**现象**: `ElementNotFound: The element was not found`

**排查步骤**:
1. 检查失败截图中的 HTML 源码
2. 使用浏览器 DevTools 验证选择器
3. 考虑使用更稳定的定位方式（ID > CSS Selector > XPath）

#### 3. Allure 报告无法打开

**现象**: 运行完成后未自动打开报告

**解决方案**:
```bash
# 手动生成报告
allure generate reports/allure-results --clean -o reports/allure-report

# 手动打开报告
allure open reports/allure-report

# 检查 Allure 是否安装
allure --version

# 如未安装，执行：
npm install -g allure-commandline
```

---

## 📦 依赖说明

### 核心依赖

| 包名 | 版本 | 用途 |
|------|------|------|
| pytest | >=7.4.0 | 测试框架 |
| playwright | >=1.40.0 | 浏览器自动化 |
| pytest-playwright | >=0.4.0 | Playwright 集成 |
| allure-pytest | >=2.13.0 | Allure 报告集成 |
| pytest-html | >=4.1.0 | HTML 报告 |

### AI 相关依赖

| 包名 | 版本 | 用途 |
|------|------|------|
| langchain | >=0.1.0 | AI 应用框架 |
| langchain-community | >=0.0.10 | LangChain 社区组件 |
| zhipuai | >=2.0.0 | 智谱 AI SDK |
| openai | >=1.0.0 | OpenAI SDK（可选） |

### 工具库

| 包名 | 版本 | 用途 |
|------|------|------|
| pyyaml | >=6.0.1 | YAML 配置解析 |
| python-dotenv | >=1.0.0 | 环境变量管理 |
| pydantic | >=2.5.0 | 数据验证 |
| loguru | >=0.7.0 | 日志记录 |
| faker | >=20.0.0 | 测试数据生成 |

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 开发环境设置

```bash
# Fork 项目后克隆到本地
git clone https://github.com/******/ui-ai-automation.git
cd ui-ai-automation

# 创建开发分支
git checkout -b feature/your-feature-name

# 安装开发依赖
pip install -r requirements.txt
pip install pytest-cov black flake8 mypy  # 可选的代码质量工具
```

### 代码规范

- 遵循 PEP 8 编码规范
- 使用 Black 格式化代码
- 添加完整的类型注解
- 编写清晰的文档字符串

```bash
# 代码格式化
black .

# 代码检查
flake8 .

# 类型检查
mypy .
```

---

## 📄 许可证

本项目采用 Apache 2.0 许可证。详见 [LICENSE](LICENSE) 文件。

---

## 🙏 致谢

感谢以下开源项目：

- [Playwright](https://playwright.dev/) - 可靠的浏览器自动化库
- [Pytest](https://docs.pytest.org/) - 成熟的 Python 测试框架
- [Allure](https://allurereport.org/) - 灵活的测试报告框架
- [LangChain](https://www.langchain.com/) - 强大的 AI 应用开发框架
- [智谱 AI](https://open.bigmodel.cn/) - 国产优秀大模型服务

---

## 📬 联系方式

- **作者**: YSC
- **邮箱**: ******
- **项目地址**: https://github.com/******/ui-ai-automation
- **问题反馈**: https://github.com/******/ui-ai-automation/issues

---

<div align="center">

**如果这个项目对你有帮助，请给一个 ⭐️ Star！**

Made with ❤️ by YOUR_NAME

</div>
