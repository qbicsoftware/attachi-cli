import os, sys, datetime, subprocess, argparse

USAGE = """Creates the folder structure needed to register files as attachment to openBIS. The folder can then be uploaded via Dync or other means.
python attachmentHelper.py PROJECTCODE FILEPATH COMMENT [USERNAME]
Comment describes the file(s) you upload and needs to be in quotes. The username will show up as uploader in openBIS"""

parser = argparse.ArgumentParser()
parser.add_argument("code", type=str, help="the 5 letter project code")
parser.add_argument("file", type=str, help="the file path of the result file to be uploaded")
parser.add_argument("comment", type=str, help="a comment describing the file")
parser.add_argument("-u", "--user", type=str, help="username shown in openbis as uploader")
parser.add_argument("-o", "--out", type=str, help="output folder path")
args = parser.parse_args()

# leaving out non-alphanumerical signs
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

def now():
	return str(datetime.datetime.now())

def log(text):
	logfile.write(now()+" "+text+"\n")

def init_log():
	now = datetime.datetime.now()
	log_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "logs")
	if not os.path.exists(log_folder):
		os.makedirs(log_folder)
	log_path = os.path.join(log_folder, "attachment_helper_"+str(now.year)+"_"+str(now.month)+"_"+str(now.day)+".log")
	global logfile
	logfile = open(log_path, "a")

USER = None
if args.user:
	USER = args.user
target = os.path.dirname(os.path.realpath(__file__))
if args.out:
	target = args.out
PROJECT = args.code
PATH = args.file
COMMENT = args.comment

init_log()
log("Want to create Attachment "+PATH+" ("+COMMENT+") folder structure for "+PROJECT)
if USER:
	log("as user:" +USER)

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
if USER:
	metadata.write("user="+USER+"\n")
metadata.write("info="+COMMENT+"\n")
metadata.write("barcode="+PROJECT+"000\n")
metadata.write("type=Results\n")
metadata.close()

log("Wrote metadata file to folder "+folder)
cmd = "cp "+PATH+" "+os.path.join(folder,f)
print ("copying "+PATH+" to the target folder")
subprocess.call(cmd.split(" "))
log("Copying of data file done. checking existence...")
exists = os.path.isfile(os.path.join(folder,f))
log(str(exists))
if not exists:
	print ("File could not be copied!")
logfile.close()
