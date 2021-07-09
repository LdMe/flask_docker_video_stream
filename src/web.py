#!/usr/bin/env/ python
from flask import Flask, render_template, Response, redirect, send_from_directory, request, jsonify
from video.videoServer import WebServer
from threading import Thread
import time
from arduino.server import SocketServer
from flask_talisman import Talisman

app = Flask(__name__,template_folder="views",static_folder='static')
webServer= WebServer()	
arduinoSocket = SocketServer()

@app.route("/")
def index():
	return render_template("index.html",temperature = arduinoSocket.temperature,humidity = arduinoSocket.humidity)

@app.route("/data")
def sendData():
	data={"temperature":arduinoSocket.temperature, "humidity":arduinoSocket.humidity}
	return jsonify(data)

@app.route('/video_feed')
def videoFeed():
	try:
		return Response(webServer.getVideoStream(),
				mimetype='multipart/x-mixed-replace; boundary=frame')
	except :
		return ('', 204)

@app.route("/record")
def record():
	print(request.args)
	outputSeconds = int(request.args.get("recording_time"))
	fps = int(request.args.get("fps"))
	timeBetweenFrames = float(request.args.get("speed"))/fps
	webServer.record(outputSeconds,fps,timeBetweenFrames)
	return redirect("/", code=302)

@app.route("/show")
def showRecorded():
	files= webServer.getRecordedVideos()
	return render_template("show.html",files = files)

@app.route("/show/<filename>")
def showVideo(filename):
	return send_from_directory("static/media",filename)

@app.route("/pause/<writerID>")
def pauseWriter(writerID):
	webServer.togglePauseTimeLapseWriter(int(writerID))
	#return send_from_directory("static/media",filename)
	return ("", 200)

@app.route("/active")
def showWriters():
	return jsonify(webServer.getTimeLapseWritersSpecs())
	



		
	

if __name__ == '__main__':
	
	#Thread(target= get_frame, args=()).start()
	#Talisman(app)
	app.run(host="0.0.0.0",port="443" ,debug=False)