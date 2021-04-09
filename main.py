import cv2
import numpy as np


def nothing(x):
    pass


def CircleDetect():
    cap = cv2.VideoCapture(0)

    cv2.namedWindow('Trackbars')
    cv2.createTrackbar('L-H', 'Trackbars', 0, 180, nothing)
    cv2.createTrackbar('L-S', 'Trackbars', 66, 255, nothing)
    cv2.createTrackbar('L-V', 'Trackbars', 134, 255, nothing)
    cv2.createTrackbar('U-H', 'Trackbars', 180, 180, nothing)
    cv2.createTrackbar('U-S', 'Trackbars', 255, 255, nothing)
    cv2.createTrackbar('U-V', 'Trackbars', 243, 255, nothing)

    font = cv2.FONT_HERSHEY_COMPLEX

    while True:
        _, frame = cap.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        l_h = cv2.getTrackbarPos('L-H', 'Trackbars')
        l_s = cv2.getTrackbarPos('L-S', 'Trackbars')
        l_v = cv2.getTrackbarPos('L-V', 'Trackbars')
        u_h = cv2.getTrackbarPos('U-H', 'Trackbars')
        u_s = cv2.getTrackbarPos('U-S', 'Trackbars')
        u_v = cv2.getTrackbarPos('U-V', 'Trackbars')

        lower_red = np.array([l_h, l_s, l_v])
        upper_red = np.array([u_h, u_s, u_v])

        mask = cv2.inRange(hsv, lower_red, upper_red)
        kernel = np.ones((5,5), np.uint8)
        mask = cv2.erode(mask, kernel)

        print(mask)

        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            area = cv2.contourArea(cnt)
            approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
            x = approx.ravel()[0]
            y = approx.ravel()[1]

            if area > 400:
                cv2.drawContours(frame, [approx], 0, (0, 0, 0), 5)

                if 10 < len(approx) < 20:
                    cv2.putText(frame, "Circle", (x, y), font, 1, (0, 0, 0))

        cv2.imshow("Frame", frame)
        cv2.imshow("Mask", mask)

        if cv2.waitKey(1) == 27 &0xff:
            break

    cap.release()
    cv2.destroyAllWindows()


hsv = 0
lower_blue1 = 0
upper_blue1 = 0
lower_blue2 = 0
upper_blue2 = 0
lower_blue3 = 0
upper_blue3 = 0


def mouse_callback(event, x, y, flags, param):
    global frame
    if event == cv2.EVENT_LBUTTONDOWN:
        #print(frame[y, x])
        color = frame[y, x]

        one_pixel = np.uint8([[color]])
        hsv = cv2.cvtColor(one_pixel, cv2.COLOR_BGR2HSV)
        hsv = hsv[0][0]

        if hsv[0] < 10:
            print('case1')
            lower_blue1 = np.array([hsv[0]-10+180, 30, 30])
            upper_blue1 = np.array([180, 255, 255])
            lower_blue2 = np.array([0, 30, 30])
            upper_blue2 = np.array([hsv[0], 255, 255])
            lower_blue3 = np.array([hsv[0], 30, 30])
            upper_blue3 = np.array(hsv[0]+10, 255, 255)

        elif hsv[0] > 170:
            print("case2")
            lower_blue1 = np.array([hsv[0], 30, 30])
            upper_blue1 = np.array([180, 255, 255])
            lower_blue2 = np.array([0, 30, 30])
            upper_blue2 = np.array([hsv[0] + 10 - 180, 255, 255])
            lower_blue3 = np.array([hsv[0] - 10, 30, 30])
            upper_blue3 = np.array([hsv[0], 255, 255])
            #     print(i, 180, 0, i+10-180)
            #     print(i-10, i)
        else:
            print("case3")
            lower_blue1 = np.array([hsv[0], 30, 30])
            upper_blue1 = np.array([hsv[0] + 10, 255, 255])
            lower_blue2 = np.array([hsv[0] - 10, 30, 30])
            upper_blue2 = np.array([hsv[0], 255, 255])
            lower_blue3 = np.array([hsv[0] - 10, 30, 30])
            upper_blue3 = np.array([hsv[0], 255, 255])

        print(hsv[0])
        print("@1", lower_blue1, "~", upper_blue1)
        print("@2", lower_blue2, "~", upper_blue2)
        print("@3", lower_blue3, "~", upper_blue3)


def CircleDetect2():  #bolb
    cv2.namedWindow('tb')
    # cv2.setMouseCallback('org', mouse_callback)
    cap = cv2.VideoCapture(0)

    while True:
        global frame
        ret, frame = cap.read()

        if not ret:
            break

        roi_gray = np.zeros((300, 500), np.uint8)

        '''copy = frame.copy()
        cv2.createTrackbar('low H', 'tb', 10, 180, nothing)
        cv2.createTrackbar('low S', 'tb', 180, 255, nothing)
        cv2.createTrackbar('low V', 'tb', 50, 255, nothing)
        cv2.createTrackbar('high H', 'tb', 25, 180, nothing)
        cv2.createTrackbar('high S', 'tb', 200, 255, nothing)
        cv2.createTrackbar('high V', 'tb', 200, 255, nothing)
        
        cv2.setTrackbarPos('low H', 'tb', 50)
        cv2.setTrackbarPos('low S', 'tb', 150)
        cv2.setTrackbarPos('low V', 'tb', 250)
        cv2.setTrackbarPos('high H', 'tb', 350)
        cv2.setTrackbarPos('high S', 'tb', 450)
        cv2.setTrackbarPos('high V', 'tb', 550)

        img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # img_mask1 = cv2.inRange(img_hsv, lower_blue1, upper_blue1)
        # img_mask2 = cv2.inRange(img_hsv, lower_blue2, upper_blue2)
        # img_mask3 = cv2.inRange(img_hsv, lower_blue3, upper_blue3)
        # img_mask = img_mask1 | img_mask2 | img_mask3


        l_h = cv2.getTrackbarPos('low H', 'tb')
        l_s = cv2.getTrackbarPos('low S', 'tb')
        l_v = cv2.getTrackbarPos('low V', 'tb')

        h_h = cv2.getTrackbarPos('high H', 'tb')
        h_s = cv2.getTrackbarPos('high S', 'tb')
        h_v = cv2.getTrackbarPos('high V', 'tb')

        # img_mask = cv2.inRange(img_hsv, (l_h, l_s, l_v), (h_h, h_s, h_v))
        # img_mask = cv2.inRange(img_hsv, (10, 180, 20), (25, 255, 255))
        # img_result = cv2.bitwise_and(frame, frame, mask=img_mask)  '''

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cut = gray[300:600, 350:850]
        roi_gray[0:300, 0:500] = cut

        ret, th1 = cv2.threshold(frame, 125, 255, cv2.THRESH_BINARY)
        ret, roi_th1 = cv2.threshold(roi_gray, 125, 255, cv2.THRESH_BINARY)

        params = cv2.SimpleBlobDetector_Params()

        params.filterByInertia = True
        params.minInertiaRatio = 0.01

        detector = cv2.SimpleBlobDetector_create()
        keypoints = detector.detect(roi_gray)

        cv2.rectangle(frame, (350, 300), (850, 600), (0, 0, 255), 3)

        im_with_keypoints = cv2.drawKeypoints(roi_th1, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        #print(im_with_keypoints)

        '''iwk = cv2.cvtColor(im_with_keypoints, cv2.COLOR_BGR2GRAY)
        M = cv2.moments(iwk)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        cv2.circle(im_with_keypoints, (cX, cY), 5, (255, 0, 0), 2)
        cv2.putText(im_with_keypoints, "centroid", (cX - 25, cY - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)'''


        iwk = cv2.cvtColor(im_with_keypoints, cv2.COLOR_BGR2GRAY)
        contours, hierarchy = cv2.findContours(iwk, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            # calculate moments for each contour
            M = cv2.moments(c)

            # calculate x,y coordinate of center
            #cX = int(M["m10"] / M["m00"])
            #cY = int(M["m01"] / M["m00"])

            #cv2.circle(im_with_keypoints, (cX, cY), 5, (255, 255, 255), -1)
            #cv2.putText(im_with_keypoints, "centroid", (cX - 25, cY - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        #print('============   key points   =========== {}')
        #print(keypoints)

        cv2.imshow('KeyPoints', im_with_keypoints)
        cv2.imshow('org', frame)
        #cv2.imshow('org', th1)


        if cv2.waitKey(1) &0xff == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


CircleDetect2()


