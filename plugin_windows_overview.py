from digitalforensics import *
import win32com.client
import os

class windows_overview(Plugin):
	PLUGIN_NAME = "Windows System Overview"
	PLUGIN_DESCRIPTION = "Returns things specific to this installation of windows, such as accessed files or users."

	username = ""
	def performScan(self):
		self.username = self.getCurrentUsername()
		self.results.append(Entry(self.PLUGIN_NAME, self.username, "Current User: %s"%self.username, Entry.LEVEL_INFO))

		recently_accessed = self.getRecentlyAccessedFiles()
		for accessed in recently_accessed:
			self.results.append(Entry(self.PLUGIN_NAME, accessed, "Recently Accessed File: %s"%accessed, Entry.LEVEL_INFO))

	def getCurrentUsername(self):
		return os.environ.get("USERNAME")

	def getRecentlyAccessedFiles(self):
		if not self.username:
			return

		directory = "C:\\Users\\%s\\AppData\\Roaming\\Microsoft\\Windows\\Recent" % (self.username)
		shell = win32com.client.Dispatch("WScript.Shell")
		paths = []
		for shortcut in os.listdir(directory):
			if shortcut[-4::] != ".lnk":
				continue

			shortcut = shell.CreateShortcut("%s\\%s" % (directory, shortcut))
			path = shortcut.TargetPath
			if path:
				paths.append(path)

		return paths

	def outputReport(self):
		""

plugin = windows_overview()

if __name__ == "__main__":
	plugin.performScan()
	print plugin.getRecentlyAccessedFiles()