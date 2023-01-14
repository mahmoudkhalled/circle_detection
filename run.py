import numpy as np
import math
import cv2
import os
from google.colab.patches import cv2_imshow
dir = '/content/images'
for i in os.listdir(dir):
  print (i)
  image = cv2.imread(dir+'/'+i, cv2.IMREAD_COLOR)
  gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  gray_image_blurred =  cv2.blur(gray_image, (3, 3))
  # Apply Hough transform on the blurred image.
  detected_circles = cv2.HoughCircles(gray_image_blurred,
          cv2.HOUGH_GRADIENT, 1, 20, param1 = 130,
        param2 = 30, minRadius = 200, maxRadius = 270)
  if detected_circles is not None:
    # Convert the circle parameters a, b and r to integers.
    detected_circles = np.uint16(np.around(detected_circles))
    a, b, r = detected_circles[0][0][0], detected_circles[0][0][1], detected_circles[0][0][2]
    print(r)
    start_point = (int(detected_circles[0][0][0]- detected_circles[0][0][2]*math.sqrt(2)/2 ) ,int(detected_circles[0][0][1]- detected_circles[0][0][2]*math.sqrt(2)/2 ))
    end_point = (int(detected_circles[0][0][0]+ detected_circles[0][0][2]*math.sqrt(2)/2 ) ,int(detected_circles[0][0][1]+ detected_circles[0][0][2]*math.sqrt(2)/2 ))
    # Draw the circumference of the circle.
    cv2.circle(image, (a, b), r, (0, 0, 255), 4)
    cv2.rectangle(image, start_point, end_point, (0, 255, 0), 4)
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = f'{end_point[0]- start_point[0]}px X {end_point[1]- start_point[1]}px'
    textsize = cv2.getTextSize(text, font, 1, 2)[0]
    print(textsize)
    # get coords based on boundary
    #textX = (image.shape[1] - textsize[0]) / 2
    textX = (a - (textsize[0]/2)) 
    textY = (start_point[1]-textsize[1])
    org = (int(textX),int(textY))
    cv2.putText(image, text, org, font, 1, (255, 0, 0), 2, cv2.LINE_AA)
    # Draw a small circle (of radius 1) to show the center.
    cv2.circle(image, (a, b), 1, (0, 0, 0), 3)
    cv2.imwrite(f'/content/outp/{i}',image)
