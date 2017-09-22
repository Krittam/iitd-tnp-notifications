import sys
import requests
import hashlib
import os
import time
from mail_utils import MailUtils
from company_parser import CompanyParser
from settings import from_mail, to_mail, sleep_time, company_url, tnp_pwd, entry_no, login_url
hash_file_name = 'hash_company'

while True:
    mailer = None
    session = None
    try:
        mailer = MailUtils()        
        mail_params = {'subject': 'You might have new Companies on TnP portal !','from':from_mail,'to':to_mail}
        
        session = requests.Session()
        payload = {'username': entry_no, 'password': tnp_pwd, 'login': 'Submit'}
        response = session.post(login_url, data=payload, verify=False)

        page = session.get(company_url, verify=False)
        
        parser = CompanyParser()
        parser.feed(page.text)
        companies = parser.get_companies()
        hash_str = hashlib.sha256(str(companies).encode('utf-8')).hexdigest()
        if not os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)),hash_file_name)):
            open(hash_file_name, 'w+').close()

        with open (hash_file_name,'r+') as hash_file:
            content = hash_file.read()
            if content != hash_str:
                print('changes detected!')
                hash_file.seek(0)
                hash_file.write(hash_str)
                hash_file.truncate()                      
                mail_params['html'] = str(page.content)
                mailer.send_mail(from_mail,to_mail,mail_params)
                print('notification mail sent!')
                mailer.quit()
            else:               
                print('no changes detected!')
        session.close()
    except Exception as e:
        log =''
        if e.message :
            log = e.message
        log +=str(sys.exc_info()[0])
        print("Exception occured{}".format(log))
        if mailer :
            mail_params['subject'] = 'TnP company sync script crashed !'
            mail_params['body'] = 'Unfortunately your TnP Company sync script crashed !\nHere is the exception traceback\n{}'.format(log)
            mailer.send_mail(from_mail,to_mail,mail_params)
        if session:
            session.close()
    time.sleep(sleep_time)

