from digitalforensics import *
import sqlite3
import os

class browser_information(Plugin):
	PLUGIN_NAME = "Browser Information Collector"
	PLUGIN_DESCRIPTION = "Grab as much info from the various browsers installed."
	firefox_usernames = 0
	firefox_searches = 0
	chrome_usernames = 0

	def performScan(self):
		profiles = self.enumerateFirefoxProfiles()
		self.getFirefoxSearchHistory(profiles)
		self.getFirefoxUsernames(profiles)
		self.getChromeUsernames()
		self.getTopChromeUrls()
		# passwords: signon.sqlite

	def enumerateFirefoxProfiles(self):
		profile_dir = os.environ.get("appdata")
		profile_dir += "\\Mozilla\\Firefox\\Profiles"
		try:
			return os.listdir(profile_dir)
		except:
			return []

	def getTopChromeUrls(self):
		path = os.getenv("localappdata") + r"\Google\Chrome\User Data\Default\History"
		conn = sqlite3.connect(path)
		c = conn.cursor()
		results = []
		for row in conn.execute("SELECT url, title, visit_count FROM urls ORDER BY visit_count DESC LIMIT 5"):
			results.append(str(row[0]))
			self.addRow(str(row[0]), "\"%s\" (%s) visited %d times" % (str(row[1]), str(row[0]), int(row[2])))

		self.chrome_usernames = len(results)
		return results

	def getChromeUsernames(self):
		path = r"C:\Users\IEUser\AppData\Local\Google\Chrome\User Data\Default"
		path = os.getenv("localappdata") + r"\Google\Chrome\User Data\Default\Login Data"
		conn = sqlite3.connect(path)
		c = conn.cursor()
		results = []
		for row in conn.execute("SELECT username_value, origin_url FROM logins"):
			results.append(str(row[0]))
			self.addRow(str(row[0]), "Chrome Username %s seen on %s"%(str(row[0]),str(row[1])))

		self.chrome_usernames = len(results)
		return results

	def getFirefoxSearchHistory(self, profiles):
		searches = []
		path = r"C:\Users\IEUser\AppData\Roaming\Mozilla\Firefox\Profiles\av2zecx8.default"
		for profile in profiles:
			conn = sqlite3.connect(os.environ.get("appdata") + "\\Mozilla\\Firefox\\Profiles\\" + profile + "\\formhistory.sqlite")
			c = conn.cursor()
			for row in conn.execute("SELECT value, timesused FROM moz_formhistory WHERE fieldname='searchbar-history' ORDER BY timesused DESC limit 5"):
				searches.append(str(row[0]))
				self.addRow(str(row[0]), "\"%s\" searched %d times" % (str(row[0]), int(row[1])))

		self.firefox_usernames = len(searches)
		return searches

	def getFirefoxUsernames(self, profiles):
		searches = []
		username_substrings = ["username", "name", "email", "uname", "id", "mail", "login", "user"]
		path = r"C:\Users\IEUser\AppData\Roaming\Mozilla\Firefox\Profiles\av2zecx8.default"
		for profile in profiles:
			conn = sqlite3.connect(os.environ.get("appdata") + "\\Mozilla\\Firefox\\Profiles\\" + profile + "\\formhistory.sqlite")
			c = conn.cursor()
			for row in conn.execute("SELECT fieldname,value FROM moz_formhistory ORDER BY timesused"):
				for username in username_substrings:
					if username in row[0]:
						searches.append(str(row[1]))
						self.addRow(str(row[1]), "Firefox Username: %s"%str(row[1]))

		self.firefox_usernames = len(searches)
		return searches

	def addRow(self, text, full_text):
		self.results.append(Entry(self.PLUGIN_NAME, text, full_text, Entry.LEVEL_WARN))

	def outputReport(self):
		buffer = ""
		buffer += "%d firefox usernames gathered\n" % (self.firefox_usernames)
		buffer += "%d firefox searches gathered\n" % (self.firefox_searches)
		buffer += "%d chrome usernames gathered\n" % (self.chrome_usernames)

plugin = browser_information()

if __name__ == "__main__":
	plugin.performScan()