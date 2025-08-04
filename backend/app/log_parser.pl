#/backend/app/log_parser.pld
#!/usr/bin/perl
use strict;
use warnings;

# 一个简单的日志扫描器，用于检测 SSH 登录失败的日志事件
# 使用：cat /var/log/auth.log | perl log_parser.pl

while (<>) {
    if (/Failed password/) {
        print "ALERT: $_";
    }
}

