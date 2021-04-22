
import imagezmq
import cv2
from threading import Thread
from video.videoWriter import *
import os

class WebServer:
	videoServer = None
	frame = None

	def getVideoStream(self):
		
		self.videoServer= VideoServer.getSingleton()
		self.videoServer.start()
		yield from self.sendFrame()
		self.videoServer.stop()	


	def getFrame(self):
		return self.videoServer.getEncodedFrame()
	def getRecordedVideos(self):
		path = "./static/media/"
		files=[]
		for r, d, f in os.walk(path):
			for file in f:
				files.append(file)
		return files
	
	def record(self, outputSeconds = 10.0, fps = 10,timeBetweenFrames=1):
		if(self.videoServer):
			print("recording")
			if( self.videoServer.started):
				self.videoServer.record(outputSeconds, fps,timeBetweenFrames)
		else:
			print("video Server not available")
	def sendFrame(self):
		while True:
			self.frame = self.getFrame()
			if(self.frame):
				yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n'+ self.frame + b'\r\n')
	def getTimeLapseWritersSpecs(self):
		if(not self.videoServer):
			return ("",204)
		return self.videoServer.getTimeLapseWritersSpecs()

	def togglePauseTimeLapseWriter(self,writerID):
		self.videoServer.togglePauseTimeLapseWriter(writerID)
		
class VideoServer:
	instance = None
	timeLapseWriters = {}
	MAX_TIMELAPSE_WRITERS = 10
	def __init__(self):
		self.imageHub = imagezmq.ImageHub()
		self.started = False
		VideoServer.instance = self

	# Singleton to initialize camera server only once	
	@classmethod
	def getSingleton(VideoServer):
		if(not VideoServer.instance):
			return VideoServer()
		return VideoServer.instance

	def stop(self):
		self.started = False

	def start(self):
		if(not self.started):
			self.started =True
			Thread(target= self.readFromWebcam, args=()).start()
		
	def readFromWebcam(self):
		while self.started:
			(rpiName, frame) = self.imageHub.recv_image()

			self.imageHub.send_reply(b'OK')
			if(frame is not None):
				self.frame = frame
				(self.frame_h, self.frame_w) = self.frame.shape[:2]
			
		cv2.destroyAllWindows()

	def getFrame(self):
		return self.frame

	def getEncodedFrame(self):
		if(not hasattr(self,"frame")):
			return None
		frame = cv2.resize(self.frame,(int(self.frame_w*1), int(self.frame_h*1)))
		return cv2.imencode('.jpeg',frame)[1].tostring()
	def record(self, outputSeconds = 10.0, fps = 10,timeBetweenFrames=1):
		if(self.started):
			Thread(target= self.recordThread, args=(outputSeconds , fps ,timeBetweenFrames)).start()

	def recordThread(self, outputSeconds = 10.0, fps = 10,timeBetweenFrames=1):
		if(not hasattr(self,"frame")):
			return
		if(len(self.getTimeLapseWriters()) < self.MAX_TIMELAPSE_WRITERS):
			specs = TimeLapseSpecs(outputSeconds,fps,timeBetweenFrames)
			timeLapseWriter = TimeLapseWriter(self,specs)
			self.addTimeLapseWriter(timeLapseWriter)
			timeLapseWriter.record()
	def addTimeLapseWriter(self,timeLapseWriter):
			writerID= timeLapseWriter.getSpecs()["id"]
			self.timeLapseWriters[writerID]=timeLapseWriter
	def getTimeLapseWriters(self):
		activeTimeLapseWriters ={}
		timeLapseWriters = self.timeLapseWriters
		for key in timeLapseWriters:
			writer = timeLapseWriters[key]
			specs = writer.getSpecs()
			if(specs["remainingTime"] > 0):
				activeTimeLapseWriters[key]= writer
		return activeTimeLapseWriters
	def getTimeLapseWritersSpecs(self):
		writersByID ={}
		timeLapseWriters = self.getTimeLapseWriters()
		for writer in timeLapseWriters.values():
			specs = writer.getSpecs()
			writersByID[specs["id"]] = specs
		return(writersByID)
		
	def timeLapseWriterExists(self,position):
		return position in self.timeLapseWriters.keys()
	def pauseTimeLapseWriter(self,position):
		if(self.timeLapseWriterExists(position)):
			self.timeLapseWriters[position].pause()
	def unPauseTimeLapseWriter(self,position):
		if(self.timeLapseWriterExists(position)):
			self.timeLapseWriters[position].unPause()
	def togglePauseTimeLapseWriter(self,position):
		if(self.timeLapseWriterExists(position)):
			print("yess")
			self.timeLapseWriters[position].togglePause()
		else:
			print("nooo")
	def stopTimeLapseWriter(self,position):
		if(self.timeLapseWriterExists(position)):
			self.timeLapseWriters[position].stop()
	
if __name__ == "__main__":
	video = VideoServer()
	video.start()