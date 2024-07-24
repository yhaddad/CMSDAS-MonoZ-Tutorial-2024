# Users guide to the *subMIT* login pool

The users guide can be found [here](https://submit.mit.edu/~freerc/MonoZ_CMSDAS/index.html).


# For people editing

This will need to be done on submit or in some other place where an apache server is running. If you are running your own apache server, then you need to make sure to put the output html files in the correct path (e.g. /var/www/html). The path is defined in the bin directory script.


Download the following sphinx packages in order to compile (use python3)

```
yum install python-sphinx
pip install groundwork-sphinx-theme
pip install sphinx-toolbox
pip install sphinx-togglebutton
```

In order to build the code and update the website do the following

```
./bin/sphinx-it.sh
```
