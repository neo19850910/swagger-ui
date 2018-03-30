#-*- coding:utf8 -*-
import os ,time
import smtplib
from email.mime.text import MIMEText
from config.config import *

def reportsort():
    result_dir = os.getcwd()+"\\report\\"
    reports = os.listdir(result_dir)
    reports.sort(key=lambda lists: os.path.getmtime(os.path.join(result_dir, lists)) if not os.path.isdir(os.path.join(result_dir, lists)) else 0)
    result = reports[-2]
    return os.path.join(result_dir, result)

def sentmail(file_new):
    mail_from=getConfig("EMAIL", "sender")
    mail_to = (getConfig("EMAIL", "receiver")).split(',')
    f = open(file_new, 'rb')
    mail_body = f.read()
    f.close()
    msg = MIMEText(mail_body, _subtype='html', _charset='utf-8')  #此处可以用默认模式，默认模式需要导出为html文件，或者直接将格式改为html，在邮件里直接观看
    msg['Subject'] = getConfig("EMAIL", "subject")
    msg['date'] = time.strftime('%a, %d %b %Y %H:%M:%S %z')
    msg['From'] = getConfig("EMAIL", "sender")
    msg['To'] = getConfig("EMAIL", "receiver")
    smtp = smtplib.SMTP_SSL(getConfig("EMAIL", "mail_host"), getConfig("EMAIL", "mail_port"))
    smtp.login(getConfig("EMAIL", "mail_user"), getConfig("EMAIL", "mail_pass"))  #动态密码，请注意
    smtp.sendmail(mail_from, mail_to, msg.as_string())
    smtp.quit()
if __name__ == '__main__':
    sentmail(reportsort())