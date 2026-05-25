import cv2
from HandDetector import HandDetector
# Import de tes modules d'actions
from VolumeAction import VolumeAction
# de même pour brightness_action, scroll_action, etc.

def main():
    cap = cv2.VideoCapture(1)
    detector = HandDetector()
    
    # --- Ton gestionnaire de modules ---
    actions = [
        VolumeAction(),
        # BrightnessAction(),  # Tu as juste à les rajouter ici quand ils sont codés
        # ScrollAction()
    ]
    
    # Exemple pour désactiver une fonction selon le choix de l'user :
    # actions[0].enabled = False 

    while True:
        success, img = cap.read()
        if not success: break
        img = cv2.flip(img, 1)
        
        img = detector.find_hands(img)
        landmarks = detector.find_positions(img)
        
        # On fait défiler toutes les actions actives
        for action in actions:
            img = action.process(landmarks, img)
            
        cv2.imshow("Controle Modulaire", img)
        if cv2.waitKey(1) & 0xFF == ord('q'): break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()