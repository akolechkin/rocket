#!/usr/bin/env python

import logging
import sys
import rocket
import re

from json import loads as json_decode
from json import dumps as json_encode

#########################################
# Namespace management functions ########
#########################################

def gen_ns_pair_default(ns):
    """A namespace pair represents the name of the object a programmer
    interacts with (first part) and a titled version of that name for
    use with object creation.

        rocket.(first part).function()
    """
    return (ns.lower(), ns.title())

default_multi_delims=['\/', '\.', ':']
def gen_ns_pair_multi_delim(ns, delims=default_multi_delims):
    """Similar to gen_ns_pair_default but allows a '/' or '.' in the
    namespace field. If any of the split segments consist entirely of
    upper case letters, they stay upper case. They are title()'d otherwise
    to create a usual looking object name.

    SMS/Messages => ('SMSMessages', 'SMSMessages')
      or
    user/noted   => ('usernoted', 'UserNoted')
      or
    user/profile.get => ('userprofileget', 'UserProfileGet')

    returns ('dynamic function name', 'dynamic class name')
    """
    def title_if_lower(nnss):
        if not nnss.isupper():
            return nnss.title()
        return nnss

    groups = re.split('|'.join(delims), ns)
    ns_fun = ''.join(groups)
    ns_title = ''.join([title_if_lower(g) for g in groups])
    return (ns_fun, ns_title)

default_ns_var_pattern = '{(\w+)}'
def gen_ns_pair_multi_vars(ns, delims=default_multi_delims,
                           var_pattern=default_ns_var_pattern):
    """Similar to gen_ns_multi_delim but allows the use of variables
    in namespaces for use in URL generation. The generated names replace
    the variable with an underscore '_'.

    artists/{artist_id}/calendar => ('artists_calendar', 'Artists_Calendar')

    It will handle multiple variables fine too.

    a/{b}/c/{d}/e/{f}/g => a_c_e_g
    """
    (ns_fun, ns_title) = gen_ns_pair_multi_delim(ns, delims=delims)
    p = re.compile(var_pattern)
    ns_fun = p.sub('_', ns_fun)
    ns_title = p.sub('_', ns_title)
    return (ns_fun, ns_title)

def fill_ns_multi_vars(rocket, ns, args, ns_var_pattern=default_ns_var_pattern):
    """Helper function for filling in the variables in the namespace
    as found by gen_ns_pair_multi_vars.

    Removes the arguments matched in ns from args.
    """
    ns = rocket.namespace_map[ns]
    var_matches = re.findall(ns_var_pattern, ns)
        
    for m in var_matches:
        var_value = args[m]
        del args[m]
        ns = re.sub(ns_var_pattern, var_value, ns, 1)

    return ns


########################################
# Proxy functions ######################
########################################

class Proxy(object):
    """Represents a namespace of API calls."""

    def __init__(self, client, name, gen_namespace_pair=gen_ns_pair_default):
        self._client = client
        self._name = name
        self.gen_namespace_pair = gen_namespace_pair

    def __call__(self, method=None, args=None, add_session_args=True):
        # for Django templates, if this object is called without any arguments
        # return the object itself
        if method is None:
            return self

        return self._client('%s.%s' % (self._name, method), args)

    
def generate_proxies(function_list, doc_fun=None, 
                     gen_namespace_pair=gen_ns_pair_default,
                     logger=logging.getLogger()):
    """Helper function for compiling function_list into runnable code.
    Run immediately after definition.
    """
    logger.debug("Creating rockets %s \n" % function_list )

    proxies = {}
    
    for namespace in function_list:
        methods = {}

        for method in function_list[namespace]:
            params = ['self']
            body = ['args = {}']

            method_params = function_list[namespace][method]
            for param_name, param_type, param_options in method_params:
                param = param_name

                for option in param_options:
                    if isinstance(option, tuple) and option[0] == 'default':
                        if param_type == list:
                            param = '%s=None' % param_name
                            body.append('if %s is None: %s = %s'
                                        % (param_name,
                                           param_name,
                                           repr(option[1])))
                        else:
                            param = '%s=%s' % (param_name, repr(option[1]))

                # We jsonify the argument if it's a list or a dict. 
                if param_type == rocket.json:
                    body.append('if isinstance(%s, list) or isinstance(%s, dict): %s = json_encode(%s)'
                                % ((param_name,) * 4))

                # Optional variables default to None
                if 'optional' in param_options:
                    param = '%s=None' % param_name
                    body.append('if %s is not None: args[\'%s\'] = %s'
                                % (param_name,
                                   param_name,
                                   param_name))
                else:
                    body.append('args[\'%s\'] = %s' % (param_name,
                                                       param_name))

                params.append(param)

            # simple docstring to refer them to web docs for their API
            if doc_fun:
                body.insert(0, doc_fun(namespace, method))
            body.insert(0, 'def %s(%s):' % (method, ', '.join(params)))
            body.append('return self(\'%s\', args)' % method)
            exec('\n    '.join(body))
            methods[method] = eval(method)

        (ns_name, ns_title) = gen_namespace_pair(namespace)

        proxy = type('%sProxy' % ns_title, (Proxy, ), methods)
        proxies[proxy.__name__] = proxy
    return proxies


