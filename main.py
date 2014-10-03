from digitalforensics import *
import imp, sqlite3

plugins = ["windows_overview", "installed_programs", "browser_information", "file_magic", "skype_overview"]
loaded = []

for plugin in plugins:
    loaded.append(imp.load_source(plugin, "plugin_%s.py" % (plugin)))

conn = sqlite3.connect('results.db')
cursor = conn.cursor()
try:
	cursor.execute("CREATE TABLE results (plugin_name text, entry text, message text, warning_level int, additional_info text)")
except sqlite3.OperationalError:
	pass

conn.commit()

for plugin in loaded:
    plugin.plugin.performScan()

for plugin in loaded:
	print "Plugin: %s" % plugin.plugin.PLUGIN_NAME
	print "Description: %s" % plugin.plugin.PLUGIN_DESCRIPTION
	for result in plugin.plugin.getResults():
		if result.entry_level == Entry.LEVEL_WARN:
			print "[WARN] %s" % result.entry_message
		elif result.entry_level == Entry.LEVEL_HIGH:
			print "[HIGH] %s" % result.entry_message
		elif result.entry_level == Entry.LEVEL_INFO:
			print "[INFO] %s" % result.entry_message
		cursor.execute("INSERT INTO results VALUES (?, ?, ?, ?, ?)",
			(result.entry_plugin, result.entry_data, result.entry_message, result.entry_level, result.entry_additional_info)
		)
		conn.commit()
	print "\n"
conn.close()
