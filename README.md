# Tab collector
An script for managing open tabs.

If you are a person like me that allwayes many of your tabs are open you need this, Trust me.
This program is a tab collector that collect all of your tabs in a HTML file with a simple style that you can manage all of your tabs just in one page.

This script needs **Python 3** and tested on **Linux Mint OS** and optimized for **Mozilla**.

### requirements:
 - Linux
 - Python3
 - reqirments.txt
 - Apache server
 
 ## Usage:
*For using this script you should go through steps:*
  
`pip3 install -r requirments.txt`

`python3 tab-collector.py YOUR_PATH/tabs.html`
 
For activating **Delete** button you need **Apache** web server because delete button works with CGI.
For that:
1 - Installing apache and configure it:
   
   `sudo apt-get install apache2`
 
2 - Go to below path and findout *cgi-bin directory*:
   
   `cat etc/apache2/conf-available/serve-cgi-bin.conf | less`
   
   
   My CGI directory was in:
   
   `/usr/lib/cgi-bin`
   
   Type this commands:
   
   `cd etc/apache2/mods-enabled`
   
   `sudo ln -s ../mods-available/cgi.load`
   
   `sudo service apache2 reload`
   
Move **tabs.html** file to `/var/www/html` move **linkrm.py** to `/var/lib/cgi-bin` then open your terminal in cgi-bin directory and type:
   
   `sudo chmod -R 777 ./cgi-bin`
   
   `service apache2 start`

Open your browser and type `127.0.0.1/tabs.html`

Now you can use it, if it's hard for you to rerun the **tab-collector.py** you can use cron job. 

### Possible Issues:
If you have **Unicode ERROR** probably you can solve it like that:
1 - Add `PassEnv LANG` to the end of `/etc/apache2/apache2.conf` or `htaccess`.
2 - Uncomment `./etc/default/apache2/envvcars`
3 - Make sure line similar to `LANG="en_US.UTF-8"` in present in `/etc/default/locale`.
