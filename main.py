import sys
import time
from urllib import request
from lxml import etree
import smtplib
from email.mime.text import MIMEText
import datetime


def send_mail(title, content, s, r, passwd):
    #设置服务器所需信息
    #163邮箱服务器地址
    mail_host = 'smtp.qq.com'  
    #163用户名
    mail_user = s  
    #密码(部分邮箱为授权码) 
    mail_pass = passwd 
    #邮件发送方邮箱地址
    sender = s + '@qq.com'  
    #邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
    receivers = [r]  

    #设置email信息
    #邮件内容设置
    message = MIMEText(content,'plain','utf-8')
    #邮件主题       
    message['Subject'] = title
    #发送方信息
    message['From'] = sender 
    #接受方信息     
    message['To'] = receivers[0]  

    server = smtplib.SMTP_SSL(mail_host, 465) # SMTP协议默认端口是25
    server.set_debuglevel(1)
    #登录到服务器
    server.login(mail_user,mail_pass) 
    #发送
    server.sendmail(sender,receivers,message.as_string()) 
    #退出
    server.quit() 

def filterNone(item):
  if item == None:
      return False
  else:
      return True

def ttg(url, cookie, s, r, passwd):
  req = request.Request(url)
  req.add_header('user-agent', 'python urllib')
  req.add_header('cookie', cookie)
  with request.urlopen(req) as f:
    content = f.read().decode('utf-8')
    tree = etree.HTML(content)
    items = tree.xpath('//a[starts-with(@href,"?action=viewtopic&topicid=")]/b')
    item = next((i for i in items if i.text != None), None)

    if item != None:
        title = item.text
        link = item.xpath("..")[0].attrib["href"]
        last_reply = item.xpath("..")[0].xpath("..")[0].xpath('..')[0].xpath("..")[0].xpath("..")[0].xpath('..')[0].xpath('..')[0].xpath('./td[5]/nobr')[0].text

        now = time.time() + 3600 * 8
        past = (now -  time.mktime(time.strptime(last_reply, "%Y-%m-%d %H:%M:%S"))) / 3600
        if (title.lower().find("opencd") != -1 or title.lower().find("open cd") != -1 or title.lower().find("皇后") != -1) and past <= 0.25:
            send_mail(title, url.split("?")[0] + link, s, r, passwd)

def u2(url, cookie, s, r, passwd):
  req = request.Request(url)
  req.add_header('cookie', cookie)
  with request.urlopen(req) as f:
    content = f.read().decode('utf-8')
    tree = etree.HTML(content)
    items = tree.xpath('//a[starts-with(@href,"?action=viewtopic&forumid=12&topicid=1")]')

    item = next((i for i in items if i.text != None), None)

    if item  != None:
        title = item.text
        link = item.attrib['href']
        last_reply = item.xpath("..")[0].xpath("..")[0].xpath('..')[0].xpath("..")[0].xpath("..")[0].xpath('./td[4]/time')[0].attrib["title"]

        now = time.time() + 3600 * 8
        past = (now -  time.mktime(time.strptime(last_reply, "%Y-%m-%d %H:%M:%S"))) / 3600
        if (title.lower().find("opencd") != -1 or title.lower().find("open cd") != -1 or title.lower().find("皇后") != -1) and past <= 0.25:
            send_mail(title, url.split("?")[0] + link, s, r, passwd)

def main(argv):
  r1 = u2(argv[1], argv[2], argv[5],argv[6],argv[7])
  r2 = ttg(argv[3], argv[4], argv[5],argv[6],argv[7])


if __name__ == '__main__':
  main(sys.argv)
