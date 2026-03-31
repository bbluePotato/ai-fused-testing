#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI融合UI自动化测试框架 - 运行入口
支持命令行参数、环境选择、测试类型筛选等功能
"""

import os
import sys
import argparse
import subprocess
import json
from pathlib import Path
from datetime import datetime

# 添加项目根目录到Python路径
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

import pytest
from common.log_utils import get_logger

logger = get_logger(__name__)


class TestRunner:
    """测试运行器"""
    
    def __init__(self):
        self.project_root = PROJECT_ROOT
        self.test_dir = self.project_root / "tests"
        self.report_dir = self.project_root / "reports"
        self.allure_dir = self.report_dir / "allure-results"
        self.html_report_dir = self.report_dir / "html-reports"
        
    def parse_args(self):
        """解析命令行参数"""
        parser = argparse.ArgumentParser(
            description="AI融合UI自动化测试框架运行器",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
使用示例:
  python run.py                          # 运行所有测试
  python run.py -m smoke                 # 运行冒烟测试
  python run.py -e staging               # 在staging环境运行
  python run.py --ai-generate            # 使用AI生成测试用例
  python run.py --browser firefox        # 使用Firefox浏览器
  python run.py -k login                 # 运行包含login的测试
  python run.py --headed                 # 有头模式运行
  python run.py --report allure          # 生成Allure报告
            """
        )
        
        # 测试选择
        parser.add_argument(
            "-m", "--marker",
            help="按标记运行测试 (smoke, regression, ai_generated等)"
        )
        parser.add_argument(
            "-k", "--keyword",
            help="按关键字匹配测试名称"
        )
        parser.add_argument(
            "--path", "-p",
            help="指定测试文件或目录路径"
        )
        
        # 环境配置
        parser.add_argument(
            "-e", "--env",
            default="test",
            choices=["test", "staging", "production"],
            help="测试环境 (默认: test)"
        )
        
        # 浏览器配置
        parser.add_argument(
            "--browser", "-b",
            default="chromium",
            choices=["chromium", "firefox", "webkit", "edge"],
            help="浏览器类型 (默认: chromium)"
        )
        parser.add_argument(
            "--headed",
            action="store_true",
            help="有头模式运行 (默认无头)"
        )
        parser.add_argument(
            "--slow-mo",
            type=int,
            default=0,
            help="慢动作延迟(毫秒)"
        )
        
        # 报告配置
        parser.add_argument(
            "--report", "-r",
            nargs="+",
            choices=["html", "allure", "json", "xml"],
            default=["allure"],
            help="报告类型 (默认: allure)"
        )
        parser.add_argument(
            "--open-report",
            action="store_true",
            help="测试完成后自动打开报告"
        )
        
        # AI功能
        parser.add_argument(
            "--ai-generate",
            action="store_true",
            help="使用AI生成测试用例"
        )
        parser.add_argument(
            "--ai-analyze",
            action="store_true",
            help="使用AI分析测试结果"
        )
        parser.add_argument(
            "--ai-fix",
            action="store_true",
            help="使用AI自动修复失败的定位器"
        )
        
        # 其他选项
        parser.add_argument(
            "--workers", "-n",
            type=int,
            default=1,
            help="并行工作进程数 (默认: 1)"
        )
        parser.add_argument(
            "--reruns",
            type=int,
            default=0,
            help="失败重试次数 (默认: 0)"
        )
        parser.add_argument(
            "--timeout",
            type=int,
            default=30000,
            help="默认超时时间(毫秒) (默认: 30000)"
        )
        parser.add_argument(
            "--verbose", "-v",
            action="count",
            default=0,
            help="详细输出级别 (-v, -vv)"
        )
        parser.add_argument(
            "--collect-only",
            action="store_true",
            help="仅收集测试用例，不执行"
        )
        parser.add_argument(
            "--clean",
            action="store_true",
            help="清理历史报告和缓存"
        )
        
        return parser.parse_args()
    
    def setup_environment(self, args):
        """设置环境变量"""
        # 设置测试环境
        os.environ["TEST_ENV"] = args.env
        os.environ["BROWSER_TYPE"] = args.browser
        os.environ["HEADED"] = str(args.headed).lower()
        os.environ["SLOW_MO"] = str(args.slow_mo)
        os.environ["DEFAULT_TIMEOUT"] = str(args.timeout)
        
        # AI功能开关
        if args.ai_generate:
            os.environ["AI_TEST_GENERATION"] = "true"
        if args.ai_analyze:
            os.environ["AI_FAILURE_ANALYSIS"] = "true"
        if args.ai_fix:
            os.environ["AI_SELF_HEALING"] = "true"
        
        logger.info(f"测试环境: {args.env}")
        logger.info(f"浏览器: {args.browser}")
        logger.info(f"有头模式: {args.headed}")
    
    def clean_reports(self, keep_logs: bool = True):
        """清理历史报告，只保留最新报告
        
        Args:
            keep_logs: 是否保留日志文件（默认True，保留7天内的日志）
        """
        import shutil
        
        logger.info("清理历史报告...")
        
        # 清理Allure结果
        if self.allure_dir.exists():
            shutil.rmtree(self.allure_dir)
            self.allure_dir.mkdir(parents=True, exist_ok=True)
            logger.info("  - 已清理 Allure 结果目录")
        
        # 清理Allure报告
        allure_report_dir = self.report_dir / "allure-report"
        if allure_report_dir.exists():
            shutil.rmtree(allure_report_dir)
            logger.info("  - 已清理 Allure 报告目录")
        
        # 清理HTML报告
        html_report_dir = self.report_dir / "html-reports"
        if html_report_dir.exists():
            shutil.rmtree(html_report_dir)
            logger.info("  - 已清理 HTML 报告目录")
        
        # 清理截图
        screenshots_dir = self.report_dir / "screenshots"
        if screenshots_dir.exists():
            shutil.rmtree(screenshots_dir)
            logger.info("  - 已清理截图目录")
        
        # 清理JSON报告
        json_report_dir = self.report_dir / "json-reports"
        if json_report_dir.exists():
            shutil.rmtree(json_report_dir)
            logger.info("  - 已清理 JSON 报告目录")
        
        # 清理XML报告
        xml_report_dir = self.report_dir / "xml-reports"
        if xml_report_dir.exists():
            shutil.rmtree(xml_report_dir)
            logger.info("  - 已清理 XML 报告目录")
        
        # 清理旧日志（可选，默认保留7天内的）
        if not keep_logs:
            logs_dir = self.report_dir / "logs"
            if logs_dir.exists():
                shutil.rmtree(logs_dir)
                logger.info("  - 已清理日志目录")
        else:
            logs_dir = self.report_dir / "logs"
            if logs_dir.exists():
                for log_file in logs_dir.glob("*.log"):
                    if log_file.stat().st_mtime < (datetime.now().timestamp() - 7 * 24 * 3600):
                        log_file.unlink()
                logger.info("  - 已清理7天前的日志文件")
        
        logger.info("清理完成，只保留最新报告")
    
    def build_pytest_args(self, args) -> list:
        """构建pytest参数"""
        pytest_args = ["-v"]
        
        # 详细级别
        if args.verbose == 1:
            pytest_args.append("-v")
        elif args.verbose >= 2:
            pytest_args.extend(["-vv", "--tb=long"])
        
        # 测试路径
        if args.path:
            pytest_args.append(args.path)
        else:
            pytest_args.append(str(self.test_dir))
        
        # 标记筛选
        if args.marker:
            pytest_args.extend(["-m", args.marker])
        
        # 关键字筛选
        if args.keyword:
            pytest_args.extend(["-k", args.keyword])
        
        # 并行执行
        if args.workers > 1:
            pytest_args.extend(["-n", str(args.workers), "--dist=loadfile"])
        
        # 失败重试
        if args.reruns > 0:
            pytest_args.extend(["--reruns", str(args.reruns), "--reruns-delay", "1"])
        
        # 报告生成
        if "html" in args.report:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            html_report = self.html_report_dir / f"report_{timestamp}.html"
            self.html_report_dir.mkdir(parents=True, exist_ok=True)
            pytest_args.extend([f"--html={html_report}", "--self-contained-html"])
            logger.info(f"HTML报告将生成: {html_report}")
        
        if "allure" in args.report:
            self.allure_dir.mkdir(parents=True, exist_ok=True)
            pytest_args.extend(["--alluredir", str(self.allure_dir)])
            logger.info(f"Allure结果将保存: {self.allure_dir}")
        
        if "json" in args.report:
            json_report = self.report_dir / "report.json"
            pytest_args.extend([f"--json-report", f"--json-report-file={json_report}"])
        
        if "xml" in args.report:
            junit_report = self.report_dir / "junit.xml"
            pytest_args.extend([f"--junitxml={junit_report}"])
        
        # 仅收集测试
        if args.collect_only:
            pytest_args.append("--collect-only")
        
        return pytest_args
    
    def run_tests(self, args) -> int:
        """运行测试"""
        self.setup_environment(args)
        
        # 每次运行测试前自动清理旧报告，只保留最新报告
        # 使用 --clean 参数可以连日志一起清理
        self.clean_reports(keep_logs=not args.clean)
        
        pytest_args = self.build_pytest_args(args)
        
        logger.info("=" * 60)
        logger.info("开始执行测试")
        logger.info(f"pytest {' '.join(pytest_args)}")
        logger.info("=" * 60)
        
        # 使用 subprocess 运行 pytest，避免 pytest-timeout 的线程问题
        import sys
        pytest_cmd = [sys.executable, "-m", "pytest"] + pytest_args
        
        try:
            # 设置超时时间为 300 秒（5分钟）
            result = subprocess.run(
                pytest_cmd,
                timeout=300,
                capture_output=False,
                text=True
            )
            exit_code = result.returncode
        except subprocess.TimeoutExpired:
            logger.error("测试执行超时（300秒）")
            exit_code = 1
        except Exception as e:
            logger.error(f"测试执行出错: {e}")
            exit_code = 1
        
        logger.info("=" * 60)
        logger.info(f"测试执行完成，退出码: {exit_code}")
        logger.info("=" * 60)
        
        return exit_code
    
    def generate_allure_report(self, args):
        """生成并打开Allure报告"""
        if "allure" not in args.report:
            return
        
        allure_report_dir = self.report_dir / "allure-report"
        
        # 检查是否有测试结果文件
        result_files = list(self.allure_dir.glob("*.json"))
        if not result_files:
            logger.warning("未找到Allure测试结果文件，跳过报告生成")
            return
        
        try:
            # 生成报告
            logger.info("生成Allure报告...")
            subprocess.run(
                f'allure generate "{self.allure_dir}" -o "{allure_report_dir}" --clean',
                shell=True,
                check=True
            )
            logger.info(f"Allure报告已生成: {allure_report_dir}")
            
            # 打开报告
            logger.info("正在打开 Allure 报告...")
            subprocess.Popen(
                f'allure open "{allure_report_dir}"',
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            logger.info("Allure 报告已在浏览器中打开")
        
        except FileNotFoundError:
            logger.warning("未找到Allure命令行工具，请安装: npm install -g allure-commandline")
        except subprocess.CalledProcessError as e:
            logger.error(f"生成Allure报告失败: {e}")
    
    def ai_analyze_results(self, args):
        """使用AI分析测试结果"""
        if not args.ai_analyze:
            return
        
        try:
            from common.ai_agent import AITestAgent
            
            agent = AITestAgent()
            
            # 读取测试结果
            results_file = self.report_dir / "report.json"
            if results_file.exists():
                with open(results_file, "r", encoding="utf-8") as f:
                    results = json.load(f)
                
                analysis = agent.analyze_failure(results)
                logger.info("AI测试结果分析:")
                logger.info(analysis)
        
        except Exception as e:
            logger.error(f"AI分析失败: {e}")
    
    def run(self):
        """主运行方法"""
        args = self.parse_args()
        
        # 创建必要的目录
        self.report_dir.mkdir(parents=True, exist_ok=True)
        
        exit_code = 0
        try:
            # 运行测试
            exit_code = self.run_tests(args)
        except Exception as e:
            logger.error(f"测试执行过程中发生错误: {e}")
            exit_code = 1
        finally:
            # 无论测试结果如何，都生成Allure报告
            self.generate_allure_report(args)
            
            # AI分析
            self.ai_analyze_results(args)
        
        return exit_code


def quick_run(marker: str = None, browser: str = "chromium", headed: bool = False):
    """
    快速运行测试的便捷函数
    
    Args:
        marker: 测试标记 (smoke, regression等)
        browser: 浏览器类型
        headed: 是否使用有头模式
    
    示例:
        from run import quick_run
        quick_run(marker="smoke", browser="firefox", headed=True)
    """
    runner = TestRunner()
    
    class Args:
        marker = marker
        keyword = None
        path = None
        env = "test"
        browser = browser
        headed = headed
        slow_mo = 0
        report = ["html"]
        open_report = False
        ai_generate = False
        ai_analyze = False
        ai_fix = False
        workers = 1
        reruns = 0
        timeout = 30000
        verbose = 1
        collect_only = False
        clean = False
    
    return runner.run_tests(Args())


if __name__ == "__main__":
    runner = TestRunner()
    sys.exit(runner.run())
