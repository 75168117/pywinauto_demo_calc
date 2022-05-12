# -*- coding: utf-8 -*-
# function 自动化测试计算器
import os.path
import re
import win32con
import codecs
from pywinauto import Desktop
from pywinauto.application import Application
from pywinauto.keyboard import send_keys
import win32clipboard as wc
 
#转换数字为汉字
def change_chn(num):
    chn_list = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九']
    return chn_list[num]
 
if __name__ == '__main__':
    # 设置txt文件保存路径
    txt_path = './TXT/'
    if not os.path.exists(txt_path):
        os.mkdir(txt_path)
    
    # 设置控件信息的txt文件名
    control_txt_name = txt_path + 'control.txt'
    
    # 设置标题信息的txt文件路径
    title_txt_file = txt_path + "title.txt"
    
    # 设置检测记录信息的txt文件路径
    record_txt_file = txt_path + "record.txt"

    # 打开计算器应用
    app = Application(backend="uia").start("calc.exe")
    dlg_spec = Desktop(backend="uia").window(title=u"计算器", visible_only=False)
    dlg_spec.restore()
    
    # 打印控件信息到指定路径
    dlg_spec.print_control_identifiers(filename=control_txt_name)
    
    # 读取控件信息txt文件
    fr = open(control_txt_name, "r")
    # 设置正则表达式，用于提取button控件的title
    par = r'.+title=\"([^,]+)\".+\"Button\"'
    content = []
    for line in fr.readlines():
        res = re.compile(par).findall(line)
        if res:
            result = str(res[0]).split(',')
            par_str = str(result[0])
            content.append(par_str)
        else:
            pass
    fr.close()
    
    # 将提取到的信息另存为标题txt文件
    fw = codecs.open(title_txt_file, "w", 'utf8')
    for i in range(0, len(content)):
        # 使用列表推导式把列表中的单个元素全部转化为str类型
        new_content_line = [str(i) for i in content[i]]
        # 把列表中的元素放在空串中，元素间用空格隔开
        new_content_lines = ''.join(new_content_line)
        # 将多余字符替换为空字符
        new_content_lines = re.sub(r'\'', "", new_content_lines)
        # 去除空行
        if new_content_lines == '':
            pass
        else:
            fw.write(new_content_lines + '\n')
    fw.close()
    
    # 清空 record_txt_file文件内容
    fw_record = codecs.open(record_txt_file, "a", 'utf8')
    fw_record.seek(0)
    fw_record.truncate()
    # 自动化测试【一位整数乘法】(10个数字两两相乘，共10*10=100种情况)
    for i in range(1, 10):
        for j in range(1, 10):
            real_value = i * j
            dlg_spec.window(title=change_chn(i), control_type="Button").click()
            dlg_spec.window(title="乘以", control_type="Button").click()
            dlg_spec.window(title=change_chn(j), control_type="Button").click()
            dlg_spec.window(title="等于", control_type="Button").click()
            # 复制内容
            send_keys("^c")
            # 打开剪贴板
            wc.OpenClipboard()
            # 获取剪贴板内容
            copy_text = wc.GetClipboardData(win32con.CF_TEXT)
            # 关闭剪贴板
            wc.CloseClipboard()
            ret = str(copy_text, encoding = "utf-8")  
            # 获取计算结果
            calc_value = ret.strip('\0')
            # 判断计算器计算结果
            if calc_value == str(real_value):
                record = "%d×%d=%s 【正确】" % (i, j, calc_value)
                print(record)
            else:
                record = "%d×%d=%s 【错误】" % (i, j, calc_value)
                print(record)
            # 将检测信息另存为日志txt文件
            fw_record = codecs.open(record_txt_file, "a", 'utf8')
            fw_record.write(record + '\n')
    fw_record.close()
