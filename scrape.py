#!/usr/bin/env python3

from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta

import urllib3, time, sys, os, random

from functools import partial
eprint = partial(print, file=sys.stderr)

website = 'http://onlineradiobox.com'

station = 'ro/tananana'

work_dir = os.getenv('HOME') + '/radio/' + station

playlist_dir = os.path.join(work_dir, 'playlist')
tracks_fn = os.path.join(work_dir, 'tracks')

http_pool = urllib3.PoolManager()


def get_url(url):
    global http_pool

    req = http_pool.request('GET', url, headers = {
            'User-agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36',
            'Cookie': 'lang=en; cs=ro.radiozu|0; tz=-120; _ouid=55a1d707200646f3; country=ro'})
    return req.data


def delay():
    r = random.randint(4, 8)
    for i in reversed(range(r)):
        sys.stderr.write('\r%d... ' % i)
        sys.stderr.flush()
        time.sleep(1)

    sys.stderr.write('\r...  ')
    sys.stderr.flush()

    time.sleep(random.uniform(0, 1))

    sys.stderr.write('\r      \r')
    sys.stderr.flush()


def embed_to_watch(emb):
    prefix = 'https://www.youtube.com/embed/'
    if not emb.startswith(prefix):
        raise Exception('unsupported embed url: ' + emb)
    return 'https://www.youtube.com/watch?v=' + emb[len(prefix):]


def get_youtube_url(track):
    url = '%s%s' % (website, track)

    html = get_url(url)
    delay()

    soup = BeautifulSoup(html, 'html.parser')

    iframe = soup.find('iframe')
    return iframe and embed_to_watch(iframe['src']) or 'NOTFOUND'


def download_playlists():
    os.makedirs(playlist_dir, exist_ok=True)

    eprint('getting playlists')

    for day in range(7):
        dt = datetime.now() + timedelta(days=-day)
        fn = os.path.join(playlist_dir, dt.strftime('%Y-%m-%d'))
        
        #if os.path.exists(fn): # and day > 0:
        #    continue

        eprint(fn)
        
        url = '%s/%s/playlist/%s' % (website, station, (day and str(day) or ''))
        
        html = get_url(url)
        delay()

        soup = BeautifulSoup(html, 'html.parser')

        links = soup.find_all('a', href=True, attrs={'class': 'ajax'})

        tracks = [t for t in links if t['href'].startswith('/track/')]
        
        f = open(fn, 'w')
        
        eprint('found %d tracks' % len(tracks))

        for t in tracks:
            f.write('%s\t%s\n' % (t['href'], t.text.strip()))

        f.close()

def lookup_yt_urls():
    known_tracks = {}

    if os.path.exists(tracks_fn):
        with open(tracks_fn, 'r') as f:
            for line in f:
                track, youtube, title = line.strip().split(maxsplit=2)
                known_tracks[track] = youtube

    for fn in os.listdir(playlist_dir):
        if fn in ['..', '.']: continue

        abs_fn = playlist_dir + '/' + fn
        eprint('looking up youtube urls in', abs_fn)
        with open(abs_fn, 'r') as f:
            for line in f:
                track, title = line.strip().split(maxsplit=1)
                if track not in known_tracks:
                    eprint('requesting', track, title)
                    
                    yt_url = get_youtube_url(track)
                    known_tracks[track] = yt_url
        
                    with open(tracks_fn, 'a') as f:
                        f.write('%s\t%s\t%s\n' % (track, yt_url, title))
                    
                    eprint('    ', yt_url)


if __name__ == "__main__":
    download_playlists()
    lookup_yt_urls()
