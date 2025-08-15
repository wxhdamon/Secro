#!/usr/bin/perl
use strict;           
use warnings;         
use utf8;             
use JSON;             
use Encode qw(encode);  

# 参数检查
if (@ARGV != 2) {
    print "参数错误：输入和输出文件各一个。\n";
    exit 1;
}
my ($input_file, $output_file) = @ARGV;

# 读取JSON文件
open(my $INPUT, '<:encoding(UTF-8)', $input_file) or die "can't open $input_file: $!\n";
my $json_string = do { local $/; <$INPUT> };  # 读取整个文件内容
close($INPUT) or die "can't close $input_file: $!\n";

# 解码JSON
my $data = eval { decode_json(encode("UTF-8", $json_string)) };
die "JSON decode failure: $@\n" if $@;
die "the input JSON must be an array\n" unless ref($data) eq 'ARRAY';

# 按服务类型统计开放端口
my %service_num;
for my $entry (@$data) {
    next unless ref($entry) eq 'HASH';
    my $status = $entry->{status} // '';
    next unless lc($status) eq 'open';

    my $service = $entry->{service};
    $service = (defined $service && $service ne '') ? $service : '未知服务';
    $service_num{$service}++;
}

# 生成输出文本
my $output = "服务类型统计结果：\n";
for my $srv (sort keys %service_num) {
    $output .= "$srv: $service_num{$srv} 个端口开放\n";
}
# 如果没有开放端口，添加提示
$output .= "无开放端口\n" unless %service_num;

# 写入输出文件
open(my $OUTPUT, '>:encoding(UTF-8)', $output_file) or die "can't open $output_file: $!\n";
print $OUTPUT $output;
close($OUTPUT) or die "can't close $output_file: $!\n";