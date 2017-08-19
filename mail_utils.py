import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from settings import kerberos_id, kerberos_pwd, mail_server, mail_port
kerberos_id = 'tt1140895'
kerberos_pwd = 'kerberos@2743'


class MailUtils(object):
    """docstring for MailUtils"""
    def __init__(self):
        super(MailUtils, self).__init__()       
        self.server = smtplib.SMTP(mail_server, mail_port)
        self.server.ehlo()
        self.server.starttls()
        self.server.login(kerberos_id, kerberos_pwd)
        
    def send_mail(self,fromaddrs, toaddrs, params):        
        msg_string = self._build(params).as_string()        
        self.server.sendmail(fromaddrs, toaddrs, msg_string)        
    def _build (self,params):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = params['subject']
        msg['From'] = params['from']
        msg['To'] = str(params['to'])
        if params.get('html', None):
            msg.attach(MIMEText(params['html'], 'html'))
        return msg

    def quit(self):
        self.server.quit()
        