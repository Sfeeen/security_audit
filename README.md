# security_audit
A simple method/demo to show the consequences of a targeted attack on a Windows user.

An e-mail is send to the target with a malicious .exe. stored wifi passwords are mailed to the attacker, a reverse shell is established and the target will be rickerolled every time he/she reboots their pc.


## Steps
* Build a malicious .exe, `main.py` is a python scrip made with Pyqt5. As soon as you start the script the following happens:
    * `script.bat` is copied to the startupfolder of the target. This will result in a rickroll video being started every time you reboot your pc. The bat file was copied from [Maurice Norden](https://github.com/MauriceNorden/rick-roll "MauriceNorden").
    Note that you can also put a bat file here that opens a reverse shell in order the make the attack persistant.
    * All stored wifi passwords are fetched and send to the attacker by email. `mailsender.py` can be configured to send the mail.
    * A reverse shell is opened to an IP:PORT of your chose. Make sure your port is forwarded to the correct internal ip.
    
  A simple GUI is made using QtDesigner. It just has a trustworthy name and icon, my gui will do nothing but you can give it legit fucntionality.
  To build the .exe run:
  `pyinstaller.exe --onefile --icon="assets/drivepng.ico" main.py --add-data "assets/;assets"`
 * Send a trustworthy email 
    An email can be send impersonating someone from within the company using online tools e.g. <https://emkei.cz/>. 
    An attacker could first mail the company to obtain their email html template and than use it with the above email sender to be more trustworthy.
    Attach the .exe
    
    
 * Receive the incoming shell
  I have written a simple script on my raspberry pi that receives the reverse shells and logs the path of the user that is connected. You can also manually listen for shells using:
  `nc –lvp 4444` (change 4444 to your chosen port).
