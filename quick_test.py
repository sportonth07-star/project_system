"""
快速网站测试 - 实验室项目管理系统
"""
import requests
import sys
from bs4 import BeautifulSoup

BASE_URL = "http://localhost:5000"

print("=" * 60)
print("快速网站功能测试")
print("=" * 60)

tests_passed = 0
tests_total = 0

# 测试1: 主页
tests_total += 1
try:
    r = requests.get(f"{BASE_URL}/", timeout=3)
    if r.status_code == 200:
        print("✓ 主页 (/) - 可访问 (HTTP 200)")
        tests_passed += 1
    else:
        print(f"✗ 主页 (/) - HTTP {r.status_code}")
except Exception as e:
    print(f"✗ 主页 - 连接失败: {str(e)[:50]}")

# 测试2: 登录页面
tests_total += 1
try:
    r = requests.get(f"{BASE_URL}/login", timeout=3)
    if r.status_code == 200:
        print("✓ 登录页面 (/login) - 可访问 (HTTP 200)")
        tests_passed += 1
    else:
        print(f"✗ 登录页面 (/login) - HTTP {r.status_code}")
except Exception as e:
    print(f"✗ 登录页面 - 连接失败")

# 测试3: 注册页面
tests_total += 1
try:
    r = requests.get(f"{BASE_URL}/register", timeout=3)
    if r.status_code == 200:
        print("✓ 注册页面 (/register) - 可访问 (HTTP 200)")
        tests_passed += 1
    else:
        print(f"✗ 注册页面 (/register) - HTTP {r.status_code}")
except Exception as e:
    print(f"✗ 注册页面 - 连接失败")

# 测试4: 仪表板保护（无认证不能访问）
tests_total += 1
try:
    r = requests.get(f"{BASE_URL}/dashboard", timeout=3, allow_redirects=False)
    if r.status_code in [302, 303]:
        print("✓ 仪表板保护 (/dashboard) - 正确重定向 (HTTP 302)")
        tests_passed += 1
    elif r.status_code == 200:
        print("✗ 仪表板保护 - 未认证用户不应该能访问")
    else:
        print(f"✗ 仪表板 - HTTP {r.status_code}")
except Exception as e:
    print(f"✗ 仪表板保护 - 连接失败")

# 测试5: 静态文件 - CSS
tests_total += 1
try:
    r = requests.get(f"{BASE_URL}/static/css/main.css", timeout=3)
    if r.status_code == 200:
        print("✓ 静态文件 (CSS) - 可加载 (HTTP 200)")
        tests_passed += 1
    else:
        print(f"✗ 静态文件 (CSS) - HTTP {r.status_code}")
except Exception as e:
    print(f"✗ 静态文件 (CSS) - 连接失败")

# 测试6: 静态文件 - JS
tests_total += 1
try:
    r = requests.get(f"{BASE_URL}/static/js/dashboard.js", timeout=3)
    if r.status_code == 200:
        print("✓ 静态文件 (JS) - 可加载 (HTTP 200)")
        tests_passed += 1
    else:
        print(f"✗ 静态文件 (JS) - HTTP {r.status_code}")
except Exception as e:
    print(f"✗ 静态文件 (JS) - 连接失败")

# 测试7: 安全标头
tests_total += 1
try:
    r = requests.get(f"{BASE_URL}/", timeout=3)
    headers = r.headers
    security_ok = (
        headers.get('X-Content-Type-Options') == 'nosniff' and
        headers.get('X-Frame-Options') == 'DENY'
    )
    if security_ok:
        print("✓ 安全标头 - 已配置")
        tests_passed += 1
    else:
        print("✗ 安全标头 - 配置不完整")
except Exception as e:
    print(f"✗ 安全标头 - 检查失败")

# 测试8: 无效登录处理
tests_total += 1
try:
    session = requests.Session()
    r = session.get(f"{BASE_URL}/login", timeout=3)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find('input', {'name': 'csrf_token'})
    
    if csrf:
        csrf_token = csrf.get('value')
        data = {
            'username': 'testuser_invalid_123',
            'password': 'wrongpassword',
            'csrf_token': csrf_token
        }
        r = session.post(f"{BASE_URL}/login", data=data, timeout=3)
        
        if r.status_code == 200:
            print("✓ 无效登录处理 - 返回登录页面")
            tests_passed += 1
        else:
            print(f"✗ 无效登录处理 - HTTP {r.status_code}")
    else:
        print("✗ 无效登录处理 - 找不到CSRF令牌")
except Exception as e:
    print(f"✗ 无效登录处理 - 失败")

print("\n" + "=" * 60)
print(f"测试结果: {tests_passed}/{tests_total} 通过")
print(f"通过率: {(tests_passed/tests_total*100):.1f}%")
print("=" * 60)

if tests_passed == tests_total:
    print("✓ 所有测试通过！网站运行正常")
    sys.exit(0)
elif tests_passed >= tests_total * 0.7:
    print("⚠ 大部分测试通过，但有一些问题需要修复")
    sys.exit(1)
else:
    print("✗ 许多测试失败，请检查服务器配置")
    sys.exit(2)
