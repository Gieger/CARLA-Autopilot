# Farhzeug.py
# Author: Dennis Gieger

#Klasse zum Bereitstellen des Kamerabildes
import time
import numpy as np
import cv2



    



class USB_kamera():
    name = "USB-Kamera"
	
	#Kamera initialisierung
    def __init__(self, airsim):
        self.cameraType = "scene"
        self.cameraTypeMap = { 
            "depth": airsim.ImageType.DepthVis,
            "segmentation": airsim.ImageType.Segmentation,
            "seg": airsim.ImageType.Segmentation,
            "scene": airsim.ImageType.Scene,
            "disparity": airsim.ImageType.DisparityNormalized,
            "normals": airsim.ImageType.SurfaceNormals
            }

        self.airsim = airsim
        self.client = self.airsim.CarClient()

        self.frame = None
        self.programm_laeuft = True

	#Endlosschleife für das Abgreifen der Bilder von der Kamera
    def aktualisieren(self):
        while self.programm_laeuft:
            rawImage = self.client.simGetImage("0", self.cameraTypeMap[self.cameraType])

            img1d = cv2.imdecode(self.airsim.string_to_uint8_array(rawImage), cv2.IMREAD_UNCHANGED)
            self.frame = img1d

    def ausfuehren_parallel(self):
        return self.frame

	# Thread beenden
    def beenden(self):
        self.programm_laeuft = False
        print('Kamera beenden')
        time.sleep(.5)