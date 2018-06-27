# Attachi

A small helper script, that creates the folder structure needed to register files as attachment to openBIS.

# Example

Creating the folder structure for an upload:
python attachmentHelper.py -u myusername QABCD README.md "this is a test for uploading the readme file"

--> folder QABCD000AQ_20180627102707758164 is created

Use tar and dync to upload the file to openBIS:

tar -c QABCD000AQ_20180627102707758164 | dync -n QABCD000AQ_20180627102707758164.tar -k untar:True data.qbic.uni-tuebingen.de