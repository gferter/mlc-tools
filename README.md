[![Build status](https://ci.appveyor.com/api/projects/status/t5sp7poff0ygygw5/branch/master?svg=true)](https://ci.appveyor.com/project/Volodar/tools-mlc/branch/master)

### Simple using: ###


```
cd src
python main.py
```

### Configured launch: ###

**Parameters:**
```
    -h, --help      show this help message and exit
    -i              Path to classes configs. Default = ./config/
    -o              Out Path for classes. Default = ./out/
    -l              Used language. Supported cpp, py, php. Default = cpp
    -f              Used serialized format. Supported xml, json. Default = xml
    -side           To different side generation, used both, server, client. Default = both
    -data           Path to static data configs. Default = empty, conversion is not used
    -data_out       Out path for static data config. Default = empty
    -only_data      Flag for build only data xml. Default = no
    -protocols      Path to file with serialization protocols. Default = empty, default protocol is used
    -php_validate   Check PHP features on generate other languages. Default = yes
    -test_script    The path to the script to run the tests
    -use_colors     Using colors on outputting to the console
```

### Syntax: ###

```
class core/Request<SerializedObject>
{
    Action action
    int int_data
    float float_data = 0
    function void some_function(){}
}
```

**class** - keyword

**core/** - The module. Used only for grouping classes into folders for c++ generation

**Request** - Name of the class

**SerializedObject** - The inherited class. Multiple inheritance is not supported.

**{ ... }** - Body of the class or method

**int int_data** - Field of class *int_data* of integer type.

**int float_data** - Field of class *float_data* of float type with initialized.

**function void some_function(){}** - Method of the class without body