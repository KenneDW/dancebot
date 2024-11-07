import cv2 as cv
# Note that the below code was AI-generated, replace with actual code

# Open the video file
video = cv.VideoCapture("dvd.mp4")

# Check if the video opened successfully
if not video.isOpened():
    print("Error opening video file")

# Read the first frame
ret, frame = video.read()

# Save the frame as an image
if ret:
    cv.imwrite("frame.jpg", frame)

# Release the video object
video.release()