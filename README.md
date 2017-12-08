# README #

This pulls radio station playlists from onlineradiobox.com and generates a list of youtube urls and bookmarks that you can import into Chrome/Firefox and play using e.g. http://github.com/patraulea/youtube-bookmarks-player .

### Requirements ###

* Python 3
* BeautifulSoup 4
* Linux (tested on Ubuntu, should be trivial to port to Windows)

### Quick setup ###

* Run scrape.py once every few days to get the tracks
* Run export.py to generate bookmarks for your browser
