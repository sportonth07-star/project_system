"""
轻量级网站测试 - 快速检查服务器状态
"""
import requests
import sys

BASE_URL = "http://localhost:5000"

print("=" * 60)
print("快速网站状态检查")
print("=" * 60)

# 检查服务器是否运行
print("\n检查服务器连接...", end=" ")
try:
    r = requests.get(f"{BASE_URL}/", timeout=2)
    print(f"✓ 服务器在线 (HTTP {r.status_code})")
    server_online = True
except requests.exceptions.ConnectionRefusedError:
    print("✗ 服务器未运行或无法连接")
    print(f"\n请在另一个终端运行:")
    print(f"  cd c:\\claude\\lab-project-manager")
    print(f"  python run.py")
    print(f"  或")
    print(f"  start.bat")
    sys.exit(1)
except Exception as e:
    print(f"✗ 连接失败: {e}")
    sys.exit(1)

# 快速功能检查
print("\n快速功能检查:")
tests = {
    "主页": "/",
    "登录": "/login",
    "注册": "/register",
    "项目列表": "/projects",
    "用户管理": "/users",
    "仪表板": "/",  # 根路由
}

passed = 0
for name, path in tests.items():
    try:
        r = requests.get(f"{BASE_URL}{path}", timeout=2, allow_redirects=True)
        status = "✓" if r.status_code in [200, 302, 401] else "⚠"
        print(f"  {status} {name:15} HTTP {r.status_code}")
        if status == "✓":
            passed += 1
    except Exception as e:
        print(f"  ✗ {name:15} 连接失败")

print("\n" + "=" * 60)
print(f"状态: {passed}/{len(tests)} 页面正常")

if passed >= len(tests) * 0.7:
    print("✓ 网站基本可用")
    print("\n可以在浏览器中访问: http://localhost:5000")
else:
    print("⚠ 网站部分功能异常")
