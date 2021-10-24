from __future__ import print_function
import os.path
from datetime import timedelta, datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from apiclient.http import MediaFileUpload
import io
from googleapiclient.http import MediaIoBaseDownload
import json
from oauth2client.service_account import ServiceAccountCredentials
import asyncio
import time

scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
service = build('drive', 'v3', credentials=creds)
saved = False

file_metadata = {
	'name': 'dataBased.json' + str(datetime.now()),
	'mimeType': 'text/plain',
}
media = MediaFileUpload('dataBased.json', mimetype='text/plain')


def downloadFile(fileID):
	file_id = fileID
	request = service.files().get_media(fileId=file_id)
	fh = io.FileIO('dataBased.json', 'w')
	downloader = MediaIoBaseDownload(fh, request)
	done = False
	while done is False:
	    status, done = downloader.next_chunk()
	    print("Download %d%%." % int(status.progress() * 100))

def backupDataBased(basedCountDatabase):
	global file_metadata
	global media
	print('Backing up...')
	with open('dataBased.json', 'w') as dataBased:
		json.dump(basedCountDatabase, dataBased)
		print('Still...')
	file_metadata = {
		'name': 'dataBased.json' + str(datetime.now()),
		'mimeType': 'text/plain',
	}
	print('And...')
	media = MediaFileUpload('dataBased.json', mimetype='text/plain')
	print('Uh...')
	p = ""
	loop = asyncio.get_event_loop()
	loop.run_in_executor(None, saveFileToDrive, p)
	#saveFile = asyncio.create_task(saveFileToDrive(file_metadata, media))
	wasteTime()
	print('Finished.')

def retrieveDataBased():
	results = service.files().list(pageSize=1, fields="nextPageToken, files(id, name)").execute()
	items = results.get('files', [])

	if not items:
		print('No files found.')
	else:
		print('Files:')
		for item in items:
			print(u'{0} ({1})'.format(item['name'], item['id']))
			downloadFile(item['id'])

def saveFileToDrive():
	global saved
	global file_metadata
	global media
	service.files().create(body=file_metadata, media_body=media, fields='id').execute()
	saved = True

def wasteTime():
	while saved == False:
		print('Wasting time...')
		time.sleep(1)