#!/usr/bin/env python
#-*- coding: utf-8 -*-
from configbuilder.validator import Validator
from configbuilder.parser import create_parser
import pprint

class MyValidator(Validator):
    def validate_protocol(self, value):
        """ Add validator method for type "Protocol"
        "Protocol" is a sub type of string.
        """
        supporting_protocol = ['ssh', 'ftp'] 
        return self._validate_choiceses(value, supporting_protocol)

if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4)
    parser = create_parser('./example_config_template.yaml',
                          validator=MyValidator(), 
                          casesensitivekey=False)
    cfg = parser.parse_configs('./example_user_config.yaml')
    print parser.get_keys()
    print cfg.get('datadir')
    print cfg.get('nodelist/node1/ip')
    node1cfg = cfg.get('nodelist/node1')
    print node1cfg.get('ip')
    print cfg.get('tags')
    pp.pprint(cfg.dump())
