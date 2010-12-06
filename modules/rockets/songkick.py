#! /usr/bin/env python

from r_songkick import Songkick

if __name__ == '__main__':
    api_key = ''
    songkick = Songkick(api_key=api_key)

    # bonobo
    artist_id = '258948'
    response = songkick.artists_calendar.get(artist_id=artist_id, per_page=1)
    print response

    # bonobo, by music brainz id
    music_brainz_id = '9a709693-b4f8-4da9-8cc1-038c911a61be'
    response = songkick.artistsmbid_calendar.get(music_brainz_id=music_brainz_id, per_page=1)
    print response
    
