import numpy as np

def get_angle(a, b, c):
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])  # first we are calculating the angle between ab and x-axis and substract it from angle between extended bc and x-axis
    angle = np.abs(np.degrees(radians))   # to convert radian to degree
    return angle

def get_distance(landmark_list):        #to get the distance between two points
    if len(landmark_list)<2:   # atleast two landmarks are there to calculate the distance
        return
    (x1,y1),(x2,y2) = landmark_list[0], landmark_list[1]
    L = np.hypot(x2-x1, y2-y1)          #distance calculation
    return np.interp(L,[0,1], [0,1000])