import re

regex_ip = re.compile( r"(\d+)\.(\d+)\.(\d+)\.(\d+)" )

def mask_ip(clk_obj):
    clk_obj.ip = regex_ip.sub(r"\1.\2.\3.*", clk_obj.ip)
    return clk_obj