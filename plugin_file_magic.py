from digitalforensics import *
import os, fnmatch, pyPdf

class file_magic(Plugin):
	PLUGIN_NAME = "File Magic"
	PLUGIN_DESCRIPTION = "Searches for certain files and gives interesting metadata about them."

	def performScan(self):
		pdf_files = self.findFiles(os.getenv("userprofile"), "*.pdf")
		for files in pdf_files:
			try:
				data = pyPdf.PdfFileReader(open(files, "rb")).getDocumentInfo()
                                self.results.append(Entry(self.PLUGIN_NAME, "PDF Author: %s"%data['/Author'], files, Entry.LEVEL_INFO))
				self.results.append(Entry(self.PLUGIN_NAME, "PDF Title: %s"%data['/Title'], files, Entry.LEVEL_INFO))
			except:
				pass

	def findFiles(self, path, pattern):
		matches = []
		for root, dirnames, filenames in os.walk(path):
			for filename in fnmatch.filter(filenames, pattern):
				matches.append(os.path.join(root, filename))

		return matches

	def outputReport(self):
		""

plugin = file_magic()

if __name__ == "__main__":
	plugin.performScan()
