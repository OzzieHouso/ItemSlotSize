# ItemSlotSize
A Python script to scan DayZ game files and extract all item size definitions from config.bin files. I made this because I was sick of digging through dozens of config files to find item dimensions.

# What it does
This tool crawls through every config.bin file in your DayZ P-drive and pulls out every single itemSize definition. It collects:
- Item class names
- Size dimensions (width x height)
- Total inventory slots used
- Location of the definition in the file structure

Since BI has this stuff scattered across HUNDREDS of files, this tool saves a ton of time.

# Requirements
- Python 3.6+
- DayZ game files mounted to P:\DZ
- DayZ Tools
- Basic knowledge of how to run a Python script

# How to use it
- Make sure your DayZ files are mounted at P:\DZ (change the path in the script if yours is different)

Run the script
```
python scan_configs.py
```

Wait while it scans everything (there are a LOT of files)
Check the output files:

 - `dayz_all_item_sizes.txt` - Complete list with all details
 - `dayz_all_item_sizes.csv` - Same data in CSV format for Excel (in my case a database)
 - `dayz_item_sizes_by_slot.txt` - Items grouped by how many slots they take up

Output will look like this

```
--------------------------------------------------
Class: AugShort
Size: 6,3
SlotSizeTotal: 6x3 (18 Slots)
Path: P:\DZ\weapons\firearms\aug\config.bin
--------------------------------------------------
Class: FAMAS
Size: 6,3
SlotSizeTotal: 6x3 (18 Slots)
Path: P:\DZ\weapons\firearms\famas\config.bin
--------------------------------------------------
```


# Troubleshooting
If the script can't read the binary config files (which most likely, wont be able to do... ), use the included conversion script first:
`python CfgConvert.py`

This will use DayZ Tools' CfgConvert.exe to convert all the binary configs to readable text. Make sure you have DayZ Tools installed from Steam!

# Known issues
- Some config.bin files might have weird encoding that breaks the parser
- Class names might not always be detected correctly if the file structure is non-standard
- If you find any other issues, submit them to the repo or just fix the script yourself

# License
Do whatever you want with it. Credit is nice but not required.

_Note: This is not affiliated with or endorsed by Bohemia Interactive. I just got tired of manually searching through config files, for slotsizes_
