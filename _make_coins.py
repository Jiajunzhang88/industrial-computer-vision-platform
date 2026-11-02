import cv2, numpy as np, base64, json

def make_coin(rich=True):
    img = np.full((300, 300, 3), 200, np.uint8)
    cv2.circle(img, (150, 150), 120, (120, 120, 120), -1)
    cv2.circle(img, (150, 150), 120, (60, 60, 60), 4)
    if rich:
        for r in range(30, 95, 12):
            cv2.circle(img, (150, 150), r, (80, 80, 80), 2)
        for a in range(0, 360, 15):
            x = 150 + int(60 * np.cos(np.radians(a)))
            y = 150 + int(60 * np.sin(np.radians(a)))
            cv2.circle(img, (x, y), 10, (90, 90, 90), -1)
    else:
        cv2.putText(img, "10", (125, 165), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (70, 70, 70), 3)
    return img

def b64(img):
    ok, buf = cv2.imencode('.png', img)
    return base64.b64encode(buf.tobytes()).decode()

obverse = make_coin(True)
reverse = make_coin(False)
cv2.imwrite("uploads/test_coin_obverse.png", obverse)
cv2.imwrite("uploads/test_coin_reverse.png", reverse)
json.dump({"obverse": b64(obverse), "reverse": b64(reverse)}, open("test_coins.json", "w"))
print("OK coins written", obverse.shape, reverse.shape)
