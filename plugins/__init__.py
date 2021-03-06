import logging
import sys

sys.path.insert(0, "plugins")
debuglog = logging.getLogger("ManaChat.Debug")

plugins_loaded = []


class PluginError(Exception):
    pass


def load_plugin(config, plugin_name):
    if plugin_name in plugins_loaded:
        return

    plugin = __import__(plugin_name)

    for p in plugin.PLUGIN['blocks']:
        if p in plugins_loaded:
            raise PluginError("{} blocks {}".format(p, plugin_name))

    for p in plugin.PLUGIN['requires']:
        if p not in plugins_loaded:
            load_plugin(config, p)

    plugin.init(config)
    plugins_loaded.append(plugin_name)
    debuglog.info('Plugin %s loaded', plugin_name)


def load_plugins(config, *plugin_names):
    for pn in plugin_names:
        try:
            load_plugin(config, pn)
        except ImportError as e:
            debuglog.error('Error loading plugin %s: %s', pn, e)
