# configbuilder
General purpose configuration parser builder for python.
You can create your own configuration parser only with ```Configuration Template```

```configbuilder``` offers you the easiest way to define a configuration file for your
application project written in python.
 
## Synopsis
Data serialization language such as YAML or JSON is a good choice to write a
configuration files for a application. 
The code for parsing and validating the configuration file have to be re-written 
even for a simple change such as attribute name modification for new application. 
```configbuilder``` offers you an easy way to define a configuration file format with
minimum code changing. It is even possible to define a configuration format without
any developing codes. Instead of parsing code, you can define a configuration with
a template file written in data serialization language.  

## Usage
### Configuration Template
You can define the format of configuration format with writing a configuration template.
Loading the configuration template in your application code, you can simply parse a
user configuration file also with the validation.
This is the example of a configuration template written in YAML.

    ConfigKey1: String
    ConfigKey2: Boolean
    ConfigKey3: Integer
    ConfigKey4: IP
    ConfigKey5: FilePath
    ConfigKey6:
        ConfigKey6Name: # indicates the name of this subconfig
            SubConfigKey1: List of DirectoryPath 
            SubConfigKey2: String
            SubConfigKey3:
                SubConfigKey3Name:
                    SubSubConfigKey1: List of String
                    SubSubConfigKey2: Integer
                    SubSubConfigKey3: IP
                SubConfigKey3Name:
                    SubSubConfigKey4: Config In SubConfigKey3
    ConfigKey7:
        -   
            SubConfigKey1: String
            SubConfigKey2: Integer
            SubConfigKey3: NotSupportingType

An Attribute in configuration template consists of Key:Type pair. A key without a type 
intends that there is a sub-config for the key.
There are built-in types to validate values. The types are case-insensitive.

#### Built-in types
* String: Any type of string is accepted, and automatically strip the string.
* Boolean: True or False
* Integer: Integers
* IP: IP address
* Path: Any path regardless of the existence
* FilePath: Existing file path
* DirectoryPath: Existing directory path
* List: Any list regardless of the type of the item

#### Compound type
* List of ```Built-in type```: The value should be a list, and each item is 
validated with the specified built-in type.
* Config In ```Other Configuration Key```: The value is the name of other configuration.
This type converts value into the configuration instead of the given name.

### Build parser
Simple function ```create_parser``` let you build your own parser. With your parser,
you are ready to parse your configuration file.

    from configbuilder.parser import create_parser
    parser = create_parser('path/your_template.yaml',
                           casesensitivekey=False)
    config = parser.parse_config('path/your_configuration.yaml')
    value = config.get('attribute')
    
Or you can define your template in your code in dictionary type, and create the parser.

    from configbuilder.parser import ConfigParser
    YOUR_TEMPLATE = {
        'KEY1': 'String',
        'KEY2': 'Integer'
    }
    parser = ConfigParser(YOUR_TEMPLATE)

### Define new types
You can define your own validator inheriting Validator class and set to parser.
You implement validate_yourtype() in your custom validator to define new type called
```yourtype```. This type can be used in the template file.
Here is the code defining a new type called ```protocol``` which is kind of string,
but only accpeting 'ssh' or 'ftp' as the value.

    from configbuilder.validator import Validator
    class MyValidator(Validator):
        def validate_protocol(self, value):
            supporting_protocol = ['ssh', 'ftp'] 
            return self._validate_choiceses(value, supporting_protocol)
            
This validator can be set when building the parser.

    parser = create_parser('path/your_template.yaml',
                           validator=MyValidator())

## Installation

    pip install configbuilder

## Authors
* ** Joong-Hee Lee ** - *Initial work* - [joongh](https://github.com/joongh)
    
## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
