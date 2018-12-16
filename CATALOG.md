# Patch's Toolbox
*Catalogue of Scripts*
*For usage and handling see each category's `USAGE.md`*

### Data Management Scripts
- `cvscrub.py` configurably scrubs csv files, including preserving data structures.
- `sqlizer.py` reads in csv files you point it at and feeds them into an sql db. Interactive.

### Pentesting Scripts
- `bruteRoots.py` enumerates the directories available immediately below a target URL. Relies on an external wordlist.
- `printf_manip.py` generates strings programatically based on certain input values, then uses those strings to do Format String Attacks against a binary. If used correctly this can result in privlege escalation. Ideally, this results in a root shell.