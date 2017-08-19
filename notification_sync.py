import requests
import hashlib
import os
import time
from mail_utils import MailUtils
from settings import from_mail, to_mail, sleep_time
hash_file_name = 'hash_notification'
noti_url = 'http://tnp.iitd.ac.in/notices/notify.php'
while True:
	mailer = MailUtils()
	try:
		page = requests.get(noti_url, verify=False)
		mail_params = {'subject': 'You might have new TnP notifications !','from':from_mail,'to':to_mail}
		hash_str = hashlib.sha256(page.text.encode('utf-8')).hexdigest()
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
	except Exception as e:
		print("Exception occured{}".format(e.message))
		mail_params['subject'] = 'TnP notification script crashed !'
		mail_params['body'] = 'Unfortunately your TnP notification script crashed !\nHere is the exception traceback\n{}'.format(e.message)
		mailer.send_mail(from_mail,to_mail,mail_params)	
	time.sleep(sleep_time)