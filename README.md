 <h1 align="center" >Regex-JS</h1>

## 免责声明

由于传播、利用Regex-JS工具（下简称本工具）提供的检测功能而造成的**任何直接或者间接的后果及损失**，均由使用者本人负责，本人**不为此承担任何责任**。

本工具会根据使用者检测结果**自动生成**扫描结果报告，本报告内容及其他衍生内容均**不能代表**本人的立场及观点。

请在使用本工具时遵循使用者以及目标系统所在国当地的**相关法律法规**，一切**未授权测试均是不被允许的**。若出现相关违法行为，我们将**保留追究**您法律责任的权利，并**全力配合**相关机构展开调查。

## 介绍
本工具源于<h5 align="center" ><a href="https://github.com/rtcatc/Packer-Fuzzer">Packer Fuzzer</a></h5>，感谢Packer Fuzzer团队开发的工具，Packer Fuzzer是一个非常优秀的工具，但在实际测试情况当中测试人员大多数使用的还是手动测试，工具自动化由于参数不全或api地址不正确会导致无效的流量增加，本工具删减了自动化测试，只保留了下载js功能，并添加了自动正则匹配js当中的敏感信息，并将结果生成html报告。

## 安装环境
1. 本工具使用Python3语言开发，在运行本工具之前请确保您装有`Python3.X`软件及`pip3`软件。若您未安装相关环境，可通过如下指引安装：[https://www.runoob.com/python3/python3-install.html](https://www.runoob.com/python3/python3-install.html)

   MacOS用户可使用如下命令快速安装：

   ```bash
   brew install python3 #会自动安装pip3
   ```

   Ubuntu用户可使用如下命令快速安装：

   ```bash
   sudo apt-get install -y python3 && sudo apt install -y python3-pip
   ```

   CentOS用户可使用如下命令快速安装：

   ```bash
   sudo yum -y install epel-release && sudo yum install python3 && yum install -y python3-setuptools && easy_install pip
   ```

2. 本工具将会通过`node_vm2`运行原生`NodeJS`代码，故我们推荐您安装`NodeJS`环境（不推荐其他JS运行环境，可能会导致解析失败）。若您未安装相关环境，可通过如下指引安装：[https://www.runoob.com/nodejs/nodejs-install-setup.html](https://www.runoob.com/nodejs/nodejs-install-setup.html)

   MacOS用户可使用如下命令快速安装：

   ```bash
   brew install node
   ```

   Ubuntu用户可使用如下命令快速安装：

   ```bash
   sudo apt-get install nodejs && sudo apt-get install npm
   ```

   CentOS用户可使用如下命令快速安装：

   ```bash
   sudo yum -y install nodejs
   ```

3. 请使用如下命令一键安装本工具所需要的Python运行库：

   ```bash
   pip3 install -r requirements.txt
   ```
