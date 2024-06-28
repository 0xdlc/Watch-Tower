A tool that watches Hackerone and Bugcrowd programs for any Scope changes and Notifies the changes via discord.


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
- you need a mongodb server as well. (use atlas)


! WILL REFACTOR THE CODE TO CLASS BASED INSTEAD OF FUNCTION BASED FOR PERFORMANCE AND READABILITY
