#! /usr/bin/env python

from r_songkick import Songkick

if __name__ == '__main__':
    api_key = ''
    songkick = Songkick(api_key=api_key)

    artist_id = '258948' # bonobo
    response = songkick.artists_calendar.get(artist_id=artist_id, per_page=1)
    print response

    music_brainz_id = '9a709693-b4f8-4da9-8cc1-038c911a61be' # bonobo, by music brainz id
    response = songkick.artistsmbid_calendar.get(music_brainz_id=music_brainz_id, per_page=1)
    print response

    min_date = "2010-12-01"
    max_date = "2010-12-31"
    response = songkick.events.get(min_date=min_date, max_date=max_date)
    print response

    event_id = "5725306" # a tool show
    response = songkick.events_setlists.get(event_id)
    print response
