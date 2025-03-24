import sys

# clear modules cache if package is reloaded (after update?)
prefix = __package__ + ".plugins"  # don't clear the base package
for module_name in [
    module_name
    for module_name in sys.modules
    if module_name.startswith(prefix)
]:
    del sys.modules[module_name]
del prefix

from .plugins.new_file import *
from .plugins.insert_frontmatter import *

from .plugins.decor import (
    HandyllmDecorBlockHeadListener,
    HandyllmDecorFrontmatterListener,
    plugin_loaded as decor_plugin_loaded,
    plugin_unloaded as decor_plugin_unloaded
)


def plugin_loaded():
    decor_plugin_loaded()

def plugin_unloaded():
    decor_plugin_unloaded()
