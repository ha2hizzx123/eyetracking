
import cv2
import mediapipe as mp
import pyautogui

#웹캠 설정
cam = cv2.VideoCapture(0)

#mediapipe 모델 초기화
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size() #현재 화면의 크기를 가져옴

while True:
    _, frame = cam.read()
    #캠 좌우반전
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    
    #얼굴 랜드마크 데이터 가져옴
    landmark_points = output.multi_face_landmarks
    frame_h, frame_w, _ = frame.shape
    if landmark_points:
        landmarks = landmark_points[0].landmark

        #랜드마크 474~478(오른쪽 눈의 좌,우,위,아래)
        for id, landmark in enumerate(landmarks[474:478]):
            #랜드마크좌표를 프레임에 맞춤
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)

            #해당 위치에 원 그림
            cv2.circle(frame, (x,y), 3, (0, 255, 0))

            #화면 크기에 맞춰 id 1번(오른쪽 눈의 윗부분)의 좌표위치로 마우스포인터 이동
            if id == 1:
                screen_x = screen_w / frame_w * x
                screen_y = screen_h / frame_h * y

                #마우스 포인터 이동
                pyautogui.moveTo(screen_x, screen_y)

        #왼쪽눈의 위,아래부분에 원을 찍음
        left = [landmarks[145], landmarks[159]]
        for landmark in left:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x,y), 3, (0, 255, 255))

        #왼쪽눈의 위,아래거리가 0.01보다 작게 좁혀졌을 때 => 눈을 감았을 때
        if (left[0].y - left[1].y) < 0.01:
            #마우스 클릭 기능 수행후 1초동안 대기
            pyautogui.click()
            pyautogui.sleep(1)

    #화면에 출력
    cv2.imshow('mouse control with eyes', frame)

    # q 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break