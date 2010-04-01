import sys
import inspect

overrides = {
    "stdin": "", # [script] -
    "digits": "n", # csplit
    "exit": "x",
    "extract": "x",
    "zip": "z",
    "gzip": "z",
    "compress": "z",
    "literal": "N", # ls
}

class CLIArgs:
    def __init__(self):
        self.mandatory = []
        self.short = {}
        self.long = {}
        self.dump = None
        self.kwdump = None

def shortarg(arg):
    return [arg[0], arg[0].swapcase()] + (overrides[arg] if arg in overrides else [])

def getargs(func):
    args = CLIArgs()
    spec = inspect.getargspec(func)
    mandargnum = len(spec[0]) - len(spec[3])
    mandargs = spec[0][:mandargnum]
    optargs = zip(spec[0][mandargnum:], spec[3] if spec[3] else ())
    
    for arg in mandargs:
        args.mandatory.append(arg)
        args.long[arg] = str
        for short in shortarg(arg):
            if short not in args.short:
                args.short[short] = arg
                break
    for arg, default in optargs:
        args.long[arg] = type(default)
        for short in shortarg(arg):
            if short not in args.short:
                args.short[short] = arg
                break
    
    if spec[1]:
        args.mandatory.append(spec[1])
        args.dump = spec[1]
    if spec[2]:
        args.kwdump = spec[2]
    
    return args

def evalval(type, val):
    if type == int:
        return int(val)
    elif type == float:
        return float(val)
    elif type == list:
        return val.split(",")
    elif type == dict:
        return dict([s.split("=")[:2] for s in val.split(",")])
    elif type == bool:
        return True
    elif type == str:
        return val
    else:
        raise TypeError, "`%s` type not supported for command-line \
arguments" % type

def parseargs(args, schema):
    passargs = {}
    takingopts = True
    errors = False
    setval = ""
    
    if schema.dump:
        passargs[schema.dump] = [] # Not OrObjected yet
    if schema.kwdump:
        passargs[schema.kwdump] = {} # Also not OO'd yet
    
    for i in args:
        if i.startswith("--") and len(i) > 2 and takingopts:
            kw, t, val = i[2:].partition("=")
            
            if kw not in schema.long and not schema.kwdump:
                print "ERROR: Unknown option `%s`" % kw
                errors = True
                continue
            elif schema.kwdump:
                passargs[schema.kwdump][kw] = evalval(str, val)
                continue
            
            if kw in schema.mandatory:
                schema.mandatory.remove(kw)
            
            passargs[kw] = evalval(schema.long[kw], val)
        elif i == "--" and takingopts:
            takingopts = False
        elif i.startswith("-") and takingopts:
            key = i[1:2]
            val = i[2:]
            
            if key not in schema.short:
                print "ERROR: Unknown option `%s`" % key
                errors = True
                continue
            elif schema.kwdump:
                setval = ":kwdump:"
                continue
            
            if schema.short[key] in schema.mandatory:
                schema.mandatory.remove(schema.short[key])
            
            if schema.long[schema.short[key]] == "bool":
                passargs[schema.short[key]] = True
            elif val:
                passargs[schema.short[key]] = evalval(schema.long[schema.short[key]], val)
            else:
                setval = schema.short[key]
        elif setval:
            if setval == ":kwdump:":
                passargs[schema.kwdump][setval] = evalval(str, val)
            else:
                passargs[setval] = evalval(schema.long[setval], i)
                setval = ""
        else:
            try:
                kw = schema.mandatory[0]
            except IndexError:
                print "ERROR: Too many arguments"
                errors = True
                continue
            
            if kw == schema.dump:
                passargs[schema.dump].append(i)
                takingopts = False
                continue
            
            passargs[kw] = evalval(schema.long[kw], i)
            schema.mandatory.pop(0)
    
    if schema.dump:
        passargs[schema.dump] = passargs[schema.dump]
    if schema.kwdump:
        passargs[schema.kwdump] = passargs[schema.kwdump]
    
    if len(schema.mandatory) and schema.mandatory[0] != schema.dump:
        m = len(schema.mandatory) - (1 if schema.dump in schema.mandatory else 0)
        print "Arguments Missing: " + ", ".join(map(lambda x: "`%s`"%x, schema.mandatory))
        print "ERROR: Missing %d arguments; consult --help for command syntax" % m
        errors = True
    if setval:
        print "ERROR: Expecting value for argument `%s`" % setval
        errors = True
    
    if errors:
        sys.exit(1)
    
    return passargs

def run_main(schema, args, help=None, version=None):
    if "--help" in args or "-h" in args or "-?" in args:
        idx = args.index("--help" if "--help" in args else "-h" if "-h" in args else "-?" if "-?" in args else None)
        if callable(help):
            help(*args[idx+1:])
        else:
            print help
    elif "--version" in args:
        if callable(version):
            version()
        else:
            print version
    else:
        return parseargs(args, schema)

def run(func, args, help=None, version=None):
    schema = getargs(func)
    kwargs = run_main(schema, args, help, version)
    if kwargs is not None: func(**kwargs)

def main():
    mod = sys.modules["__main__"]
    if hasattr(mod, "__main__"):
        func = mod.__main__
        help = mod.__help__ if hasattr(mod, "__help__") else mod.__doc__ if hasattr(mod, "__doc__") else None
        version = mod.__version__ if hasattr(mod, "__version__") else None
        run(func, sys.argv[1:], help, version)
