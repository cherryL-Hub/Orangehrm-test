# Orangehrm自动化测试

## 项目简介
这是基于[Orangehrm](https://opensource-demo.orangehrmlive.com)员工管理系统的UI复合接口的自动化测试项目

## 技术栈
- python 3.11
- pytest
- selenium (UI自动化)
- requests (接口自动化)
- fixture (pytest 依赖注入)
- Page Object Model (页面封装)
- Allure(测试报告)
- GitHub Actions(CI/CD)
- Docker(容器化运行)

## 如何运行
 ### 1.安装依赖
```bash
pip install -r requirements.txt
```
### 2.运行
```bash
pytest -v -s
```
### 3.生成allure报告
```bash
# 生成测试数据
pytest --alluredir=./allure-results

# 预览报告
allure serve ./allure-results

# 生成静态报告
allure generate ./allure-results -o ./allure-report --clean
```

## 测试场景覆盖
| 模块     | 测试内容                                       | 测试路径  |
|:-------|:-------------------------------------------|:------|
| 登录     | 正常用户登录，错误用户登录（包含错误断言）                      | 接口    |
| 员工信息管理 | UI创建员工（含异常处理+ID冲突重试），接口进行查询，更改，删除，删除进行二次验证 | UI+接口 |

## 项目结构
```
orangehrm_test/
├── pages/                 # Page Object 页面封装
│   ├── dashboard_page.py
│   ├── pim_page.py
│   ├── add_page.py
│   └── infomation_page.py
├── tests/                 # 测试用例
│   ├── conftest.py        # fixture 配置
│   └── test_pim.py        # 完整流程测试
├── api_client.py          # 接口请求封装
├── requirements.txt
├── README.md
├── .github/workflows/     # CI/CD 配置
└── allure-results/        # 测试报告数据
```
### 作者
李湘湘

### 参考资料
- pytest文档
- requests文档
- selenium文档
- Orangehrm官网