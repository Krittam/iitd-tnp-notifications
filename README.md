# iitd-tnp-notifications
This project has been made to keep IIT Delhi students informed about any updates on T&amp;P portal. It runs as a daemon on the user's account on IITD CSC machine. It checks the Companies on Campus page and notifications page at regular intervals and sends an email to the user in case the pages have been updated.

## Getting Started

These instructions will help you get a copy of the project up and running.

### Prerequisites

The project has been designed to only use packages or services already provided by CSC. So actually there are no prerequisites !!

### Deployment


Clone the repository on your local machine.
```
git clone https://github.com/Krittam/iitd-tnp-notifications.git
cd iitd-tnp-notifications
```
You need to create a file settings.py in the project root directory to store your personal details. You can use vim or any other tool to create the file with following details.

```

entry_no = 'your_entry_no'
tnp_pwd = 'your_tnp_password'
kerberos_id = 'your_kerberos_id'
kerberos_pwd = 'your_kerberos_password'

from_mail = 'tnpnotifications@gmail.com'
to_mail = 'username@anymail.com'
sleep_time = sleep_time_in_seconds
noti_url = 'Notification_page_url'
login_url = "training/placement_login_link"
company_url = "training/placement_companies_on_campus_link"
```
Now you need to transfer these files on your account on the CSC machine. This can be done using any file transfer tool based on FTP/SFTP/SSH

Once the project files are on your account access it using your favourite ssh client.
```
For linux users:
ssh kerberos_id@ssh1.iitd.ac.in
Enter your password
```
You should now find yourself logged in to the machine. 
You are good to go now !!
Navigate to the project directory.
You can now deploy the daemons by running
```
python notifications_sync.py
```
and
```
python companies_sync.py
```
But in order to keep the daemons running even after the ssh session is closed you need to run them as tmux sessions.
```
tmux new -s tnp-notifications
python notifications_sync.py
```
Open another terminal window
```
tmux new -s tnp-notifications
python companies_sync.py
```

You can now safely close the terminal (ignore any possible warnings) without worrying about missing any important notification ever !
