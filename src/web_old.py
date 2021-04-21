#!/usr/bin/env/ python
from flask import Flask, render_template, Response, redirect, send_from_directory
from video.videoServer import VideoServer
from threading import Thread
import time
import os

app = Flask(__name__,template_folder="views",static_folder='media')
videoServer = None
frame = None
class webServer:
	
@app.route("/")
def index():
	return render_template("index.html")

def gen():
	global videodServer
	videoServer= VideoServer.getSingleton()
	videoServer.start()
	while True:
		frame = 
		if(frame):
			yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n'+ frame + b'\r\n')
	videoServer.stop()	

def getFrame():
	return videoServer.getEncodedFrame()
def sendFrame():

@app.route('/video_feed')
def videoFeed():
	return Response(gen() ,
		mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/record")
def record():

	if(vid):
		print("recording")
		if( videoServer.started):
			videoServer.record()
	else:
		print("falseeeeeee")
	return redirect("/", code=302)

@app.route("/show")
def show_recorded():
	path = "./media/"
	files=[]
	for r, d, f in os.walk(path):
		for file in f:
			files.append(file)
	print(files)
	return render_template("show.html",files = files)
@app.route("/show/<filename>")
def show_video(filename):
	return send_from_directory("media",filename)


if __name__ == '__main__':

	#Thread(target= get_frame, args=()).start()
	app.run(host="0.0.0.0", debug=False)