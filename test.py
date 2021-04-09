import cv2
import numpy as np

def CircleDetect2():  # bolb
    # cv2.setMouseCallback('org', mouse_callback)
    cap = cv2.VideoCapture(0)

    while True:
        global frame
        ret, frame = cap.read()

        if not ret:
            break

        roi_gray = np.zeros((300, 500), np.uint8)  # 영역자르기
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  #  흑백영상으로
        cut = gray[300:600, 350:850]  # 흑백영상 자르기
        roi_gray[0:300, 0:500] = cut

        ret, th1 = cv2.threshold(frame, 125, 255, cv2.THRESH_BINARY)  # 특징잡기
        ret, roi_th1 = cv2.threshold(roi_gray, 125, 255, cv2.THRESH_BINARY)

        params = cv2.SimpleBlobDetector_Params()

        params.filterByInertia = True
        params.minInertiaRatio = 0.01

        detector = cv2.SimpleBlobDetector_create()
        keypoints = detector.detect(roi_gray)

        cv2.rectangle(th1, (350, 300), (850, 600), (0, 0, 255), 3)

        im_with_keypoints = cv2.drawKeypoints(roi_th1, keypoints, np.array([]), (0, 0, 255),
                                              cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)  # 원찾기
        # print(im_with_keypoints)

        iwk = cv2.cvtColor(im_with_keypoints, cv2.COLOR_BGR2GRAY)
        #contours, hierarchy = cv2.findContours(iwk, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #for c in contours:
            # calculate moments for each contour
            # M = cv2.moments(c)

            # calculate x,y coordinate of center
            # cX = int(M["m10"] / M["m00"])
            # cY = int(M["m01"] / M["m00"])

            # cv2.circle(im_with_keypoints, (cX, cY), 5, (255, 255, 255), -1)
            # cv2.putText(im_with_keypoints, "centroid", (cX - 25, cY - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        # print('============   key points   =========== {}')
        # print(keypoints)

        cv2.imshow('bef', th1)
        cv2.imshow('KeyPoints', im_with_keypoints)

        if cv2.waitKey(1) & 0xff == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

CircleDetect2()