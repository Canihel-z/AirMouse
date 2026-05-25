import math
import screen_brightness_control as sbc
from BaseAction import BaseAction

class BrightnessAction(BaseAction):
    def __init__(self):
        super().__init__("Brightness Control")

    def match_pattern(self, landmarks):
        index_up = landmarks[8][2] < landmarks[6][2]
        majeur_up = landmarks[12][2] < landmarks[10][2]
        annulaire_up = landmarks[16][2] < landmarks[14][2]
        auriculaire_up = landmarks[20][2] < landmarks[18][2]

        # Condition "Pistolet" : Index levé, les 3 autres doigts longs pliés
        if index_up and not majeur_up and not annulaire_up and not auriculaire_up:
            return True
        return False

    def execute(self, landmarks):
        # Calcul de la distance entre le pouce (4) et l'index (8)
        x1, y1 = landmarks[4][1], landmarks[4][2]
        x2, y2 = landmarks[8][1], landmarks[8][2]
        dist = math.hypot(x2 - x1, y2 - y1)

        # On mappe la distance (ex: entre 30 et 150 pixels) sur un pourcentage (0 à 100)
        # Formule de normalisation simple :
        min_dist, max_dist = 30, 150
        
        # On contraint la distance entre nos bornes
        dist = max(min_dist, min(dist, max_dist))
        
        # Calcul du pourcentage de luminosité
        brightness_level = int(((dist - min_dist) / (max_dist - min_dist)) * 100)
        
        # Application immédiate au système
        try:
            sbc.set_brightness(brightness_level)
        except Exception:
            # Sécurité si le PC ou l'écran externe ne supporte pas le changement direct via la lib
            pass