# Virtual-Mouse-Controlled-by-hand-gestures-using-OpenCV-
## Overview

This project implements a hand gesture-based mouse control system using OpenCV, MediaPipe, and PyAutoGUI. The system detects hand gestures through a webcam and maps them to mouse actions such as movement, clicks, scrolling, and taking screenshots.

## Features

Move Mouse Cursor: Moves the cursor based on the index finger tip position.

Left Click: Bends the index finger while the middle finger remains straight.

Right Click: Bends the middle finger while the index finger remains straight.

Double Click: Bends both the index and middle fingers simultaneously.

Screenshot: Closes all fingers to take a screenshot.

Scroll Down: Bends the ring finger while others remain straight.

Scroll Up: Bends the pinky finger while others remain straight.

## Prerequisites

Ensure you have the following dependencies installed:

opencv-python, mediapipe, pyautogui and pynput

## Usage

Run the script using:

vmouse.py

Make sure your webcam is enabled.

Use hand gestures to control the mouse.

Press q to exit the program.

## How It Works

Captures video using OpenCV.

Uses MediaPipe to detect hand landmarks.

Maps detected gestures to specific mouse actions.

Executes actions using PyAutoGUI and Pynput.

## Functions

move_mouse(index_finger_tip): Moves the cursor based on index finger position.

is_left_click(landmarks_list, thumb_index_dist): Detects left-click gesture.

is_right_click(landmarks_list, thumb_index_dist): Detects right-click gesture.

is_double_click(landmarks_list, thumb_index_dist): Detects double-click gesture.

is_screenshot(landmarks_list, thumb_index_dist): Detects screenshot gesture.

is_down_scroll(landmarks_list, thumb_index_dist): Detects scroll-down gesture.

is_up_scroll(landmarks_list, thumb_index_dist): Detects scroll-up gesture.

detect_gestures(frame, landmarks_list, processed): Analyzes hand gestures and triggers corresponding mouse actions.
