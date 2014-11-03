from digitalforensics import *
import os
import fnmatch
import win32api
import sqlite3


class skype_overview(Plugin):
    PLUGIN_NAME = "Skype Overview"
    PLUGIN_DESCRIPTION = "Returns skype database information"

    
    
    def performScan(self):
        skypedbfilesfullpath = ""
        skypedbfilesfullpath = self.getSkypeDBFiles()
        maindb = []

        # Add full path to db files to forensics database
        for dbfiles in skypedbfilesfullpath:
           print dbfiles
           # Add information to database results.db using 4 parameters.
           self.results.append(Entry(self.PLUGIN_NAME, dbfiles, "Skype DB Files %s" % dbfiles, Entry.LEVEL_INFO))
           if dbfiles.endswith('\main.db'):
               maindb.append(dbfiles)

       
        print "\n"

        # loop over all main.db files that are found
        for maindbfiles in maindb:
            print "\n********************** \n"
            # Extract ACCOUNTS table information from maindb
            accounts = self.getSkypeMainDBaccounts(maindbfiles)
            for item in accounts:
                print "ACCOUNTS skypename: " + str(item[0])
                print "fullname: " + str(item[1])
                print "birthday: " + str(item[2])
                print "country: " + str(item[3])
                print "province: " + str(item[4])
                print "city: " + str(item[5])
                print "phone_home: " + str(item[6])
                print "phone_office: " + str(item[7])
                print "phone_mobile: " + str(item[8])
                print "emails: " + str(item[9])
                self.results.append(Entry(self.PLUGIN_NAME, "Account skypename: %s" % str(item[0]), "FullName: [%s], Birthday: [%s], Country: [%s], Province: [%s], City: [%s], PhoneHome: [%s], PhoneOffice: [%s], PhoneMobile: [%s], Emails: [%s] " %(str(item[1]),str(item[2]),str(item[3]),str(item[4]),str(item[5]),str(item[6]),str(item[7]),str(item[8]),str(item[9])), Entry.LEVEL_INFO))
                

                
            print "\n"
            
            # Extract CONTACTS table information from maindb
            contacts = self.getSkypeMainDBcontacts(maindbfiles)
            for item in contacts:
                print "CONTACTS skypename: %s" % item[0]
                print "fullname: %s" % item[1]
                print "birthday: %s" % item[2]
                print "country: %s" % item[3]
                print "city: %s" % item[4]
                print "\n"
                self.results.append(Entry(self.PLUGIN_NAME, "contacts skypename: %s"%str(item[0]), "FullName: [%s], Birthday: [%s], Country: [%s], City: [%s] "%(str(item[1]),str(item[2]),str(item[3]),str(item[4])), Entry.LEVEL_INFO))



            print "\n"

            # Extract MESSAGES table information from maindb
            messages = self.getSkypeMainDBmessages(maindbfiles)
            for item in messages:
                print "Messages> %s: %s " % (item[0], item[1])
                self.results.append(Entry(self.PLUGIN_NAME, "Messages> ", "%s: %s"% (str(item[0]), str(item[1])), Entry.LEVEL_INFO))
                



           

    def getSkypeDBFiles(self):
        # create empty arrays
        skypedirfound = []
        skypedbfiles = []

        # This will extract drive letters (ex: C:\, D:\ ) - requires win32api
        drives = win32api.GetLogicalDriveStrings()
        drives = drives.split('\000')[:-1]
        

        # search over each drive partition for full skype directory names
        for d in drives:
    
            #root = full directory path (ex: c:\dir1\dir2\dir3)
            #dirs = directory (ex: dir1, dir2, dir3)
            #files = filenames
            #topdown = scan directory True: top to bottom, False: bottom to up
    
            for root, dirs, files in os.walk(d, topdown=True):
                for directoryname in fnmatch.filter(dirs, 'Skype'):
                    skypedirfound.append((os.path.join(root,directoryname)))



        # loop over found skype directories and search for database files
        # if found then append full file paths to skypedbfiles array
        for d in skypedirfound:
            for root, dirs, files in os.walk(d, topdown=False):
                for name in files:
                    if name.endswith('.db'):
                        skypedbfiles.append((os.path.join(root, name)))


        return skypedbfiles




    def getSkypeMainDBaccounts(self, maindbfiles):
        accounts = []
        conn = sqlite3.connect(maindbfiles)
        cursor = conn.cursor()
        try:
            # ACCOUNTS DB
            cursor.execute("select skypename, fullname, birthday, country, province, city, phone_home, phone_office, phone_mobile, emails from accounts;")
            return cursor
            conn.close()
        except sqlite3.OperationalError, e:
            pass




    def getSkypeMainDBcontacts(self, maindbfiles):
        contacts = []
        conn = sqlite3.connect(maindbfiles)
        cursor = conn.cursor() 
        try:
            # CONTACTS DB
            cursor.execute("select skypename, fullname, birthday, country, city from contacts;")
            return cursor     
            conn.close()
        except sqlite3.OperationalError, e:
            pass


    
    def getSkypeMainDBmessages(self, maindbfiles):
        messages = []
        conn = sqlite3.connect(maindbfiles)
        cursor = conn.cursor()
        try:
            # MESSAGES DB
            cursor.execute("select from_dispname, body_xml from messages;")
            return cursor
            conn.close()
        except sqlite3.OperationalError, e:
            pass
    

            

plugin = skype_overview()

if __name__ == "__main__":
    plugin.performScan()
    









        
   
