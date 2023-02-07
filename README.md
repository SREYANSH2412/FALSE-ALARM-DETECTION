# FALSE_ALARM_DETECTION_SBP
A github repository for stuck between pixels

➡️Camera rotator
   -Prepare the hardware first using esp8266, pcb boards, A4988 stepper motor, 8mm to 5mm coupler for nema 17 motor, nema 17 motor
   -use rotator.py for working of camera rotator

➡️Object Detection
   -Copy the Yolo v5 repository
   -Copy person detection and tracking repository
    https://github.com/ambakick/Person-Detection-and-Tracking
   -Replace Detector.py and Person_det_track.py
   
➡️Face recognition
   -In AWK, in the S3 bucket put the images of persons and make Amazon rekognition working
   -use facerecognition.py to implement face recognition
