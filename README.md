<div align="center">
  
# PyInstaLive
## Download Instagram Livestreams as Videos

![github stars badge](https://badgen.net/github/stars/samuelchristlie/PyInstaLive?icon=github)
![github forks badge](https://badgen.net/github/forks/samuelchristlie/PyInstaLive?icon=github)
![github issues badge](https://badgen.net/github/open-issues/samuelchristlie/PyInstaLive?icon=github)

This is a fork of [PyInstaLive](https://github.com/dvingerh/PyInstaLive). Please visit the repository for full installation and guide.

</div>

## ▶ Usage
To load JSON cookies to **PyInstaLive**, create a `username.txt` file containing the Netscape-formatted cookies, e.g.
```
# Netscape HTTP Cookie File

.instagram.com	TRUE	/	TRUE	1758082584	mid	xxx
.instagram.com	TRUE	/	TRUE	1758082585	datr	xxx
.instagram.com	TRUE	/	TRUE	1755058602	ig_did	xxx
.instagram.com	TRUE	/	TRUE	1755058602	ig_nrcb	xxx
.instagram.com	TRUE	/	TRUE	1755058690	sessionid	xxx
.instagram.com	TRUE	/	TRUE	1724127492	shbid	xxx
.instagram.com	TRUE	/	TRUE	1724127492	shbts	xxx
.instagram.com	TRUE	/	TRUE	1724127494	wd	xxx
.instagram.com	TRUE	/	TRUE	1754973655	csrftoken	xxx
.instagram.com	TRUE	/	TRUE	0	rur	xxx
.instagram.com	TRUE	/	TRUE	1731300055	ds_user_id	xxx
```
You can also specify custom paths for session and cookies files in `config.ini`
```
[pyinstalive]
username = johndoe
password = grapefruits
session_file = ../sessions/johndoe.dat
cookies_file = ../cookies/johndoe.txt
download_path = {:s}
download_comments = True
clear_temp_files = True
cmd_on_started =
cmd_on_ended =
ffmpeg_path = 
log_to_file = True
no_assemble = False
use_locks = True
send_heartbeat = True
proxy =
```
