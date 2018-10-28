# coding: utf-8

from flask import Flask, jsonify, make_response
from flask._compat import string_types
from flask.app import setupmethod
from flask.helpers import _endpoint_from_view_func
from flask_babelex import Babel
from flask_compress import Compress
from werkzeug.routing import BaseConverter, Rule

from config import config
from flask_cors import CORS


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


class ServerFlask(Flask):
    def __init__(self, name, *args, **kwargs):
        super(ServerFlask, self).__init__(name, *args, **kwargs)
        self.config.from_mapping(config)

    def make_response(self, rv):
        if isinstance(rv, dict):
            if 'success' not in rv:
                rv['success'] = True
            if 'message' not in rv:
                rv['message'] = 'ok'
            rv = jsonify(rv)
        return super().make_response(rv)

    @setupmethod
    def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
        if endpoint is None:
            endpoint = _endpoint_from_view_func(view_func)
        options['endpoint'] = endpoint
        methods = options.pop('methods', None)

        # if the methods are not given and the view_func object knows its
        # methods we can use that instead.  If neither exists, we go with
        # a tuple of only ``GET`` as default.
        if methods is None:
            methods = getattr(view_func, 'methods', None) or ('GET',)
        if isinstance(methods, string_types):
            raise TypeError('Allowed methods have to be iterables of strings, '
                            'for example: @app.route(..., methods=["POST"])')
        methods = set(item.upper() for item in methods)

        # Methods that should always be added
        required_methods = set(getattr(view_func, 'required_methods', ()))

        # starting with Flask 0.8 the view_func object can disable and
        # force-enable the automatic options handling.
        provide_automatic_options = getattr(view_func,
                                            'provide_automatic_options', None)

        if provide_automatic_options is None:
            if 'OPTIONS' not in methods:
                provide_automatic_options = True
                required_methods.add('OPTIONS')
            else:
                provide_automatic_options = False

        # Add the required methods now.
        methods |= required_methods

        if not isinstance(rule, Rule):
            rule = self.url_rule_class(rule, methods=methods, **options)
            rule.provide_automatic_options = provide_automatic_options

        self.url_map.add(rule)
        if view_func is not None:
            old_func = self.view_functions.get(endpoint)
            if old_func is not None and old_func != view_func:
                raise AssertionError('View function mapping is overwriting an '
                                     'existing endpoint function: %s' % endpoint)
            self.view_functions[endpoint] = view_func


app = ServerFlask('server')

CORS(app, resources=r'/*')

app.url_map.converters['regex'] = RegexConverter

Babel(app, 'zh_CN')
Compress(app)
