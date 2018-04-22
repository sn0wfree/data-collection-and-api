# -*- coding:utf-8 -*-
import commands
import re
import time


def findstatus(output):
    o = output
    activestatus = o.split('\n')[2]
    a = re.search('Active:', activestatus).span()
    b = re.search('\(', activestatus).span()

    return 'active' in activestatus[a[1]:b[0]]


def getstatus(count=0, checkcommand='systemctl status shadowsocks', startcommand='systemctl start shadowsocks', othercommand=''):
    o = commands.getoutput(checkcommand)
    if findstatus(o):
        print 'ok'
        return 'ok'
    else:
        start = commands.getoutput(startcommand)
        time.sleep(100)
        if count < 100:

            getstatus(count + 1)
        else:
            sms= 'Error,Have tried %d times. will stop!' % count
            sendemail(sms)
            return sms
def sendemail(messagestr):
	import smtplib
	from email.mime.text import MIMEText
	from email.header import Header
	 
	sender = '846079443@qq.com'
	receivers = ['linlu1234567@sina.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
	 
	# 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
	if messagestr ==None:
		messagestr='Shadowsocks has down and cannot restart automatically!'
	else:
		pass
	message = MIMEText(messagestr, 'plain', 'utf-8')
	message['From'] = Header("me", 'utf-8')
	message['To'] =  Header("me", 'utf-8')
	 
	subject = 'Python: Fail to start shadowsocks'
	message['Subject'] = Header(subject, 'utf-8')
	 
	 
	try:
	    smtpObj = smtplib.SMTP('localhost')
	    smtpObj.sendmail(sender, receivers, message.as_string())
	    print "邮件发送成功"
	except smtplib.SMTPException:
	    print "Error: 无法发送邮件"
if __name__ == '__main__':
    print getstatus()
    time.sleep(10)
