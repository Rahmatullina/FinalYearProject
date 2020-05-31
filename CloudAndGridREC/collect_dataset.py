import imutils
import time
import cv2
import os

# load OpenCV's Haar cascade for face detection from disk
detector = cv2.CascadeClassifier('../haarcascade_frontalface_default.xml')
# initialize the video stream, reding the video file
vs = cv2.VideoCapture('people_videos/emiliyaVideo.mp4')
#number of captured images from video
total = 0
# loop over the frames from the video stream
while vs.isOpened():
    # grab the frame from the threaded video stream, clone it and
    # then resize the frame so we can apply face detection faster
    success, frame = vs.read()
    orig = frame[:]
    frame = imutils.resize(frame, width=400, height=400)

    # detect faces in the grayscale frame
    rects = detector.detectMultiScale(
        cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), scaleFactor=1.1,
        minNeighbors=5, minSize=(30, 30))

    # loop over the face detections and draw them on the frame
    for (x, y, w, h) in rects:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # show the output frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the `k` key was pressed, write the *original* frame to disk
    # so we can later process it and use it for face recognition
    person_id = 1
    if key == ord("k"):
        p = os.path.sep.join(['CloudAndGridREC/dataset/{}'.format(person_id),
                             "{}.png".format(str(total).zfill(5))])
        cv2.imwrite(p, orig)
        total += 1

    # if the `q` key was pressed, break from the loop
    elif key == ord("q"):
        break
# print the total faces saved and do a bit of cleanup
print("[INFO] {} face images stored".format(total))
print("[INFO] cleaning up...")
vs.release()
cv2.destroyAllWindows()





