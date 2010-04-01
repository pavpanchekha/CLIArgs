CLIArgs: Absolutely Trivial Command-line Arguments
==================================================

Doesn't parsing command line arguments suck? At best, you use ``optparse``, and
then if that doesn't work you hand-code it. Or, you use ``getargs``, which
requires writing your own loops. Don't you wish for something a little bit...
smarter? CLIArgs makes argument parsing a piece of cake.

Basics
------

Define a few functions, change your ``if __name__ == "__main__"`` block, and
CLIArgs does the rest::

    import cliargs
    
    __help__ = "clone source [destinations] [-v]"
    __version__ = "1.0"

    def __main__(source, *dest, verbose=False):
        ...

    if __name__ == "__main__":
        cliargs.main()

If you run this file (``clone``), the following command lines will all do the
obvious::

    clone a b c d e
    clone --source=a b c d e
    clone a b -v
    clone --help
    clone -?
    clone --version

In general, all arguments to the function ``__main__`` are examined, based on
which the command line will be intelligently parsed. If necessary, the help and
version info will be displayed. Finally, most errors in parsing command-lines
are caught and a summary prepared for the user.

Argument types
--------------

The basic algorithm will examine the arguments of the function (that is, of
``__main__``) and assign, for each arguments, a short and long argument, and
a type. The long argument is always the name of argument; the short argument
is, in order, the short name is the first letter of this short argument, or
(if that is unavailable) the swapcase'd version of that letter, or one of a
built-in list of exceptions. These are assigned left-to-right.

The type of any argument is by default assumed to be a string. However, if
the argument is given a default value (as is ``verbose`` in the example above),
the type of the default argument is used. If the type is a string, the
command-line argument is simply passed to the function. However, integers and
floats are converted into true integers and floats, booleans make their
corresponding arguments into flags (such as ``verbose`` above), lists
are created by splitting a single comma-delimited argument (that means that
there cannot be spaces between the arguments; use ``--list=1,2,3,4`` or
similar constructions) and dictionaries by splitting by commas, then
equal signs (e.g. ``--dict=a=1,b=2,c=3``). Of course, list and dictionary
arguments are usually better handled by the ``*args`` and ``**kwargs``
parameters.

Help & Version
--------------

The help information is taken from a function called ``__help__``, a string named
``__help__``, or the module documentation. If ``__help`` is a function, it is called,
with all of the arguments after the first ``-?`` (or ``-h`` or `--help``) passed as
arguments; thus, it it best that ``__help__`` take a variable number of arguments.
Otherwise, ``__help__`` is assumed to be a string and is printed. ``__version__`` can
likewise be either a string or a function; as a function, it is called without arguments.

Use Beyond Argument Parsing
---------------------------

Sometimes, we want to parse arguments other than those in ``sys.argv``, such as for
a built-in shell. One can use CLIArgs to provide a similarly-shiny tool for this
purpose as well. Simply use the function ``cliargs.run(function, arguments, help=None,
version=None)``.
