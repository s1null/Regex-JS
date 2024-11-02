# !/usr/bin/env python3
# -*- encoding: utf-8 -*-

import optparse,sys


class CommandLines():

    def cmd(self):
        parse = optparse.OptionParser()
        parse.add_option('-u', '--url', dest='url', help='Please Enter the Target Site')
        
        parse.add_option('-c', '--cookie', dest='cookie', help='Please Enter the Site Cookies')

        parse.add_option('-d', '--head', dest='head', default='Cache-Control:no-cache', help='Please Enter the extra HTTP head')
        
        parse.add_option('-l', '--lang', dest='language', default='zh', help='Please Select Language')

        parse.add_option('-p', '--proxy', dest='proxy', type=str, help='Please Enter your own Proxy Address')

        parse.add_option('-j', '--js', dest='js', type=str, help='Extra JS Files')
        parse.add_option('-s', '--silent', dest='silent', type=str, help='Silent Mode (Custom Report Name)')

        parse.add_option('-f', '--flag', dest='ssl_flag', default='1', type=str, help='SSL SEC FLAG')

        parse.add_option('--st', '--sendtype', dest='sendtype', type=str, help='HTTP Request Type POST or GET')

        parse.add_option('--ct', '--contenttype', dest='contenttype', type=str, help='HTTP Request Header Content-Type')

        parse.add_option('--pd', '--postdata', dest='postdata', type=str, help='HTTP Request PostData (When Scanning)')

        (options, args) = parse.parse_args()
        if options.url == None:
            parse.print_help()
            sys.exit(0)
        return options


if __name__ == '__main__':
    print(CommandLines().cmd().cookie)
