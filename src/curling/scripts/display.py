import cv2
import numpy as np

cap = cv2.VideoCapture(0)

dictionary_name = cv2.aruco.DICT_4X4_50
dictionary = cv2.aruco.getPredefinedDictionary(dictionary_name)

def getmarkers(ids,corners):
    if ids is not None:
        for i, id in enumerate(ids):
            v = np.mean(corners[i][0],axis=0)
            #return [v[0],v[1]]
            print(id[0],v[0],v[1])
        
    return None
    

while True:
    ret, frame = cap.read()

    #frame = cv2.resize(frame, (int(2*frame.shape[1]), int(2*frame.shape[0])))

    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(frame, dictionary)
    frame = cv2.aruco.drawDetectedMarkers(frame, corners, ids)
    cv2.imshow('Edited Frame', frame)
    '''
    if ids is not None:
        for number, corner in zip(ids, corners):  
            print number, corner
    '''

    getmarkers(ids, corners)
    

    k = cv2.waitKey(1)
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
