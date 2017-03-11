import argparse
version1 = '0.1'
parser = argparse.ArgumentParser(
    usage='%(prog)s [options]', #自訂使用方法外觀，預設由參數產生
    description='程式說明', #頂端程式說明，預設 None
    epilog='程式說明2', #底端程式說明，預設 None
    prefix_chars='-', #參數起始字串，預設 '-'
    )
parser.add_argument('-V', '--version', action='version', version=version1, help="Show Version")
parser.add_argument('-s', action='store_true', help="s!")
args = parser.parse_args() #解析

def showof():
    return args
