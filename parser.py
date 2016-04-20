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

    def get_config(self, key):
        if self.casesensitivekey:
            return self.configs[key]
        idxkey = None
        for configkey in self.configs.iterkeys():
            if configkey.lower() == key.lower():
                idxkey = configkey
                break
        if not idxkey:
            raise KeyError(key)
        return self.configs[idxkey]


    def get(self, configkey, *args):
        keys = configkey.split('/')
        key = keys.pop(0)
        if len(keys) == 0:
            try:
                return self.get_config(key)
            except KeyError as err:
                if not len(args):
                    raise err
                return args[0]
        config = self.get_config(key)
        return config.get('/'.join(keys))

    def iteritems(self):
        return self.configs.iteritems()

    def iterkeys(self):
        return self.configs.iterkeys()

    def itervalues(self):
        return self.configs.itervalues()

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
    CONFIGINKEY='config in'

    def __init__(self,
                 template,
                 name=None,
                 validator=None,
                 casesensitivekey=True):
        self.casesensitivekey = casesensitivekey
        self.name = name
        self.parser = {}
        self.configinkeys = []
        self.validator = validator or Validator()
        self._build(template)

    def _is_config_name(self, key):
        try:
            if not self.name:
                return False
            name = self.name.split('/')[-1]
            lowerkey = key.lower()
            return lowerkey.endswith('name') and lowerkey.startswith(name.lower())
        except IndexError:
            return False

    def _build(self, template):
        for key, val in template.iteritems():
            try:
                self.parser[key] = self.validator.get_validator(val)
                if val.strip().lower().startswith(self.CONFIGINKEY):
                    self.configinkeys.append(
                        key if self.casesensitivekey else key.lower()
                    )
            except AttributeError as err:
                if type(val) is not dict:
                    raise err
                name=key
                if self._is_config_name(key):
                    key = self.CONFIGNAMEKEY
                self.parser[key] = \
                    ConfigParser(
                        val,
                        name='%s/%s' % (self.name, name),
                        validator=self.validator,
                        casesensitivekey=self.casesensitivekey
                    )

    def _get_parser(self, key):
        if self.casesensitivekey:
            return self.parser[key]
        idxkey = None
        for k in self.parser.iterkeys():
            if k.lower() == key.lower():
                idxkey = k
                break
        if not idxkey:
            raise KeyError(key)
        return self.parser[idxkey]

    def _parse(self, configs, ignorekeys=[]):
        if not configs:
            return configs
        config = Config(casesensitivekey=self.casesensitivekey)
        for key, val in configs.iteritems():
            ignore = key if self.casesensitivekey else key.lower()
            if ignore in ignorekeys:
                continue
            try:
                parser = self._get_parser(key)
            except KeyError as err:
                try:
                    parser = self.parser[self.CONFIGNAMEKEY]
                except KeyError:
                    raise err
            if issubclass(type(parser), ConfigParser):
                subconfig = parser._parse(val, ignorekeys=ignorekeys)
                config.set_config(key, subconfig)
            else:
                config.set_config(key, None if val==None else parser(val))
        return config

    def get_keys(self):
        return self.parser.keys()

    def _get_list_of_configin_keys(self):
        configinkeys = self.configinkeys
        for key, value in self.parser.iteritems():
            if issubclass(type(value), ConfigParser):
                configinkeys = configinkeys + value._get_list_of_configin_keys()
        return configinkeys

    def _process_parent_configs(self, rootconfig, configs):
        configinkeys = self._get_list_of_configin_keys()
        for key, value in configs.iteritems():
            if issubclass(type(value), Config):
                self._process_parent_configs(rootconfig, value)
            if key.lower() in configinkeys:
                configs.set_config(key, rootconfig.get(value))

    def parse_configs(self, config_path, ignorekeys=[]):
        if not os.path.isfile(config_path):
            raise ValueError('%s is not a existing file.' % config_path)
        try:
            config_data = yaml.load(open(config_path, 'r').read())
        except yaml.parser.ParserError as err:
            raise TypeError('Supporting yaml format only.')
        if not self.casesensitivekey:
            ignorekeys = [key.lower() for key in ignorekeys]
        configs = self._parse(config_data, ignorekeys=ignorekeys)
        self._process_parent_configs(configs, configs)
        return configs

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
