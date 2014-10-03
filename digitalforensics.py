class Plugin:
    PLUGIN_NAME = ""
    PLUGIN_AUTHOR = ""
    PLUGIN_DESCRIPTION = ""
    results = []
    def __init__(self, results=None):
    	if results is None:
    		results = []

    	self.results = results
        ""

    def performScan(self):
        ""

    def getResults(self):
    	return self.results

    def outputReport(self):
        ""

class Entry:
	entry_data = ""
	entry_message = ""
	entry_additional_info = ""
	entry_level = 1
	entry_plugin = ""
	LEVEL_HIGH = 3
	LEVEL_WARN = 2
	LEVEL_INFO = 1

	def __init__(self, plugin_name, entry_data, entry_message, warning_level, additional_info=None):
		self.entry_data = entry_data
		self.entry_message = entry_message
		self.entry_additional_info = repr(additional_info)
		self.entry_level = warning_level
		self.entry_plugin = plugin_name