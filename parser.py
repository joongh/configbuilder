#!/usr/bin/env python
#-*- coding: utf-8 -*-
import yaml
import os
from validator import Validator

class Config(object):
    def __init__(self, casesensitivekey=True):
        self.configs = {}
        self.casesensitivekey = casesensitivekey

    def set_config(self, key, value):
        self.configs[key] = value

    def get(self, configkey):
        keys = configkey.split('/')
        key = keys.pop(0) if self.casesensitivekey else keys.pop(0).lower()
        if len(keys) == 0:
            return self.configs[key]
        config = self.configs[key]
        return config.get('/'.join(keys))

    def dump(self):
        dumpdata = {}
        for key, val in self.configs.iteritems():
            if type(val) is Config:
                dumpdata[key] = val.dump()
            else:
                dumpdata[key] = val
        return dumpdata

class ConfigParser(object):
    CONFIGNAMEKEY='_confignamekey'

    def __init__(self, 
                 template, 
                 name=None,
                 validator=None,
                 casesensitivekey=True):
        self.casesensitivekey = casesensitivekey
        self.name = name
        self.parser = {}
        self.validator = validator or Validator()
        self._build(template)

    def _is_config_name(self, key):
        try:
            return self.name and key[len(self.name):].lower() == 'name'
        except IndexError:
            return False

    def _build(self, template):
        for key, val in template.iteritems():
            if not self.casesensitivekey:
                key = key.lower()
            try:
                self.parser[key] = self.validator.get_validator(val)
            except AttributeError as err:
                if type(val) is not dict:
                    raise err
                name=key
                if self._is_config_name(key):
                    key = self.CONFIGNAMEKEY
                self.parser[key] = \
                    ConfigParser(
                        val,
                        name=name,
                        validator=self.validator,
                        casesensitivekey=self.casesensitivekey
                    )

    def _parse(self, configs):
        if not configs:
            return configs
        config = Config(casesensitivekey=self.casesensitivekey)
        for key, val in configs.iteritems():
            key = key if self.casesensitivekey else key.lower()
            try:
                parser = self.parser[key]
            except KeyError as err:
                try:
                    parser = self.parser[self.CONFIGNAMEKEY]
                except KeyError:
                    raise err
            if issubclass(type(parser), ConfigParser):
                subconfig = parser._parse(val)
                config.set_config(key, subconfig)
            else:
                config.set_config(key, None if not val else parser(val))
        return config

    def get_keys(self):
        return self.parser.keys()

    def parse_configs(self, config_path):
        if not os.path.isfile(config_path):
            raise ValueError('%s is not a existing file.' % config_path)
        try:
            config_data = yaml.load(open(config_path, 'r').read())
        except yaml.parser.ParserError as err:
            raise TypeError('Supporting yaml format only.')
        return self._parse(config_data)

def create_parser(template_path, 
                  validator=Validator(),
                  casesensitivekey=False):
    if not os.path.isfile(template_path):
        raise ValueError('Load template with template file.')
    try:
        template_data = yaml.load(open(template_path, 'r').read())
    except yaml.parser.ParserError as err:
        raise TypeError('Supporting yaml format only.')
    return ConfigParser(template_data, 
                        validator=validator, 
                        casesensitivekey=casesensitivekey)

