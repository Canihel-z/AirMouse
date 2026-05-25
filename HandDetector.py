import cv2
import mediapipe as mp

class HandDetector:
    def __init__(self, mode=False, max_hands=2, detection_confidence=0.5, track_confidence=0.5):
        # Configuration des paramètres de MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=mode,
            max_num_hands=max_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=track_confidence
        )
        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self, img, draw=True):
        # MediaPipe utilise le format RGB, OpenCV utilise le BGR
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        # Dessiner les repères sur la main si demandé
        if self.results.multi_hand_landmarks and draw:
            for hand_lms in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(img, hand_lms, self.mp_hands.HAND_CONNECTIONS)
        return img

    def find_positions(self, img, hand_no=0):
        landmark_list = []
        if self.results.multi_hand_landmarks:
            # On sélectionne la main désirée (0 pour la première main détectée)
            target_hand = self.results.multi_hand_landmarks[hand_no]
            
            for id, lm in enumerate(target_hand.landmark):
                # Les coordonnées de MediaPipe sont normalisées (de 0 à 1). 
                # On les convertit en pixels selon la taille de l'image.
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                landmark_list.append([id, cx, cy])
                
        return landmark_list

# --- Zone de Test en Temps Réel ---
if __name__ == "__main__":
    # 0 est généralement l'ID de la webcam intégrée
    cap = cv2.VideoCapture(1)
    detector = HandDetector()

    while True:
        success, img = cap.read()
        if not success:
            print("Impossible d'accéder à la webcam.")
            break

        # Inversion miroir pour que le contrôle soit intuitif (gauche/droite)
        img = cv2.flip(img, 1)
        
        # Détection et dessin
        img = detector.find_hands(img)
        landmarks = detector.find_positions(img)

        # Si on détecte des points, on affiche la position du bout de l'index (ID 8)
        if len(landmarks) != 0:
            # landmarks[8] renvoie [8, x, y]
            print(f"Index position: X={landmarks[8][1]}, Y={landmarks[8][2]}")

        # Affichage de la fenêtre
        cv2.imshow("Hand Tracking Test", img)
        
        # Quitter si on appuie sur la touche 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()