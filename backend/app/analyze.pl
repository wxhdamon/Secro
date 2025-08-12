#/backend/app/analyze.pl

#!/usr/bin/perl
use strict;
use warnings;
use JSON;

# 从参数读取输入/输出文件名
my $input_file = $ARGV[0] || 'scan_result.json';
my $output_file = $ARGV[1] || 'analyzed.txt';

# 读取 JSON 文件内容
open(my $fh, '<', $input_file) or die "Cannot open $input_file: $!";
my $json_text = do { local $/; <$fh> };
close($fh);

# 解码 JSON
my $data = decode_json($json_text);

# 统计服务类型
my %service_count;
foreach my $entry (@$data) {
    my $service = $entry->{service} || 'Unknown';
    $service_count{$service}++;
}

# 写入统计结果
open(my $out, '>', $output_file) or die "Cannot write to $output_file: $!";
print $out "服务类型统计结果：\n";
foreach my $service (sort keys %service_count) {
    print $out "$service: $service_count{$service} 个端口开放\n";
}
close($out);
