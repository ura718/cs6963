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

        for dbfiles in skypedbfilesfullpath:
           print dbfiles
           # add information to database results.db using 4 parameters.
           self.results.append(Entry(self.PLUGIN_NAME, dbfiles, "Skype DB Files %s"%dbfiles, Entry.LEVEL_INFO))
           if dbfiles.endswith('main.db'):
               maindb = dbfiles

        
        print "\n"
        
        # Extract CONTACTS table information from maindb
        contacts = self.getSkypeMainDB(maindb)
        for item in contacts:
            print "CONTACTS skypename: " + str(item[0])
            print "fullname: " + str(item[1])
            print "birthday: " + str(item[2])
            print "country: " + str(item[3])
            print "city: " + str(item[4]) + "\n"
            self.results.append(Entry(self.PLUGIN_NAME, "contacts skypename: %s"%str(item[0]), "FullName: [%s], Birthday: [%s], Country: [%s], City: [%s] "%(str(item[1]),str(item[2]),str(item[3]),str(item[4])), Entry.LEVEL_INFO))





           

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

                    
        #for dbfiles in skypedbfiles:
         #  print dbfiles
           # add information to database results.db using 4 parameters.
          # self.results.append(Entry(self.PLUGIN_NAME, dbfiles, "Skype DB Files %s"%dbfiles, Entry.LEVEL_INFO)) 

        return skypedbfiles


    def getSkypeMainDB(self, maindb):
        #print maindb
        contacts = []
        conn = sqlite3.connect(maindb)
        cursor = conn.cursor()
        try:
            # CONTACTS DB
            cursor.execute("select skypename,fullname,birthday,country,city from contacts;")
            return cursor
            #for item in cursor:
            #    print 'skypename: ' + str(item[0])
            
            
            conn.close()
        except sqlite3.OperationalError, e:
            pass


            

plugin = skype_overview()

if __name__ == "__main__":
    plugin.performScan()
    









        
   
