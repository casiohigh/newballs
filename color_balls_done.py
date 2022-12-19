import cv2
import numpy as np
import random
import time

def color_range(h):
    return { h < 13: 'Red', 13 <= h < 80: 'Green', 80 <= h < 145: 'Blue', 145 <= h: 'Red'}[True]

def default_colors():
    colors = ['Red', 'Green', 'Blue']
    unclear = []
    while len(unclear) != 3:
        check = colors[random.randint(0, 2)]
        if check not in unclear:
            unclear.append(check)
    return(unclear)

if __name__ == '__main__':
    def callback(*arg):
        print (arg)

unclear = default_colors()
print(unclear)
cam = cv2.VideoCapture(0)
cv2.namedWindow("Image")

#blue
lower_1 = np.array([95, 70, 140])
upper_1 = np.array([105, 255, 255])

#green
lower_2 = np.array([50, 20, 120])
upper_2 = np.array([90, 120, 255])

#red
lower_3 = np.array([170, 100, 90])
upper_3 = np.array([255, 255, 255])


pixel = None
while cam.isOpened():
    _, frame = cam.read()
    frame = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask_1 = cv2.inRange(hsv, lower_1, upper_1)
    mask_2 = cv2.inRange(hsv, lower_2, upper_2)
    mask_3 = cv2.inRange(hsv, lower_3, upper_3)

    masks = mask_1 + mask_2 + mask_3

    # contours_1, _ = cv2.findContours(mask_1, cv2.RETR_EXTERNAL,
    #                                 cv2.CHAIN_APPROX_SIMPLE)
    # contours_2, _ = cv2.findContours(mask_2, cv2.RETR_EXTERNAL,
    #                                 cv2.CHAIN_APPROX_SIMPLE)
    # contours_3, _ = cv2.findContours(mask_3, cv2.RETR_EXTERNAL,
    #                                 cv2.CHAIN_APPROX_SIMPLE)

    contours, _ = cv2.findContours(masks.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    data = {}

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            (x, y, w, h) = cv2.boundingRect(cnt)
            cv2.circle(frame, ((x+x+w)//2, (y+y+h)//2), 4, (0,255,0), -1)
            hsv_color = hsv[(y+y+h)//2, (x+x+w)//2][0]
            color = color_range(hsv_color)

            data[color] = x
            cv2.imshow("Background", masks)
    cv2.imshow("Image", frame)

    if len(data) > 2:
        sorted_data = {}
        sorted_keys = sorted(data, key=data.get)  
        for srt_k in sorted_keys:
            sorted_data[srt_k] = data[srt_k]

        showed_colors = list(sorted_data)

        if (unclear == showed_colors):
            # cv2.putText(frame, f"You're right", (10, 30), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 0))
            print("Right")
            time.sleep(1)
            break
        else:
            print("Not Right")
            time.sleep(1)
            # cv2.putText(frame, f"Incorrect, try again", (10, 30), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 0))

    key = cv2.waitKey(50)
    if key == ord('q'):
        break
 
cam.release()
cv2.destroyAllWindows()