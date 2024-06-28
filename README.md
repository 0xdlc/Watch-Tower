A tool that watches Hackerone and Bugcrowd for any Scope changes and sends a message to your discord. (via webhooks)
# subfinder


### Set permissions for bash files
```
python set_permissions.py
```

### Set the program on crontab or just manualy run:
```
python watcher.py -p "program1,program2,program3"
```
- Copy the Exact names from the bug-bounty platform
- Supported platform are: hackerone and bugcrowd
- you need a mongodb from atlas as well.
