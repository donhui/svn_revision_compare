# Svn revision compare
Consistency check between svn server and backup severs.

Compare the revisions between svn server and backup severs, and send email notification.

# PreRequire tools
- Python2.7 or Python3
- svn cli
  
# About svn auth
svn username and password should be added to svn cli option for auth. 
in addition，update `～/.subversion/servers` file as follows:
```
store-passwords = yes
store-plaintext-passwords = yes
```

# How to run
- modify configuration parameter of `settings.py`
- execute script： `svn_revision_compare.py`

# Email demo screenshot

![Email demo screenshot](./images/email_demo_screenshot.png)