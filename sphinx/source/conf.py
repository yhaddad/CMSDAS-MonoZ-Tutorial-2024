# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'Mono Z'
copyright = '2024, The Mono Z CMSDAS Team'
author = 'The Mono Z Analysis Team'

# The full version, including alpha/beta/rc tags
release = 'v1'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
'sphinx_toolbox.collapse','sphinx_tabs.tabs','sphinx_togglebutton'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#

#html_theme = 'alabaster'
#html_theme = 'sizzle'
html_theme = 'groundwork'

#Theme options for groundwork: https://github.com/useblocks/groundwork-sphinx-theme
html_theme_options = {
#    "sidebar_width": '240px',
    "stickysidebar": True,
    "stickysidebarscrollable": True,
#    "contribute": True,
#    "github_fork": "useblocks/groundwork",
#    "github_user": "useblocks",
}

#import sphinx_adc_theme
#html_theme = 'sphinx_adc_theme'
#html_theme_path = [sphinx_adc_theme.get_html_theme_path()]

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []
#html_logo = 'img/submit-logo-construction.png'
html_logo = 'img/monoz.png'
html_favicon = 'img/monoz.png'
