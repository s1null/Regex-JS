# !/usr/bin/env python3
# -*- encoding: utf-8 -*-

from lib.Controller import Project
from lib.TestProxy import testProxy
from lib.common.cmdline import CommandLines

class Program():
    def __init__(self,options):
        self.options = options

    def check(self):
        url = self.options.url
        t = Project(url,self.options)
        t.parseStart()


if __name__ == '__main__':
    cmd = CommandLines().cmd()
    testProxy(cmd,1)
    RegxJS = Program(cmd)
    RegxJS.check()