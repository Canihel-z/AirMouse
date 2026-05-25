import pyautogui
from BaseAction import BaseAction

class ScrollAction(BaseAction):
    def __init__(self):
        super().__init__("Scroll Control")
        # On stocke la position précédente pour calculer le déplacement
        self.prev_y = None

    def match_pattern(self, landmarks):
        # État des doigts
        index_up = landmarks[8][2] < landmarks[6][2]
        majeur_up = landmarks[12][2] < landmarks[10][2]
        annulaire_up = landmarks[16][2] < landmarks[14][2]
        auriculaire_up = landmarks[20][2] < landmarks[18][2]

        # Condition : Index et Majeur levés, les autres pliés
        if index_up and majeur_up and not annulaire_up and not auriculaire_up:
            return True
        
        # Si on relâche le geste, on réinitialise la mémoire de position
        self.prev_y = None
        return False

    def execute(self, landmarks):
        # On suit le point de l'index (ID 8)
        current_y = landmarks[8][2]

        if self.prev_y is not None:
            # Calcul de la distance de déplacement vertical
            movement = self.prev_y - current_y
            
            # Seuil de tolérance pour éviter les micro-tremblements
            if abs(movement) > 10:
                # pyautogui.scroll prend des valeurs positives pour monter, négatives pour descendre
                # On multiplie par un facteur pour ajuster la vitesse du scroll
                pyautogui.scroll(int(movement * 2))
        
        self.prev_y = current_y