import cv2
import mediapipe as mp
from cv2.gapi.wip import draw
import util
import pyautogui
from pynput.mouse import Button, Controller
mouse = Controller()

screen_width, screen_height = pyautogui.size()  # to take screen size
draw = mp.solutions.drawing_utils  # draw the points of finger position
mpHands = mp.solutions.hands  # hand features from mediapipe as mpHands
hands = mpHands.Hands(
  static_image_mode=False,  # false coz we are cpturing video
  model_complexity=1,       # to get a better model
  min_detection_confidence=0.7,  # the minimum detection confidence score required is 70%
  min_tracking_confidence=0.7,   # the minimum tracking confidence required is 70%
  max_num_hands=1           # number of hands to recognize is 1
)

def move_mouse(index_finger_tip):   #to move the mouse pointer
    if index_finger_tip is not None:  # to get the index finger tip position
        x = int(index_finger_tip.x * screen_width*1.8)  # measuring index finger tip position for x axis on the screen through camera
        y = int(index_finger_tip.y * screen_height*1.8)  # measuring index finger tip position for y axis on the screen through camera
        pyautogui.moveTo(x,y) # moving the cursor along with thw index finger tip position on the screen

def is_left_click(landmarks_list, thumb_index_dist):  #left click on mouse
    return (util.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8])<50 and  # calculating the angle or bent of index finger while middle fingre is stright and thumb is open.
        util.get_angle(landmarks_list[9], landmarks_list[10], landmarks_list[12]) > 90 and
        thumb_index_dist > 50
    )

def is_right_click(landmarks_list, thumb_index_dist):
    return (
        util.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8])>90 and   # calculating the angle or bent of middle finger while index fingre is stright and thumb is open. to right click.
        util.get_angle(landmarks_list[9], landmarks_list[10], landmarks_list[12]) < 50 and
        thumb_index_dist > 50
    )
def is_double_click(landmarks_list, thumb_index_dist):
    return (
        util.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8])<50 and  # calculating the angle or bent of index finger along with middle fingre and thumb is open. to double click
        util.get_angle(landmarks_list[9], landmarks_list[10], landmarks_list[12]) < 50 and
        thumb_index_dist > 50
    )
def is_screenshot(landmarks_list, thumb_index_dist):
    return (
        util.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8])<50 and  # closing the all fingers to take a screenshot.
        util.get_angle(landmarks_list[9], landmarks_list[10], landmarks_list[12]) < 50 and
        util.get_angle(landmarks_list[13], landmarks_list[14], landmarks_list[16]) < 50 and
        util.get_angle(landmarks_list[17], landmarks_list[18], landmarks_list[20]) < 50 and
        thumb_index_dist < 50
    )
def is_down_scroll(landmarks_list, thumb_index_dist): # bending the ring finger to scroll down while other fingers are stright and thub is open
    return (      util.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8])>50 and
        util.get_angle(landmarks_list[9], landmarks_list[10], landmarks_list[12]) > 50 and
        util.get_angle(landmarks_list[13], landmarks_list[14], landmarks_list[16]) < 50 and
        util.get_angle(landmarks_list[17], landmarks_list[18], landmarks_list[20]) > 50 and
        thumb_index_dist > 50
    )
def is_up_scroll(landmarks_list, thumb_index_dist): # bending the pinky finger to scroll up while other fingers are stright and thub is open
    return (      util.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8])>50 and
        util.get_angle(landmarks_list[9], landmarks_list[10], landmarks_list[12]) > 50 and
        util.get_angle(landmarks_list[13], landmarks_list[14], landmarks_list[16]) > 50 and
        util.get_angle(landmarks_list[17], landmarks_list[18], landmarks_list[20]) < 50 and
        thumb_index_dist > 50
    )

def find_finger_tip(processed):   #to find the finger tip
  if processed.multi_hand_landmarks:  # only one hand should be recognise if multiple hand detected
    hand_landmarks = processed.multi_hand_landmarks[0]
    return hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP] # get the hand landmark from mediapipe
  return None

def detect_gestures(frame, landmarks_list, processed):
    if len(landmarks_list) >= 21:  # to get all 21 hand landmarks 0 to 20
        index_finger_tip = find_finger_tip(processed) # to locate the index finger tip
        thumb_index_dist = util.get_distance([landmarks_list[4], landmarks_list[5]]) # to get the thumb distance from palm.

        if thumb_index_dist < 40 and util.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8])>90:  # if thumb is open (thumb tip distance from palm is more than 40) and index finger is stright (angle >90 degree)
            move_mouse(index_finger_tip)   # move the cursor along with the index finger tip
        elif is_left_click(landmarks_list, thumb_index_dist): #for left click
            mouse.press(Button.left)
            cv2.putText(frame, "Left Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)  # print on the frame as left click
        elif is_right_click(landmarks_list, thumb_index_dist): #for right click
            mouse.press(Button.right)
            cv2.putText(frame, "Right Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)  # print on the frame as right click
        elif is_double_click(landmarks_list, thumb_index_dist): # for double click
            pyautogui.doubleClick()
            cv2.putText(frame, "Double Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2) # print on the frame as double click
        elif is_screenshot(landmarks_list, thumb_index_dist): # to take screenshot
            pyautogui.screenshot('my_screenshot.png')
            cv2.putText(frame, "Screenshot", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)  # print on the frame as screenshot
        elif is_down_scroll(landmarks_list, thumb_index_dist): # to scroll down
            mouse.scroll(0, 2)
            cv2.putText(frame, "Scroll Down", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2) # print on the frame as Scroll Down
        elif is_up_scroll(landmarks_list, thumb_index_dist): # to scroll up
            mouse.scroll(0, -2)
            cv2.putText(frame, "Scroll Up", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2) # print on the frame as Scroll Up


def main():
  cap = cv2.VideoCapture(0)   #to capture video from a single camera

  try:
    while cap.isOpened():      #checking the camera is capturing or not
      ret, frame = cap.read()  #we are reading the video frame by frame. ret returns a boolean value(true or false). frame contains the frame
      if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
      frame = cv2.flip(frame, 1)  #to flip the capturing image for better understanding

      frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # to convert the color to RGB formate on frame
      processed = hands.process(frameRGB)  # to get the color as RGB formate on frame
      landmarks_list = []  # hand landmarks array 21 points landmark in total
      if processed.multi_hand_landmarks:
        hand_landmarks = processed.multi_hand_landmarks[0] # only one hand landmarks are considered if both  the hands are detected

        draw.draw_landmarks(frame, hand_landmarks, mpHands.HAND_CONNECTIONS)  # to draw the lines on hand image on each frame.
        for lm in hand_landmarks.landmark:
          landmarks_list.append((lm.x, lm.y)) # appending all the landmarks to the landmaek list

      detect_gestures(frame, landmarks_list, processed)  # to detect the hand genture


      cv2.imshow('frame', frame)  # to show the capture
      if cv2.waitKey(1) & 0xFF == ord('q'):  #waiting for 1 milisecond after each frame is read and if the keyboard input is 'q' (0xFF will take ascii value of q) then break and end the loop of capturing
        break
  finally:
    cap.release()                 # close the camera
    cv2.destroyAllWindows()       # destroy all windows that created by open cv

if __name__ == '__main__':        #this functiion will only run if we run this file and cannot run from any other file.
    main()
