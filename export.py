#!/usr/bin/env python3

from datetime import date, datetime, timedelta

import sys, os

from functools import partial
eprint = partial(print, file=sys.stderr)

station = 'ro/tananana'

work_dir = os.getenv('HOME') + '/radio/' + station

playlist_dir = os.path.join(work_dir, 'playlist')
tracks_fn = os.path.join(work_dir, 'tracks')

icon="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAABZklEQVQ4jcWRP0tbYRTGf+e915ggCgkIgiHYFBFL28VFP4CTuEh17IdwKJ2DYEsFEbW00M9RhbRLBCedBEVwci7JkJC8fe+f08Eo996EDB3aB57hnOf8ezjwvyHnUJDixDcRXUB5hUhuVIMqVyLqUL1ebvXeylmxsCuY93+zXYk/mFBlNURJMsqN8fzoC2PVKlktRZVVE0AlAJKM8nlKb7Z4/aNBcWOTrJ5gxTjVklNIsheDtRZnDM/2D5nbOyAcz5Otc6olPxDxhrnrdrtP0eTaOuUo4u7dduYF4vmB6mB7nB7Qur+n8fmY8pBa36lGZK5QFGstADenJ5zt7rDoLE4ks0kj/7dKU2A6lQ9juu02Pz995NfJd176Bg/BabZfmvJ1qnABLCWFCDh3IfO+x4zJbE3j0neqdSPpAQAruQdXIYO+HxErdT9o25o3mZ8FXvTzA8OeTkZvBen0g9NWx9ZGnfdv8AdZHLkn9K0FLQAAAABJRU5ErkJggg=="

known_tracks = {}


def get_day(day):
    global known_tracks

    dt = datetime.now() + timedelta(days=-day)
    fn = os.path.join(playlist_dir, dt.strftime('%Y-%m-%d'))

    if not os.path.exists(fn):
        return []
 
    ret = []

    with open(fn, 'r') as f:
        for line in f:
            track, title = line.strip().split(maxsplit=1)
            if track in known_tracks:
                yt = known_tracks[track]
                if yt != 'NOTFOUND':
                    ret.append((yt, title))
    
    return ret


def print_folder(tracks, name):
    global icon

    n = int(datetime.now().timestamp())

    print('<DT><H3 ADD_DATE="%d" LAST_MODIFIED="%d">%s</H3>' % (n, n, name))
    print('<DL><p>')

    for i in tracks:
        print('  <DT><A HREF="%s" ADD_DATE="%d" ICON="%s">%s</A>' % (i[0], n, icon, i[1]))
    
    print('</DL>')


if __name__ == "__main__":
    arg = (len(sys.argv) > 1) and sys.argv[1] or '1'

    if arg != 'week':
        try:
            i = int(arg)
        except:
            eprint("syntax: export.py [week]")
            sys.exit(1)

    with open(tracks_fn, 'r') as f:
        for line in f:
            track, youtube, title = line.strip().split(maxsplit=2)
            known_tracks[track] = youtube

    if arg == 'week':
        tracks = []
        for day in reversed(range(1,8)):
            tracks += get_day(day)

        print_folder(tracks, datetime.now().strftime('%Y-%m-%d week'))
    else:
        for day in reversed(range(1,1+int(arg))):
            tracks = get_day(day)

            dt = datetime.now() + timedelta(days=-day)
            print_folder(tracks, dt.strftime('%Y-%m-%d'))
