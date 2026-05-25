Voici le code complet du `README.md` formaté dans un seul bloc de code propre. Tu as juste à cliquer sur l'icône de copie en haut à droite du bloc et à le coller directement dans ton fichier.

```markdown
# 🚀 GestureOS

Un framework Python modulaire et ultra-léger pour contrôler son système d'exploitation par les gestes en temps réel, développé en mode "Hackathon d'un jour".

## 📌 Vision du Projet
L'objectif de ce projet est de s'affranchir de la souris et du clavier pour les tâches quotidiennes répétitives (contrôle du volume, scroll, luminosité) en utilisant la vision par ordinateur. Le projet est conçu pour être exécuté en local avec une latence minimale, sans dépendre de serveurs cloud.

---

## 📈 Évolution et Historique du Développement

### Étape 1 : Le Squelette de Base (Preuve de Concept)
Au départ, l'objectif était de valider la faisabilité du tracking en temps réel. 
* **Approche :** Initialisation du flux vidéo via OpenCV et injection de la matrice d'images dans le modèle de détection de points clés de Google MediaPipe.
* **Résultat :** Extraction réussie des 21 repères (*landmarks*) tridimensionnels de la main avec conversion des coordonnées normalisées en pixels réels $(X, Y)$ par rapport à la résolution de la webcam.

### Étape 2 : Le Problème des Interférences de Gestes
Lors des premiers tests de contrôle du volume (basés sur la distance euclidienne entre le pouce et l'index), un problème majeur est apparu : **les faux positifs**. Une simple paume ouverte déclenchait involontairement des variations de volume parce que la distance pouce-index était également grande.

### Étape 3 : Pivot vers une Architecture Modulaire (POO & SOLID)
Pour résoudre les conflits de patterns et rendre le projet scalable, nous avons complètement réarchitecturé le code en appliquant le **Principe de Responsabilité Unique** :
1. **Extraction de la donnée** (`HandDetector`) : S'occupe uniquement de la vision et des coordonnées.
2. **Filtrage des fonctionnalités** (Système de Plugins/Actions) : Chaque action système possède désormais sa propre classe isolée dans un fichier distinct.
3. **Logique d'activation stricte (Finger Counting) :** Une action ne s'exécute que si la signature exacte des doigts levés/pliés correspond (ex: le volume ne s'active *que si* l'index et le pouce sont détectés et que les autres doigts sont pliés).

---

## 🛠️ Architecture du Code (Modulaire)

Le projet est découpé de manière à pouvoir ajouter une fonctionnalité en créeant simplement un nouveau fichier sans modifier le coeur de l'application :


```

├── main.py                # Point d'entrée, boucle OpenCV et gestionnaire d'actions
├── hand_tracking.py       # Classe HandDetector (Initialisation MediaPipe & Coordonnées)
├── base_action.py         # Classe Abstraite parente définissant le contrat des actions
├── volume_action.py       # Module isolé pour le contrôle du volume système
└── (prochaines actions)   # scroll_action.py, brightness_action.py, etc.

```

---

## 💻 Aperçu du Coeur Logique

### La Classe Parente : `BaseAction`
Toutes les actions héritent de cette structure. Elle intègre un attribut `enabled` permettant à l'utilisateur d'activer ou de désactiver la fonctionnalité à la volée.

```python
class BaseAction:
    def __init__(self, name):
        self.name = name
        self.enabled = True

    def process(self, landmarks, img):
        if not self.enabled or len(landmarks) == 0:
            return img
        if self.match_pattern(landmarks):
            self.execute(landmarks)
        return img

```

### Algorithme de calcul géométrique (Exemple du Volume)

Pour éviter la lourdeur d'un modèle d'IA personnalisé, nous utilisons la géométrie analytique. La distance entre le pouce ($P_1$) et l'index ($P_2$) est calculée via la formule de la distance euclidienne :

$$\text{Distance} = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}$$

En Python : `math.hypot(x2 - x1, y2 - y1)` associée à une vérification de l'état des autres doigts pour valider le contexte du geste.

---

## 🚀 Installation et Utilisation

### Prérequis

* Python 3.10+
* Une webcam fonctionnelle

### Installation

1. Cloner le dépôt :
```bash
git clone [https://github.com/ton-username/nom-du-projet.git](https://github.com/ton-username/nom-du-projet.git)
cd nom-du-projet

```


2. Installer les dépendances :
```bash
pip install opencv-python mediapipe pyautogui

```


3. Lancer l'application :
```bash
python main.py

```



---

## 🔮 Prochaines Étapes et Perspectives (R&D)

* [ ] **Module Scroll :** Gestion du défilement des pages web par suivi vertical de l'index et du majeur collés.
* [ ] **Module Luminosité :** Ajustement des composants système via la bibliothèque `screen-brightness-control`.
* [ ] **Interface de Réalité Augmentée (GUI) :** Intégration de fenêtres transparentes au premier plan via `Tkinter` ou `PyQt` pour faire interagir des éléments graphiques (comme des personnages ou des effets de balayage de pixels) directement sur le bureau de l'utilisateur.

```

```