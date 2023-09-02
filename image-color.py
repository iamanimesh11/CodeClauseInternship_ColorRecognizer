import cv2
import numpy as np
import pandas as pd

img_path = "img.png"
img = cv2.imread(img_path)
img = cv2.resize(img, (700, 500))

r = g = b = xpos = ypos = 0

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
    b, g, r = img[y, x]
    b = int(b)
    g = int(g)
    r = int(r)


cv2.namedWindow('Colors Recognizer')
cv2.setMouseCallback('Colors Recognizer', draw_function)

text_color = (255, 255, 255)  # Fixed text color (white)

while True:
    img_copy = img.copy()

    color_name = getColorName(r, g, b)
    text = f"{color_name} R={r} G={g} B={b}"

    # Calculate text size to ensure it fits within the image window
    text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)

    # Adjust text position to fit within the image window
    if xpos + text_size[0] > img.shape[1]:
        xpos = img.shape[1] - text_size[0]
    if ypos - text_size[1] < 0:
        ypos = text_size[1]

    cv2.putText(img_copy, text, (xpos, ypos), cv2.FONT_HERSHEY_SIMPLEX, 0.8, text_color, 2, cv2.LINE_AA)

    # Display color swatch
    swatch = np.zeros((50, 50, 3), dtype=np.uint8)
    swatch[:, :] = [b, g, r]
    cv2.putText(swatch, color_name, (5, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.4, text_color, 1, cv2.LINE_AA)

    # Update swatch position based on cursor position
    swatch_x = max(10, xpos - 25)
    swatch_y = min(img.shape[0] - 60, ypos + 20)  # Adjusted swatch position below cursor
    img_copy[swatch_y:swatch_y + 50, swatch_x:swatch_x + 50] = swatch

    cv2.imshow("Colors Recognizer", img_copy)

    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()
