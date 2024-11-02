# !/usr/bin/env python3
# -*- encoding: utf-8 -*-

import os
from urllib.parse import urlparse
from lib.ParseJs import ParseJs
from lib.common.utils import Utils
from lib.Database import DatabaseType
from lib.CheckPacker import CheckPacker
from lib.Recoverspilt import RecoverSpilt
from lib.common.CreatLog import creatLog,log_name,logs
from lib.RegexMatcher import RegexMatcher



class Project():

    def __init__(self, url, options):
        self.url = url
        self.codes = {}
        self.options = options

    def parseStart(self):
        projectTag = logs
        if self.options.silent != None:
            print("[TAG]" + projectTag)
        DatabaseType(projectTag).createDatabase()
        ParseJs(projectTag, self.url, self.options).parseJsStart()
        path_log = os.path.abspath(log_name)
        path_db = os.path.abspath(DatabaseType(projectTag).getPathfromDB() + projectTag + ".db")
        creatLog().get_logger().info("[!] " + Utils().getMyWord("{db_path}") + path_db)  #显示数据库文件路径
        creatLog().get_logger().info("[!] " + Utils().getMyWord("{log_path}") + path_log) #显示log文件路径
        checkResult = CheckPacker(projectTag, self.url, self.options).checkStart()


        if checkResult == 1 or checkResult == 777: #打包器检测模块
            
            if checkResult != 777: #确保检测报错也能运行
                creatLog().get_logger().info("[!] " + Utils().getMyWord("{check_pack_s}"))
            RecoverSpilt(projectTag, self.options).recoverStart()

        else:
            creatLog().get_logger().info("[!] " + Utils().getMyWord("{check_pack_f}"))
        
        res = urlparse(self.url)
        host = res.netloc
        directory = "tmp" + os.sep + projectTag + "_" + host
        regex_file = os.getcwd() + os.sep + "RegexLibrary.json"  # 替换为正则表达式库文件路径

        matcher = RegexMatcher(regex_file)
        matcher.scan_directory(directory)
        matcher.generate_report(f'reports/{host}_report.html')
        print("[!] "+ Utils().getMyWord("{report_path}") +f'reports/{host}_report.html')
