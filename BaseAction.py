class BaseAction:
    def __init__(self, name):
        self.name = name
        self.enabled = True  # L'utilisateur peut passer ça à False

    def process(self, landmarks, img):
        """Méthode principale appelée par le main à chaque frame"""
        if not self.enabled or len(landmarks) == 0:
            return img
            
        # 1. On vérifie si le pattern spécifique est détecté
        if self.match_pattern(landmarks):
            # 2. Si oui, on exécute l'action système
            self.execute(landmarks)
            
        return img

    def match_pattern(self, landmarks):
        """Doit être réécrite dans chaque sous-classe"""
        raise NotImplementedError

    def execute(self, landmarks):
        """Doit être réécrite dans chaque sous-classe"""
        raise NotImplementedError