import cv2

cap = cv2.VideoCapture(1)

dictionary_name = cv2.aruco.DICT_4X4_50
dictionary = cv2.aruco.getPredefinedDictionary(dictionary_name)

while True:
    ret, frame = cap.read()

    #frame = cv2.resize(frame, (int(frame.shape[1]/3), int(frame.shape[0]/3)))

    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(frame, dictionary)
    frame = cv2.aruco.drawDetectedMarkers(frame, corners, ids)

    cv2.imshow('Edited Frame', frame)

    if ids is not None:
        for number, corner in zip(ids, corners):  
            print number, corner

    

    k = cv2.waitKey(1)
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
