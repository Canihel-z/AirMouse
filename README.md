# AirMouse
Il s'agit de pouvoir interagir avec son systèmes d'exploitation uniquement avec les mains

            Trois étapes fondamentaux
HandDetector : La classe qui capture le flux de la caméra, initialise MediaPipe, et extrait les coordonnées des 21 points de la main ($landmarks$).
GestureController : La classe logique. Elle prend les coordonnées, calcule les distances ou les positions (ex: "est-ce que l'index et le pouce se touchent ?"), et identifie le geste.
SystemActions : La classe qui traduit le geste en action réelle sur le PC (via des bibliothèques comme pyautogui ou screen-brightness-control).