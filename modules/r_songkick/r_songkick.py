#! /usr/bin/env python
#
# r_songkick - songkick API implemented with rocket


__doc__ = """Python bindings for the Songkick API
(r_songkick - courtesy of exfm)

For more information, see

Home Page: http://github.com/exfm/rocket/modules/r_songkick
Songkick API: http://www.songkick.com/developer
"""

import re
import rocket
from rocket.auth import sign_sorted_values
from rocket.proxies import gen_ns_pair_multi_vars as gen_namespace_pair
from rocket.proxies import default_ns_var_pattern
from rocket.proxies import fill_ns_multi_vars

########################################
# Settings #############################
########################################

VERSION = '0.1'

# %s to make room for basic_auth_string
API_URL = 'http://api.songkick.com/api/3.0'
API_URL_SECURE = None

API_DOCSTRING = '"""See songkick docs: http://www.songkick.com/developer"""'

def _get_api_docstring(namespace, function):
    """The songkick api docs 
    """
    return API_DOCSTRING 


########################################
# API implementation details ###########
########################################

# IDL for the API
FUNCTIONS = {
    'artists/{artist_id}/calendar': {
        'get': [
            ('artist_id', str, []),
            ('page', int, ['optional']),
            ('per_page', int, ['optional']),
        ],
    },
    'artists/mbid:{music_brainz_id}/calendar': {
        'get': [
            ('music_brainz_id', str, []),
            ('page', int, ['optional']),
            ('per_page', int, ['optional']),
        ],
    },
    'users/{username}/events': {
        'get': [
            ('username', str, []),
        ],
    },
    'events': {
        'get': [
            ('artist_name', str, ['optional']),
            ('location', str, ['optional']),
            ('min_date', str, ['optional']),
            ('max_date', str, ['optional']),
            ('page', int, ['optional']),
            ('per_page', int, ['optional']),
        ],
    },
    'events/{event_id}/setlists': {
        'get': [
            ('event_id', str, []),
        ],
    },
}


########################################
# API class implementation #############
########################################

class Songkick(rocket.Rocket):
    """Provides access to the Songkick API.

    Initialize with api_key 
    """
    def __init__(self, *args, **kwargs):
        super(Songkick, self).__init__(FUNCTIONS, client='songkick',
                                     api_url=API_URL,
                                     gen_namespace_pair=gen_namespace_pair,
                                     *args, **kwargs)

    def check_error(self, response):
        """Checks if the given API response is an error, and then raises
        the appropriate exception.
        """
        pass
    

    def gen_query_url(self, url, function, format=None, method=None, get_args=None):
        """Songkick urls sometimes have variables in them. Sometimes they don't.

        This is handled by using fill_ns_multi_vars.

        Example: http://api.songkick.com/api/3.0/artists/{artist_id}/calendar.json
        """
        function = fill_ns_multi_vars(self, function, get_args)

        query_url = '%s/%s' % (url, function)
        if format:
            query_url = '%s.%s' % (query_url, format)

        return query_url


    def build_query_args(self, method, args=None, signing_alg=None):
        """build_query_args is used to set the api_key in the request arguments
        as 'apikey'. That is songkick's convention.
        """
        args = self._expand_arguments(args)
        
        if self.api_key:
            args['apikey'] = self.api_key

        return args
