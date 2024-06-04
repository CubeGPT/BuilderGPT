# Author: Acer Zhang
# Datetime: 2021/9/17 
# Copyright belongs to the author.
# Please indicate the source for reprinting.
import sys


class StdOutWrapper:
    def __init__(self, stdout, callback=None, do_print=True):
        self.buff = ""
        self.stdout = stdout
        self.callback = callback
        self.do_print = do_print

    def write(self, output_stream):
        self.buff += output_stream
        if self.do_print:
            self.stdout.write(output_stream)
        if self.callback and ("\n" in self.buff or "\r" in output_stream):
            self.callback(self.buff)
            self.buff = ""

    def flush(self):
        self.buff = ""

    def __del__(self):
        sys.stdout = self.stdout


class DataCache:
    def __init__(self, seq_len=10, cache=7):
        assert seq_len >= cache, "请设置seq_len的值低于cache"
        self.seq_len = seq_len
        self.cache = cache
        self.seq = list()

    def add(self, item):
        if len(self.seq) == self.seq_len:
            for i in range(self.seq_len - self.cache):
                self.seq.pop(0)
        self.seq.append(item)

    def __add__(self, other):
        self.add(other)
        return self
