import cv2

cap = cv2.VideoCapture(0)
print("Camera ouverte :", cap.isOpened())

while True:
    ret, frame = cap.read()
    if not ret:
        print("Impossible de lire la camera")
        break

    cv2.imshow("Test Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
