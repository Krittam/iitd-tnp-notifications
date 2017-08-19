import requests
import hashlib
import os
from bs4 import BeautifulSoup
from mail_utils import MailUtils
from settings import from_mail, to_mail
hash_file_name = 'hash_notification'

noti_url = 'http://tnp.iitd.ac.in/notices/notify.php'
page = requests.get(noti_url, verify=False)
soup = BeautifulSoup(page.content,'html.parser')
mail_params = {'subject': 'You might have new TnP notifications !','from':from_mail,'to':to_mail}
hash_str = hashlib.sha256(page.text.encode('utf-8')).hexdigest()
if not os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)),hash_file_name)):
    open(hash_file_name, 'w+').close()

with open (hash_file_name,'r+') as hash_file:
    content = hash_file.read()
    print(content)
    print(hash_str)
    if content != hash_str:
        hash_file.seek(0)
        hash_file.write(hash_str)
        hash_file.truncate()
        mail_params['html'] = str(soup)
        mailer = MailUtils()
        mailer.send_mail(from_mail,to_mail,mail_params)
        mailer.quit()
    else:
        print('no changes detected!')