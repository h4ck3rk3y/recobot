#Recommendation BOT for DC++

Generates recommendations as per the filelists of users in the hub.

##Requirements
- mongodb
- python-recsys
- python2.7+

## Algorithm Implemented

Implements user-user based collaborative filtering where the items are the tth of the files shared. Extracts top 10 similar users to filter down on relevant results.

## Installation

- `pip install -r requirements.txt`

## Running instructions

- Configure recobot.py with your nick, hubname, ip address and password.
- You can add support for more file types by changing the supported_file_types list in recobot.py.
- Minimum file size has been set to 100 Mb, you can change that too on line 76.
- After you are done configuring try `python recobot.py`
- You will be asked if you want to download filelists of users before launch. Press y on first run.
- You will be prompted to build the recommendation file. Press y on first run.

## Acknowledgements
- [pydc-sheriffbot](https://github.com/kaustubh-karkare/pydc-sheriffbot/) by [Kaustubh Karkare](https://github.com/kaustubh-karkare)
- The above bot allowed us to connect with dc++ via python. Had to fix some bugs to get the code running.

## Built By
- [@shubh24](https://github.com/shubh24)
- [@h4ck3rk3y](https://github.com/h4ck3rk3y)

## ToDo
- Search Instant
- Search based recommendations
- Make installation easier.
- Make conifgurations easier.
- Caching results for a given day.
- Better README.md


### found a bug? create a pull request.
