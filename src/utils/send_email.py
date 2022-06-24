# -*- coding:utf-8 -*-
"""
======================================
@author:        Destiny
@file_name:     send_email.py
@create_date:   2022/6/16 13:39
@description:   Type the desc here ...
======================================
"""
from email.mime.multipart import MIMEMultipart
import smtplib
from email.mime.text import MIMEText
from email.header import Header


class SendEmail(object):
    def __init__(self, mail_info):
        self.mail_info = mail_info

    def format_email_content(self, result):
        head = """
                <head>
            <meta charset="UTF-8">
            <title>Title</title>
            <style type="text/css">
               .mailTable{
            width: 25%;
            margin: auto;
            border-top: 1px solid #808080;
            border-left: 1px solid #808080;
            position:static ;
            left: 0px;
        }
        .mailTable tr td{
            width: 200px;
            height: 35px;
            line-height: 35px;
            box-sizing: border-box;
            padding: 0 10px;
            border-bottom: 1px solid #808080;
            border-right: 1px solid #808080;
        }
        .mailTable tr td.column {
            background-color: #EFF3F6;
            color: #393C3E;
            width: 20%;
            text-align: center;
        
        }
        .mailTable td.data{
            width: 20%;
        }
        .mailTable caption{
            font-size: 1.4em;
            padding: 0.5em;
        }
        p{
            text-indent: 2em;
        }
            </style>
        </head>
        """
        body = """
                <body>
                Dear All:<br/>
                &emsp;&emsp;RPA平台非功能自动化用例，执行结果如下：<br/>
                <br/>
                运行环境：{}<br/>
                测试用例数：{} &emsp;Pass：{}&emsp;<b>Fail：<font color="red">{}</font></b><br/>
                <br/>
                <table class="mailTable"  border="1" cellspacing="0">
                <tr>
                <th>模块</th><th>用例数</th><th>Pass</th><th>Fail</th>
                </tr>
                <tr>
                <td>后端性能</td><td>{}</td><td>{}</td><td><font color="red"><b>{}</b></font></td>
                </tr>
                <tr>
                <td>前端性能</td><td>{}</td><td>{}</td><td><font color="red"><b>{}</b></font></td>
                </tr>
                </table>
        </body>
        """.format(*result)
        content = "<!DOCTYPE html><html>" + head + body + "</html>"
        return content

    def send_mail(self, subject, content):
        # 1.实例化SMTP
        smtp = smtplib.SMTP(self.mail_info['host'], port=587)
        # 2. 链接邮件服务器 eg:163邮箱: smtp.163.com
        # smtp.connect(self.mail_info['host'])
        smtp.connect(self.mail_info['host'], port=587)
        smtp.starttls()
        # 3. 配置发送邮箱的用户名和密码
        smtp.login(self.mail_info['from_user'], self.mail_info['from_pwd'])
        # 4. 配置发送内容msg
        msg = MIMEText(content, 'html', _charset='utf-8')
        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = self.mail_info['from_user']
        msg['To'] = ",".join(self.mail_info['to_user'].split(","))
        msg['Cc'] = ",".join(self.mail_info['cc_user'].split(","))
        # 5. 配置发送邮箱，接收邮箱，以及发送内容
        smtp.sendmail(self.mail_info['from_user'], self.mail_info['to_user'] + ',' + self.mail_info['cc_user'],
                      msg.as_string())
        # 6. 关闭邮件服务
        smtp.quit()

    def send_mail_attach(self, subject, content):
        # 1.实例化SMTP
        smtp = smtplib.SMTP_SSL(host=self.mail_info['host'])
        # 2. 链接邮件服务器 eg:163邮箱: smtp.163.com qq:smtp.qq.com port=465
        smtp.connect(host=self.mail_info['host'])
        # 3. 配置发送邮箱的用户名和密码
        smtp.login(self.mail_info['from_user'], self.mail_info['from_pwd'])
        # 4. 添加附件
        # with open((self.mail_info['attachment_path'] + self.mail_info['attachment']), 'rb') as m:
        #     send_file = m.read()
        send_file = self.mail_info['attachment_path'] + self.mail_info['attachment']
        att = MIMEText(send_file, 'base64', 'utf-8')
        att["Content-Type"] = 'application/actet-stream'
        att["Content-Disposition"] = 'attachment;filename = %s' % (self.mail_info['attachment'])
        # 4. 配置发送内容msg
        msg_content = MIMEText(content, 'html', _charset='utf-8')
        msg = MIMEMultipart('mixed')  # alternative:纯文本 related:内嵌资源 mixed:附件
        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = self.mail_info['from_user']
        msg['To'] = ",".join(self.mail_info['to_user'])
        msg['Cc'] = ",".join(self.mail_info['cc_user'])
        msg.attach(att)  # 添加附件、文本、图片都可以用attach
        msg.attach(msg_content)
        # 5. 配置发送邮箱，接收邮箱，以及发送内容
        smtp.sendmail(self.mail_info['from_user'], self.mail_info['to_user'], msg.as_string())
        # 6. 关闭邮件服务
        smtp.quit()

    @staticmethod
    def _send_mail(smtp_host, from_account, from_password, to_account, cc_account, subject, content):
        # 邮件发送
        # 1.实例化SMTP
        smtp = smtplib.SMTP_SSL(host=smtp_host)
        # 2. 链接邮件服务器 eg:163邮箱: smtp.163.com
        smtp.connect(host=smtp_host, port=465)
        # smtp.ehlo()  # 向邮箱发送SMTP 'ehlo' 命令
        # smtp.starttls()
        # 3. 配置发送邮箱的用户名和密码
        smtp.login(from_account, from_password)
        # 4. 配置发送内容msg
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = from_account
        msg['To'] = to_account
        msg['Cc'] = cc_account
        # 5. 配置发送邮箱，接收邮箱，以及发送内容
        smtp.sendmail(from_account, to_account, msg.as_string())
        # 6. 关闭邮件服务
        smtp.quit()


if __name__ == '__main__':
    mail_info = {
        "host": "smtp.partner.outlook.cn",
        "from_user": "wei.yang@cyclone-robotics.com",
        "from_pwd": "N!WizZ5KE&",
        "to_user": "wei.yang@cyclone-robotics.com",
        "cc_user": "wei.yang@cyclone-robotics.com",
        # "to_user": ["xiaotong.zhang@cyclone-robotics.com"],
        # "cc_user": ["dongkan.tao@cyclone-robotics.com"],
        "attachment_path": "",
        "attachment": "",
    }
    c = SendEmail(mail_info)
    import glob
    report_file = glob.glob('D:\\Code\\python_project\\interface_scenes_test\\report\\performance_test_report.html')[0]
    print(report_file)
    f = open(report_file, 'r', encoding='utf-8')
    html_mail = f.read()
    f.close()
    c.send_mail("RPA平台-九宫格Daily Build非功能自动化测试报告", html_mail)
