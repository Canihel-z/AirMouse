import math

class GestureController:
    def __init__(self):
        # Seuils à ajuster selon la distance entre toi et ta webcam
        self.clutch_threshold = 40  # Si la distance est plus petite, le poing est fermé
        
    def calculate_distance(self, p1, p2, landmarks):
        """Calcule la distance en pixels entre deux landmarks p1 et p2"""
        if len(landmarks) == 0:
            return 0
        
        # Récupération des coordonnées (id, x, y)
        x1, y1 = landmarks[p1][1], landmarks[p1][2]
        x2, y2 = landmarks[p2][1], landmarks[p2][2]
        
        # Calcul du point central (optionnel, utile pour le visuel)
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        
        # Distance euclidienne
        length = math.hypot(x2 - x1, y2 - y1)
        
        return length, [x1, y1, x2, y2, cx, cy]

    def is_hand_open(self, landmarks):
        """Détermine si la main est ouverte en mesurant la distance 
        entre la base de la paume (ID 0) et le bout des doigts"""
        if len(landmarks) == 0:
            return False
            
        # On prend la distance entre le poignet (0) et le bout du majeur (12)
        dist, _ = self.calculate_distance(0, 12, landmarks)
        
        # Si la distance est trop courte, c'est que les doigts sont repliés (poing fermé)
        return dist > 120