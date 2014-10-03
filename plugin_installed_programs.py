from digitalforensics import *
from _winreg import *

class installed_programs(Plugin):
    PLUGIN_NAME = "Installed Programs"
    PLUGIN_DESCRIPTION = "Get a list of high-risk software that is installed on the system"
    def performScan(self):
        risky_program = "%s is a potentially risky program, typically used by criminals."
        regular_program = "%s was found installed on the system."
        aReg = ConnectRegistry(None,HKEY_LOCAL_MACHINE)
        aKey = OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
        for i in range(1024):
            try:
                asubkey_name=EnumKey(aKey,i)
                asubkey=OpenKey(aKey,asubkey_name)
                val=QueryValueEx(asubkey, "DisplayName")

                if self.determineDangerous(val[0]):
                    self.results.append(Entry(self.PLUGIN_NAME, str(val[0]), risky_program%str(val[0]), Entry.LEVEL_WARN))
                else:
                    try:
                        self.results.append(Entry(self.PLUGIN_NAME, str(val[0]), regular_program%str(val[0]), Entry.LEVEL_INFO))
                    except UnicodeEncodeError:
                        pass
            except EnvironmentError:
                continue

    def determineDangerous(self, program_name):
        substrings = ["nmap", "wireshark", "cain & abel", "hashcat", "nessus", "kismet", "netstumbler", "itunes"]
        for string in substrings:
            if string in program_name.lower():
                return True

    def outputReport(self):
        template = "High Risk Program Found: %s\n"
        buffer = ""
        for result in self.results:
            if result.entry_level == Entry.LEVEL_WARN:
                buffer += template % result.entry_data

        return buffer

plugin = installed_programs()
