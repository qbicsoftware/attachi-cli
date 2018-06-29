import os
import sys
import getpass
import datetime
import subprocess

class Attachi(object):

    def __init__(self, qcode, fpath, comment, username = "", output = ""):
        self.code = qcode
        self.path = fpath
        self.comment = comment
        self.username = username

    def run(self):
        now = datetime.datetime.now()
        log_path = os.path.dirname(os.path.realpath(__file__))+"/helper_logs/attachment_helper_"+str(now.year)+"_"+str(now.month)+"_"+str(now.day)+".log"
        global logfile
        
        logfile = open(log_path, "a+")

        USER = getpass.getuser()
        PROJECT = self.code
        PATH = self.path
        COMMENT = self.comment
        target = os.path.dirname(os.path.realpath(__file__))

        init_log()
        log("Want to upload Attachment "+PATH+" ("+COMMENT+") to openBIS project "+PROJECT+" as user "+USER)

        if os.path.isdir(PATH):
            log(PATH+" is a directory. Quitting.")
            sys.exit(PATH+" is a directory. You can only upload files as attachments.")
        f = os.path.basename(PATH)

        timestamp = now().replace(" ","").replace(":","").replace(".","").replace("-","")
        base = PROJECT+"000A"
        barcode = base+checksum(base)
        folder = os.path.join(target, barcode+"_"+timestamp)
        os.system("mkdir "+folder)
        log("Folder "+folder+" created")

        metadata = open(os.path.join(folder,"metadata.txt"),"w")
        metadata.write("user="+USER+"\n")
        metadata.write("info="+COMMENT+"\n")
        metadata.write("barcode="+PROJECT+"000\n")
        metadata.write("type=Results\n")
        metadata.close()

        log("Wrote metadata file to folder "+folder)
        cmd = "cp "+PATH+" "+os.path.join(folder,f)
        print("copying "+PATH+" to the dropbox...")
        subprocess.call(cmd.split(" "))
        log("Copying of data file done. checking existence...")
        exists = os.path.isfile(os.path.join(folder,f))
        log(str(exists))
        if not exists:
            print("File could not be copied!")
        else:
            print("done.")
            cmd = "touch "+os.path.join(OPENBIS_DROPBOX, ".MARKER_is_finished_"+timestamp)
            subprocess.call(cmd.split(" "))
            print("marker file has been created. your attachment should now be registered to openbis.")
            log("Marker file created\n")
        logfile.close()

def now():
    return str(datetime.datetime.now())

def log(text):
    logfile.write(now()+" "+text+"\n")

def init_log():
	now = datetime.datetime.now()
	log_path = os.path.dirname(os.path.realpath(__file__))+"/helper_logs/attachment_helper_"+str(now.year)+"_"+str(now.month)+"_"+str(now.day)+".log"
	global logfile
	logfile = open(log_path, "a+")

def mapToDigit(num):
	num += 48 # 0 to 9
	if num > 57:
		num += 7 # A to X
	return chr(num)

def checksum(name):
	i = 1;
	sum = 0;
	for x in name:
		sum += (ord(x))*i
		i += 1
	return mapToDigit(sum%34) # 10 numbers + 24 letters
