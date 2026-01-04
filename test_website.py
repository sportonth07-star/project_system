"""
网站测试脚本 - 实验室项目管理系统
测试主要功能：注册、登录、项目创建、编辑等
"""
import requests
import json
from bs4 import BeautifulSoup
import time

# 配置
BASE_URL = "http://localhost:5000"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

class WebsiteTester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.csrf_token = None
        self.test_results = []
        
    def log_test(self, test_name, success, message=""):
        """记录测试结果"""
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"\n{status} - {test_name}")
        if message:
            print(f"  → {message}")
        self.test_results.append({
            'test': test_name,
            'success': success,
            'message': message
        })
    
    def extract_csrf_token(self, html):
        """从HTML中提取CSRF令牌"""
        soup = BeautifulSoup(html, 'html.parser')
        csrf_input = soup.find('input', {'name': 'csrf_token'})
        if csrf_input:
            return csrf_input.get('value')
        return None
    
    def test_homepage(self):
        """测试主页"""
        try:
            response = self.session.get(f"{self.base_url}/", timeout=5)
            success = response.status_code in [200, 302]  # 可能重定向到登录
            self.log_test(
                "主页可访问性",
                success,
                f"HTTP {response.status_code}"
            )
            return success
        except Exception as e:
            self.log_test("主页可访问性", False, str(e))
            return False
    
    def test_login_page(self):
        """测试登录页面"""
        try:
            response = self.session.get(f"{self.base_url}/login", timeout=5)
            success = response.status_code == 200
            
            if success:
                self.csrf_token = self.extract_csrf_token(response.text)
                success = self.csrf_token is not None
            
            self.log_test(
                "登录页面加载",
                success,
                f"HTTP {response.status_code}, CSRF token: {'Found' if self.csrf_token else 'Missing'}"
            )
            return success
        except Exception as e:
            self.log_test("登录页面加载", False, str(e))
            return False
    
    def test_login_invalid_credentials(self):
        """测试无效登录凭证"""
        try:
            response = self.session.get(f"{self.base_url}/login", timeout=5)
            csrf_token = self.extract_csrf_token(response.text)
            
            login_data = {
                'username': 'invalid_user',
                'password': 'wrong_password',
                'csrf_token': csrf_token
            }
            
            response = self.session.post(
                f"{self.base_url}/login",
                data=login_data,
                timeout=5,
                allow_redirects=True
            )
            
            success = response.status_code == 200
            self.log_test(
                "无效登录处理",
                success,
                f"HTTP {response.status_code} - 返回登录页面"
            )
            return success
        except Exception as e:
            self.log_test("无效登录处理", False, str(e))
            return False
    
    def test_register_page(self):
        """测试注册页面"""
        try:
            response = self.session.get(f"{self.base_url}/register", timeout=5)
            success = response.status_code == 200
            
            if success:
                csrf_token = self.extract_csrf_token(response.text)
                success = csrf_token is not None
            
            self.log_test(
                "注册页面加载",
                success,
                f"HTTP {response.status_code}"
            )
            return success
        except Exception as e:
            self.log_test("注册页面加载", False, str(e))
            return False
    
    def test_dashboard_access(self):
        """测试未认证访问仪表板"""
        try:
            response = self.session.get(
                f"{self.base_url}/dashboard",
                timeout=5,
                allow_redirects=False
            )
            
            # 应该重定向到登录页面
            success = response.status_code in [302, 303]
            self.log_test(
                "未认证仪表板保护",
                success,
                f"HTTP {response.status_code} - 正确地重定向到登录"
            )
            return success
        except Exception as e:
            self.log_test("未认证仪表板保护", False, str(e))
            return False
    
    def test_projects_api(self):
        """测试项目API"""
        try:
            response = self.session.get(
                f"{self.base_url}/api/projects",
                timeout=5,
                allow_redirects=False
            )
            
            # API可能需要认证或返回404
            success = response.status_code in [200, 401, 403, 404]
            self.log_test(
                "项目API响应",
                success,
                f"HTTP {response.status_code}"
            )
            return success
        except Exception as e:
            self.log_test("项目API响应", False, str(e))
            return False
    
    def test_security_headers(self):
        """测试安全标头"""
        try:
            response = self.session.get(f"{self.base_url}/", timeout=5)
            headers = response.headers
            
            security_checks = {
                'X-Content-Type-Options': headers.get('X-Content-Type-Options') == 'nosniff',
                'X-Frame-Options': headers.get('X-Frame-Options') == 'DENY',
                'X-XSS-Protection': 'X-XSS-Protection' in headers,
            }
            
            all_pass = all(security_checks.values())
            
            details = ", ".join([f"{k}: {'✓' if v else '✗'}" for k, v in security_checks.items()])
            self.log_test(
                "安全标头检查",
                all_pass,
                details
            )
            return all_pass
        except Exception as e:
            self.log_test("安全标头检查", False, str(e))
            return False
    
    def test_static_files(self):
        """测试静态文件访问"""
        try:
            static_files = [
                '/static/css/main.css',
                '/static/js/dashboard.js',
                '/static/js/projects.js',
            ]
            
            results = {}
            for file_path in static_files:
                response = self.session.get(
                    f"{self.base_url}{file_path}",
                    timeout=5,
                    allow_redirects=False
                )
                results[file_path] = response.status_code == 200
            
            all_accessible = all(results.values())
            details = ", ".join([f"{k.split('/')[-1]}: {'✓' if v else '✗'}" for k, v in results.items()])
            
            self.log_test(
                "静态文件加载",
                all_accessible,
                details
            )
            return all_accessible
        except Exception as e:
            self.log_test("静态文件加载", False, str(e))
            return False
    
    def test_database_connection(self):
        """测试数据库连接"""
        try:
            # 尝试访问需要数据库的端点
            response = self.session.get(f"{self.base_url}/api/projects", timeout=5)
            
            # 如果没有连接错误，说明数据库连接正常
            # 500错误可能表示其他问题，不是连接问题
            success = response.status_code != 500 or "database" not in response.text.lower()
            
            self.log_test(
                "数据库连接",
                success,
                f"HTTP {response.status_code}"
            )
            return success
        except requests.exceptions.ConnectionError as e:
            self.log_test("数据库连接", False, "无法连接到服务器")
            return False
        except Exception as e:
            self.log_test("数据库连接", False, str(e))
            return False
    
    def run_all_tests(self):
        """运行所有测试"""
        print("=" * 60)
        print("实验室项目管理系统 - 网站测试")
        print("=" * 60)
        print(f"目标URL: {self.base_url}")
        print()
        
        try:
            # 基础连接测试
            print("[1/8] 测试基础连接...")
            time.sleep(0.5)
            self.test_homepage()
            
            print("[2/8] 测试登录页面...")
            time.sleep(0.5)
            self.test_login_page()
            
            print("[3/8] 测试注册页面...")
            time.sleep(0.5)
            self.test_register_page()
            
            print("[4/8] 测试无效登录...")
            time.sleep(0.5)
            self.test_login_invalid_credentials()
            
            print("[5/8] 测试仪表板保护...")
            time.sleep(0.5)
            self.test_dashboard_access()
            
            print("[6/8] 测试安全标头...")
            time.sleep(0.5)
            self.test_security_headers()
            
            print("[7/8] 测试静态文件...")
            time.sleep(0.5)
            self.test_static_files()
            
            print("[8/8] 测试数据库连接...")
            time.sleep(0.5)
            self.test_database_connection()
            
        except Exception as e:
            print(f"\n错误: {e}")
        
        # 汇总结果
        self.print_summary()
    
    def print_summary(self):
        """打印测试汇总"""
        print("\n" + "=" * 60)
        print("测试汇总")
        print("=" * 60)
        
        passed = sum(1 for r in self.test_results if r['success'])
        total = len(self.test_results)
        
        print(f"\n总计: {passed}/{total} 测试通过")
        print(f"通过率: {(passed/total*100):.1f}%\n")
        
        # 分类显示
        passed_tests = [r for r in self.test_results if r['success']]
        failed_tests = [r for r in self.test_results if not r['success']]
        
        if passed_tests:
            print("✓ 通过的测试:")
            for test in passed_tests:
                print(f"  • {test['test']}")
        
        if failed_tests:
            print("\n✗ 失败的测试:")
            for test in failed_tests:
                print(f"  • {test['test']}")
                if test['message']:
                    print(f"    {test['message']}")
        
        print("\n" + "=" * 60)
        
        return passed, total


if __name__ == "__main__":
    tester = WebsiteTester(BASE_URL)
    
    print("\n⏳ 正在等待服务器响应...")
    time.sleep(1)
    
    try:
        tester.run_all_tests()
    except KeyboardInterrupt:
        print("\n\n⚠ 测试被中断")
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        print("\n请确保服务器正在运行 (http://localhost:5000)")
