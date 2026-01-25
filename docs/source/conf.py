# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import datetime

project = 'CodeVideoRenderer'
copyright = f'{datetime.datetime.now().year}, ZhuChongjing'
author = 'ZhuChongjing'
release = 'v1.1.1'
language = 'zh_CN'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.mathjax',
    'sphinx_copybutton',
    'sphinx_design'
]

templates_path = ['_templates']
exclude_patterns = []

autosummary_generate = True
autosummary_imported_members = True
viewcode_follow_imported_members = True
viewcode_imported_members = True
napoleon_google_docstring = False
napoleon_numpy_docstring = True

autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'undoc-members': True,
    'private-members': True,
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']
html_title = f"CodeVideoRenderer {release}"
html_favicon = '_static/favicon.ico'
html_logo = '_static/logo.png'
html_theme_options = {
    "sidebar_hide_name": False,

    "light_css_variables": {
        "font-stack": "华文中宋",
        "font-stack--headings": "华文中宋",
    },
}
