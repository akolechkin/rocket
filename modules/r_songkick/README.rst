r_songkick
=============

r_songkick is a Python library for interfacing with the `Songkick API
<http://www.songkick.com/developer>`_

r_songkick is licensed under the `Apache Licence, Version 2.0 <http://www.apache.org/licenses/LICENSE-2.0.html>`_


Using
-----

r_songkick is a complete implementation of songkick's API.

::

    from r_songkick import Songkick

    api_key = ''
    songkick = Songkick(api_key=api_key)

    artist_name = 'Bonobo'
    response = songkick.events.get(artist_name=artist_name)

    music_brainz_id = '9a709693-b4f8-4da9-8cc1-038c911a61be'
    response = songkick.artistsmbid_calendar.get(artist_name=artist_name,
                                                 per_page=1)

See example.py for more.

Install
-------

::

    python ./setup.py install

r_songkick depends on Rocket being installed.
http://github.com/exfm/rocket

pip / easy_install support on the way

James Dennis <james@extension.fm>
