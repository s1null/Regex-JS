<h1 align="center">🔍 Regex-JS</h1>
<p align="center">一款简单但强大的JS敏感信息检测工具 ⚡️</p>

## ⚠️ 免责声明

由于传播、利用Regex-JS工具（下简称本工具）提供的检测功能而造成的**任何直接或者间接的后果及损失**，均由使用者本人负责，本人**不为此承担任何责任**。

本工具会根据使用者检测结果**自动生成**扫描结果报告，本报告内容及其他衍生内容均**不能代表**本人的立场及观点。

请在使用本工具时遵循使用者以及目标系统所在国当地的**相关法律法规**，一切**未授权测试均是不被允许的**。若出现相关违法行为，将**保留追究**您法律责任的权利，并**全力配合**相关机构展开调查。

## 🎯 项目介绍
本工具源于 [Packer Fuzzer](https://github.com/rtcatc/Packer-Fuzzer)，感谢Packer Fuzzer团队开发的优秀工具！

🤔 为什么要开发这个工具？
- 实际测试中，大多数测试人员更倾向于手动测试
- 自动化测试可能因参数不全或API地址不正确导致无效流量
- 我们精简了功能，专注于JS文件下载和敏感信息检测
- 自动生成美观的HTML报告，让结果一目了然！

## 🚀 特色功能
- 🔄 自动下载并解析JS文件
- 🔍 智能正则匹配敏感信息
- 📊 生成美观的HTML报告
- 🛠 简单易用的命令行界面

## 💻 安装环境

### 1. Python环境配置
确保您已安装 `Python3.X` 和 `pip3`

🍎 **MacOS**:
```bash
brew install python3 #会自动安装pip3
```

🐧 **Ubuntu**:
```bash
sudo apt-get install -y python3 && sudo apt install -y python3-pip
```

🎩 **CentOS**:
```bash
sudo yum -y install epel-release && sudo yum install python3 && yum install -y python3-setuptools && easy_install pip
```

### 2. NodeJS环境配置
为了更好地解析JS代码，我们推荐使用原生`NodeJS`环境

🍎 **MacOS**:
```bash
brew install node
```

🐧 **Ubuntu**:
```bash
sudo apt-get install nodejs && sudo apt-get install npm
```

🎩 **CentOS**:
```bash
sudo yum -y install nodejs
```

### 3. 安装依赖
```bash
pip3 install -r requirements.txt
```

## 🎮 使用方法

基本用法非常简单：
```bash
python3 main.py -u URL
```

## 📝 使用示例

1. 基础扫描：
```bash
python3 main.py -u https://example.com
```

2. 带Cookie的扫描：
```bash
python3 main.py -u https://example.com -c "PHPSESSID=xxx"
# 或者
python3 main.py -u https://example.com -c "Cookie: PHPSESSID=xxx"
```

3. 添加自定义请求头：
```bash
python3 main.py -u https://example.com -d "Authorization: Bearer xxx"
# 多个请求头使用||分隔
python3 main.py -u https://example.com -d "Authorization: Bearer xxx||X-Token: xxx"
```

4. 使用代理：
```bash
# HTTP代理
python3 main.py -u https://example.com -p "http://127.0.0.1:8080"
# SOCKS5代理
python3 main.py -u https://example.com -p "socks5://127.0.0.1:1080"
```

5. 指定额外的JS文件：
```bash
python3 main.py -u https://example.com -j "path/to/extra.js"
```

6. 静默模式（自定义报告名称）：
```bash
python3 main.py -u https://example.com -s "my_report"
```

7. 自定义请求方式和内容：
```bash
# POST请求
python3 main.py -u https://example.com --st POST --ct "application/json" --pd '{"key":"value"}'
```

8. 查看帮助信息：
```bash
python3 main.py -h
```

## 🎉 扫描结果展示

![image](https://github.com/user-attachments/assets/4719e2f6-1204-4331-94f0-335cbf394498)

扫描完成后，工具会在当前目录生成一个HTML报告，包含：
- 发现的敏感信息列表
- 信息危险等级评估
- 详细的匹配位置和上下文
- 修复建议

### 4. 检测类型
目前支持检测的敏感信息类型包括：
- 💳 各类accesskey
- 📧 邮箱地址
- 🔒 密码和加密信息
- 🌐 API接口
- 📱 手机号码
- 🆔 身份证号码
- 💻 IP
- 更多...

## 🤝 贡献代码
欢迎提交 Issue 和 Pull Request！

## 🎉 开源协议
本项目遵循 MIT 协议
