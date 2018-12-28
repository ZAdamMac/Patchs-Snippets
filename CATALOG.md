# Patch's Toolbox
*Catalogue of Scripts*
*For usage and handling see each category's `USAGE.md`*

### Data Management Scripts
- `cvscrub.py` configurably scrubs csv files, including preserving data structures.
- `sqlizer.py` reads in csv files you point it at and feeds them into an sql db. Interactive.

### Pentesting Scripts
- `bruteRoots.py` enumerates the directories available immediately below a target URL. Relies on an external wordlist.
- `enumerate.py` a helper script for the enumpi project. When run, it will do a quick nmap scan of a target subnet/network range, determine which hosts are up, and use that information to provide some preliminary information (open TCP, top 100 UDP, and a basic directory enumeration against port 80). The information is provided as bundled packages for convenient download.
- `printf_manip.py` generates strings programatically based on certain input values, then uses those strings to do Format String Attacks against a binary. If used correctly this can result in privlege escalation. Ideally, this results in a root shell.