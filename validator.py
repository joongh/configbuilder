#!/usr/bin/env python
#-*- coding: utf-8 -*-
import ast
import socket
import os

class Validator(object):
    def __init__(self):
        self.TYPE_PREFIX = {
            'list of': self.get_validate_list_of,
        }
   
    def get_validator(self, t):
        validator_name = 'validate_%s' % t.strip().lower()
        try:
            return getattr(self, validator_name)
        except AttributeError as err:
            for key, val in self.TYPE_PREFIX.iteritems():
                if t.lower().startswith(key):
                    return self.TYPE_PREFIX[key](t[len(key):].strip())
            raise err
        
    def get_validate_list_of(self, subtype):
        name = 'validate_list_of_%s' % subtype.strip().lower()
        validate_func = lambda v: self._validate_list_of(v, subtype)
        setattr(self, name, validate_func)
        return validate_func
        
    def validate_string(self, value):
        if not isinstance(value, basestring):
            raise ValueError('Value should be a string.')
        return value.strip()            

    def validate_boolean(self, value):
        if isinstance(value, basestring):
            value = ast.literal_eval(value)
        if type(value) is not bool:
            raise ValueError('Value should be a boolean.')
        return value
        
    def validate_integer(self, value):
        return int(value)
        
    def validate_ip(self, value):
        if not isinstance(value, basestring):
            raise ValueError('Value should be a IP address string.')
        try:
            socket.inet_pton(socket.AF_INET, value)
        except socket.error as err:
            raise ValueError(err.message)
        else:
            return value.strip()
    
    def validate_path(self, value):
        if not isinstance(value, basestring):
            raise ValueError('Value should be a path string.')
        return os.path.normpath(value)
        
    def validate_existingpath(self, value):
        value = self.validate_path(value)
        if not os.path.exists(value):
            raise ValueError('%s does not exist.' % value)
        return value
    
    def validate_filepath(self, value):
        value = self.validate_existingpath(value)
        if not os.path.isfile(value):
            raise ValueError('%s does not a file.' % value)
        return value
        
    def validate_directorypath(self, value):
        value = self.validate_existingpath(value)
        if not os.path.isdir(value):
            raise ValueError('%s does not a directory.' % value)
        return value
        
    def validate_list(self, value):
        if type(value) is not list:
            raise ValueError('Value should be a list')
        return value
        
    def _validate_list_of(self, value, subtype):
        subvalidator = self.get_validator(subtype)
        value = self.validate_list(value)
        return [subvalidator(v) for v in value]

    def _validate_choiceses(self, value, choices):
        value = self.validate_string(value)
        if value not in choices:
            raise ValueError('Value should be in %s' % choices)
        return value

