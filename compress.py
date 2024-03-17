#!/usr/bin/env python3
# coding=utf-8
import subprocess
import sys
import json
import os, signal
import error_info
import cmd

######## 通用模版部分 begin ###########
def parse_input(param_str):
    param_map = json.loads(param_str)
    work_path = ''
    input_files = []
    arg_map = {}
    if 'work_path' in param_map:
        work_path = param_map['work_path']
    if 'input_files' in param_map:
        input_files = param_map['input_files']
    if 'arg_map' in param_map:
        arg_map = param_map['arg_map']
    return work_path, input_files, arg_map

def check_code(code, arg_map, error_key, extra_message=""):
    error_code = error_info.ERROR_INFO["SHCODE"] + error_info.ERROR_INFO[error_key][0]
    error_msg = error_info.ERROR_INFO[error_key][1] + extra_message
    if code:
        output = {'status': int(error_code), 'description': error_msg, 'arg_map': arg_map}
        sys.stdout.write(json.dumps(output))
        sys.exit(error_info.EXITCODE)


def run(cmdline):
    child_proc = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,
                                  preexec_fn=os.setsid)
    try:
        std_out, std_err = child_proc.communicate()
        if child_proc.returncode == 0:
            output_results = std_out.strip().decode()
        else:
            output_results = std_err.strip().decode()
    finally:
        try:
            os.killpg(child_proc.pid, signal.SIGKILL)
        except OSError:
            pass

    return output_results, child_proc.returncode

def success_output(output_files, arg_map):
    output = {"status": 0, "files": output_files, "arg_map": arg_map}
    sys.stdout.write(json.dumps(output))

######## 通用模版部分 end ###########

class Compress:
    work_path = ''
    input_files = []
    arg_map = {}

    input_video_path = ''
    output_video_path = ''
    out_width = 1280
    out_height = 720
    
    def __init__(self, param_str):
        work_path, input_files, arg_map = parse_input(param_str)
        self.work_path = work_path
        self.input_files = input_files
        self.arg_map = arg_map
        self.check_params()

    def check_params(self):
        inputs = (self.work_path, self.input_files)
        output_params = {'metas': {'cpu': self.cpu, 'mem': self.mem, 'gpu': self.gpu, 'concurrent': self.concurrent}}
        check_code((not all(inputs)), output_params, "PARAMS_JSON", "Number of params must be 2.")
        if not os.path.exists(self.work_path):
            os.makedirs(self.work_path)
        for file in self.input_files:
            if file["key"] == "video":
                self.input_video_path = file["local_path"] if file["local_path"] else file["remote_url"]

    def do(self):
        #命令参数个性化
        cmdline = cmd.CMD.format(input_file=self.input_video_path, out_width=self.out_width, out_height=self.out_height, out_file=self.output_video_path)
        result, code = run(cmdline)
        output_params = {
            'metas': {'cmdline': cmdline, 'ret_code': code, 'cpu': self.cpu, 'mem': self.mem, 'gpu': self.gpu,
                      'concurrent': self.concurrent}}
        check_code(code, output_params, "RUN_FFPROBE_INFO_ERROR",
                   " ffprobe error info: {0},{1}".format(code, result[0:2000]))
        output_video_info = {"key": "video", "form": "ByteContent", "body": self.output_video_path}
        success_output([output_video_info], output_params)

if __name__ == '__main__':
    params = sys.argv[1]
    job = Compress(params)
    job.do()