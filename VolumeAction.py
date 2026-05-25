import math
import pyautogui
from BaseAction import BaseAction

class VolumeAction(BaseAction):
    def __init__(self):
        super().__init__("Volume Control")
        
    def _get_finger_states(self, landmarks):
        """Retourne True ou False pour l'état de chaque doigt (levé/plié)"""
        # Repères des bouts des doigts : Index(8), Majeur(12), Annulaire(16), Auriculaire(20)
        # Repères des articulations juste en dessous : Index(6), Majeur(10), Annulaire(14), Auriculaire(18)
        
        index_up = landmarks[8][2] < landmarks[6][2]
        majeur_up = landmarks[12][2] < landmarks[10][2]
        annulaire_up = landmarks[16][2] < landmarks[14][2]
        auriculaire_up = landmarks[20][2] < landmarks[18][2]
        
        return index_up, majeur_up, annulaire_up, auriculaire_up

    def match_pattern(self, landmarks):
        index_up, majeur_up, annulaire_up, auriculaire_up = self._get_finger_states(landmarks)
        
        # CONDITION STRICTE : Seuls l'index (et potentiellement le pouce) doivent agir.
        # Si le majeur, l'annulaire ou l'auriculaire sont levés (comme une paume ouverte), on refuse le geste !
        if not majeur_up and not annulaire_up and not auriculaire_up and index_up:
            return True
        return False

    def execute(self, landmarks):
        # Calcul de la distance Pouce (4) et Index (8)
        x1, y1 = landmarks[4][1], landmarks[4][2]
        x2, y2 = landmarks[8][1], landmarks[8][2]
        dist = math.hypot(x2 - x1, y2 - y1)
        
        if dist < 40:
            pyautogui.press('volumedown')
        elif dist > 140:
            pyautogui.press('volumeup')