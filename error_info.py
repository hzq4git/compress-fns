# definition of error code and error message used in segment module

# @Author: ruanyi
# @Time:   2019/12/19

# error exit code = 255
# @SHCODE: 4000～5000

EXITCODE = 255

ERROR_INFO = {
    "SHCODE": "10",
    "PARAMS_JSON": ("00", "input params error!"),
    "FILES_NOT_FOUND": ("01", "input files not found!"),
    "RUN_FFPROBE_INFO_ERROR": ("02", "run ffprobe extra info error!")
}
