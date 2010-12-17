#! /usr/bin/env python

from r_songkick import Songkick

if __name__ == '__main__':
    api_key = ''
    songkick = Songkick(api_key=api_key)

    # look for bonobo shows 
    # (I got the artist id from : http://www.songkick.com/artists/258948-bonobo)
    artist_id = '258948'
    response = songkick.artists_calendar.get(artist_id, per_page=1)

    # bonobo, by music brainz id
    music_brainz_id = '9a709693-b4f8-4da9-8cc1-038c911a61be'
    response = songkick.artistsmbid_calendar.get(music_brainz_id, per_page=1)

    # fetch my calendar
    username = 'j2.d2'
    response = songkick.users_events.get(username)

    # look for shows in dec 2010
    min_date = "2010-12-01"
    max_date = "2010-12-31"
    response = songkick.events.get(min_date=min_date, max_date=max_date)

    # get the set list for a tool show
    event_id = "5725306"
    response = songkick.events_setlists.get(event_id)
