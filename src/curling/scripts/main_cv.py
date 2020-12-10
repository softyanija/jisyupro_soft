import numpy as np
import cv2


H_MARGIN = 30
W_MARGIN = 40

HEIGHT = 720
WIDTH = 960

S_H = 480
S_W = 640

img = np.full((HEIGHT + 2*H_MARGIN, WIDTH + 2*W_MARGIN, 3), 0,dtype = np.uint8)

#def make_board(board):
    


if __name__ == '__main__':

    WIN_NAME = 'GAME'

    cv2.namedWindow(WIN_NAME, cv2.WINDOW_AUTOSIZE)
    #cv2.imshow()

    
    while True:
        cv2.rectangle(img, (W_MARGIN, H_MARGIN), (W_MARGIN+S_W, H_MARGIN+S_H), (255, 255, 255))
        cv2.imshow(WIN_NAME,img )
        k = cv2.waitKey(1)
        
        if k == 27:
             break

    cv2.destroyAllWindows()
             
