import cliargs

__version__ = "0.1.WIN"

def __help__(cmd=""):
    if cmd:
        print "No help available for command `%s`. Because this command ain't not be havin them subcommands" % cmd
        return
    print "You want help? Read the source, it's like 20 lines damn it. Gosh. People these days."

def __main__(source, source2, intermediate="/tmp/tmp", silent=False, *names_to_print, **kwargs):
    f = open(source).read()
    open(intermediate, "w").write(f)
    g = open(intermediate).read()
    open(source2, "w").write(g)
    print "\n".join(names_to_print)
    if not silent:
        for kw, val in kwargs.items():
            print "\t%s:\t%s" % (kw, val)

if __name__ == "__main__":
    cliargs.main()
