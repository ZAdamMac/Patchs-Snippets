# Data Management Scripts Usage

###csvscrub.py
### Configuration
`csvscrub.cfg` is a text file in the cwd of the script, formatted thusly:
```INI
[$Header]
scrub: boolean
delete: true
scrubbed value: string
map: boolean
```
where:
- $HEADER is the name of a header in row one of the csv
- scrub determines whether or not to scrub the values in this column.
- scrubbed value is the strong with which to replace the original data.
- map is a boolean controlling Mapped Scrub Mode
- if delete is set, the whole column will be excised from the scrubbed record.

If Mapped Scrub Mode is `True` for a particular column, values under that column will be indexed and modified accodingly, replaced with the string `$HEADER-$INDEX`. `%s` in a scrubbed value string will be replaced with the value of a counter that advances each row parsed - a space must exist on either side of the symbol and only one such symbol may be provided

**A note on encoding**: by default, both input and output as the `locale.getpreferredencoding()` return - that is, the system default. Modify lines 10 and 11 accordingly if other values are needed. If you want to always use the defaults, set those values to None, or comment out the lines. 


#### Usage
Preconfigure the headers you want to modify into the config file, run the script, and enter the path to the file you wish to scrub.

#### Limitations
Header data is required in both the csv and the config file. If data for a given header is missing, it will be skipped.


### sqlizer.py
#### Configuration
None.

#### Usage
Follow the steps. Both the DB path and the source paths can be full paths (under UNIX, anyway.)

#### Limitations
- Minimal testing and error handling
- No capability to update DBs (suggest creating a backup as soon as complete)