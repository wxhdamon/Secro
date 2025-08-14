#/backend/app/analyze.pl

#!/usr/bin/perl
use strict;
use warnings;
use utf8; 
use JSON;
use Encode qw(encode);
use File::Slurper qw(read_text write_text);

# 参数检查
if (@ARGV != 2) {
    print "参数错误：输入和输出文件各一个。\n";
    exit 1;
}
my ($input_file, $output_file) = @ARGV;

#读取JSON 文件（UTF‑8）
my $json_text = read_text($input_file, 'UTF-8')
    or die "无法读取输入文件 $input_file: $!\n";

#解码JSON
my $data = eval { decode_json( encode("UTF-8", $json_text) ) };
die "JSON 解码失败: $@\n" if $@;
die "输入 JSON 必须是数组\n" unless ref($data) eq 'ARRAY';

#按服务类型统计开放端口
my %service_counts;
for my $entry (@$data) {
    next unless ref($entry) eq 'HASH';
    my $status  = $entry->{status}  // '';
    next unless lc($status) eq 'open';

    my $service = $entry->{service};
    $service = (defined $service && $service ne '') ? $service : '未知服务';
    $service_counts{$service}++;
}

#生成输出文本
my $output = "服务类型统计结果：\n";
for my $srv (sort keys %service_counts) {
    $output .= "$srv: $service_counts{$srv} 个端口开放\n";
}

#写入输出文件（UTF‑8）
write_text($output_file, $output, 'UTF-8')

