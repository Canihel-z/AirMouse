import cv2
import pyautogui
from HandDetector import HandDetector
from GestureController import GestureController

# Désactiver le failsafe de pyautogui pour éviter les crashs si la souris va dans un coin
pyautogui.FAILSAFE = False

def main():
    cap = cv2.VideoCapture(1)
    detector = HandDetector(detection_confidence=0.7, track_confidence=0.7)
    controller = GestureController()
    
    # Variables pour éviter de spammer le système trop vite
    counter = 0 

    while True:
        success, img = cap.read()
        if not success:
            break
            
        img = cv2.flip(img, 1)
        img = detector.find_hands(img)
        landmarks = detector.find_positions(img)

        if len(landmarks) != 0:
            # 1. Vérification de l'embrayage (La main doit être ouverte pour agir)
            if controller.is_hand_open(landmarks):
                cv2.putText(img, "Statut: ACTIF", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                # 2. Geste du Volume : Pouce (4) et Index (8)
                dist_vol, info_vol = controller.calculate_distance(4, 8, landmarks)
                cx, cy = info_vol[4], info_vol[5]
                
                # Dessiner un cercle sur le point central pour avoir un retour visuel
                cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)
                
                # Logique de contrôle : Si les doigts sont très proches -> Baisser le volume
                if dist_vol < 30:
                    pyautogui.press('volumedown')
                    cv2.putText(img, "VOLUME DOWN", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                # Si les doigts sont écartés au-dessus d'un certain seuil -> Augmenter le volume
                elif dist_vol > 130:
                    pyautogui.press('volumeup')
                    cv2.putText(img, "VOLUME UP", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                cv2.putText(img, "Statut: VEILLE (Poing ferme)", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow("Controle Gestuel", img)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()