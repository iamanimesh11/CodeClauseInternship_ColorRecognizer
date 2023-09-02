import cv2
import numpy as np
import pandas as pd

# Load color information from CSV
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names=index, header=None)

def getColorName(R, G, B):
    minimum = 10000
    color_name = ""
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            color_name = csv.loc[i, "color_name"]
    return color_name

def draw_function(event, x, y, flags, param):
    global b, g, r, xpos, ypos
    xpos = x
    ypos = y
    b, g, r = frame[y, x]
    b = int(b)
    g = int(g)
    r = int(r)

xpos, ypos = 0, 0  # Initialize xpos and ypos
r, g, b = 0, 0, 0  # Initialize r, g, b

cv2.namedWindow('Color Detection')
cv2.setMouseCallback('Color Detection', draw_function)

text_color = (255, 255, 255)  # Fixed text color (white)

# Open the camera
cap = cv2.VideoCapture("http://192.168.1.6:8080/video")  # 0 corresponds to the default camera

while True:
    ret, frame = cap.read()  # Read a frame from the camera

    if not ret:
        break

    frame = cv2.resize(frame, (700, 500))

    color_name = getColorName(r, g, b)
    text = f"Color: {color_name}\nR={r} G={g} B={b}"

    # Display color swatch
    swatch = np.zeros((50, 50, 3), dtype=np.uint8)
    swatch[:, :] = [b, g, r]
    cv2.putText(swatch, color_name, (5, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.4, text_color, 1, cv2.LINE_AA)

    # Update swatch position based on cursor position
    swatch_x = max(10, xpos - 25)
    swatch_y = min(frame.shape[0] - 60, ypos + 20)  # Adjusted swatch position below cursor
    frame[swatch_y:swatch_y+50, swatch_x:swatch_x+50] = swatch

    cv2.putText(frame, text, (70, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, text_color, 2, cv2.LINE_AA)

    cv2.imshow("Color Detection", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()  # Release the camera
cv2.destroyAllWindows()
