
from datetime import datetime
import cv2
import os

class TimeLapseWriter:
	paused = True
	def __init__(self,videoServer,specs):
		self.specs = specs
		self.videoServer = videoServer
		self.frameSize = (videoServer.frame_w,videoServer.frame_h)
		#fourcc = cv2.VideoWriter_fourcc('X','V','I','D')# for .avi
		#self.fourcc = cv2.VideoWriter_fourcc(*'MP4V')# for .mp4
		#self.fourcc = cv2.VideoWriter_fourcc('F','M','P','4')# for .mp4
		self.fourcc = cv2.VideoWriter_fourcc(*'VP80')# for .webm
		self.timeLapseTimer = TimeLapseTimer(self.specs)
		if not os.path.exists('static/media/'):
			os.makedirs('static/media/')
		fps = self.specs["fps"]
		speed = self.specs["speed"]
		self.filename = "static/media/"+self.timeLapseTimer.getFormattedStartTime()+"x"+speed+"-"+fps+'fps.webm'
		self.videoWriter = cv2.VideoWriter(self.filename,self.fourcc, self.specs.fps, self.frameSize)

	def record(self):
		self.paused = False
		while (not self.timeLapseTimer.isOver()):
			self.recordFrame()
		self.videoWriter.release()

	def recordFrame(self):
		if(self.paused):
			return
		if(self.timeLapseTimer.isReady()):
			self.timeLapseTimer.updateRemainingTime()
			self.videoWriter.write(self.videoServer.getFrame())
		self.timeLapseTimer.updateDeltaTime()

	def togglePause(self):
		if(self.paused):
			self.unPause()
			return
		self.pause()
	def pause(self):
		self.paused = True
	def unPause(self):
		self.paused	= False
		self.timeLapseTimer.unPause()
	def stop(self):
		self.timeLapseTimer.end()
	def getSpecs(self):
		specs= self.timeLapseTimer.getSpecs()
		specs["paused"] = self.paused
		return specs

class TimeLapseTimer:
	instances = 0
	def __init__(self,specs):
		TimeLapseTimer.instances +=1
		self.instanceID=TimeLapseTimer.instances
		self.specs= specs
		self.remainingTime = self.specs.realRecordingDuration 
		self.startTime = datetime.now()
		self.lastTime = self.startTime
		self.actualTime=self.lastTime
		self.deltaTime= 0.0
		self.ready=True

	def getStartTime(self):
		return self.startTime

	def getFormattedStartTime(self):
		return self.getStartTime().strftime("%Y-%m-%d-%H:%M:%S")

	def calculateDeltaTime(self):
		self.actualTime =  datetime.now()
		deltaTime =(self.actualTime- self.lastTime).total_seconds()
		return deltaTime

	def updateDeltaTime(self):
		localDeltatime = self.calculateDeltaTime()
		self.lastTime =self.actualTime
		self.remainingTime -=localDeltatime
		self.deltaTime += localDeltatime
		if(self.deltaTime >= self.specs.timeBetweenFrames):
			self.ready= True

	def updateRemainingTime(self):
		self.debugTimer()
		self.deltaTime= 0
		self.ready= False
		
	def isOver(self):
		return (self.remainingTime <= 0)

	def isReady(self):
		return self.ready
	def end(self):
		self.remainingTime = 0
	def debugTimer(self):
		print("timer number %d, time remaining: %8.2f, deltaTime: %8.2f" % (self.instanceID,self.remainingTime,self.deltaTime))
	def __str__(self):
		outputString = str(self.specs)
		outputString += " remaing recording time: " + str(self.remainingTime)
	def getSpecs(self):
		specsDict = self.specs.getSpecs()
		specsDict["remainingTime"] = self.remainingTime
		specsDict["id"] = self.instanceID
		return specsDict
	def unPause(self):
		self.lastTime = datetime.now()

class TimeLapseSpecs:
	def __init__(self, outputSeconds,fps,timeBetweenFrames):
		self.outputSeconds= outputSeconds
		self.fps = fps
		self.timeBetweenFrames = timeBetweenFrames
		self.realRecordingDuration = self.outputSeconds * self.fps * self.timeBetweenFrames
		self.speed= self.fps* self.timeBetweenFrames
	def getSpecs(self):
		return self.__dict__
	def __str__(self):
		outputString = "Specs: "
		outputString += " video duration: "+ str(self.outputSeconds)
		outputString += " frames per second: " + str(self.fps)
		outputString += " recording duration: " + str(self.realRecordingDuration)
		outputString += " real time between frames: " + str(self.timeBetweenFrames)
		return outputString
