import cv2
from HandDetector import HandDetector
# Import de tout les modules d'actions
from VolumeAction import VolumeAction
from ScrollAction import ScrollAction
from BrightnessAction import BrightnessAction
# de même pour brightness_action, scroll_action, etc.

def main():
    cap = cv2.VideoCapture(1)
    detector = HandDetector(detection_confidence=0.7, track_confidence=0.7)
    
    # Intégration dans le pipeline modulaire
    actions = [
        VolumeAction(),
        ScrollAction(),
        BrightnessAction()
    ]

    while True:
        success, img = cap.read()
        if not success: break
        img = cv2.flip(img, 1)
        
        # 1. ANALYSER ET DESSINER D'ABORD (Crée self.results)
        img = detector.find_hands(img)
        
        # 2. EXTRAIRE LES COORDONNÉES ENSUITE (Lit self.results)
        landmarks = detector.find_positions(img)
        
        # Exécution automatique de chaque module indépendant
        for action in actions:
            img = action.process(landmarks, img)
            
        cv2.imshow("GestureOS - Dashboard", img)
        if cv2.waitKey(1) & 0xFF == ord('q'): break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()