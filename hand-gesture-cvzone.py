"""
Contrôle Vidéo par Gestes de la Main - Version CVZone
Plus simple et plus stable que MediaPipe !
"""

import cv2
from cvzone.HandTrackingModule import HandDetector
import pyautogui
import time

class HandGestureController:
    def __init__(self):
        # Initialisation du détecteur CVZone
        self.detector = HandDetector(
            detectionCon=0.7,      # Confiance de détection
            maxHands=1             # Une seule main
        )
        
        # Variables de contrôle
        self.last_gesture_time = 0
        self.gesture_cooldown = 1.5  # Cooldown entre les gestes
        self.previous_gesture = None
        
    def detect_gesture(self, fingers):
        """
        Détecte le geste selon les doigts levés
        fingers = [pouce, index, majeur, annulaire, auriculaire]
        1 = levé, 0 = baissé
        """
        
        # Poing fermé (0 doigts) = Pause/Play
        if sum(fingers) == 0:
            return "Pause/Play"
        
        # 2 doigts (index + majeur) = Avancer 10s
        if sum(fingers) == 2 and fingers[1] == 1 and fingers[2] == 1:
            return "Avancer 10s"
        
        # 3 doigts = Reculer 10s
        if sum(fingers) == 3:
            return "Reculer 10s"
        
        # Pouce seul levé = Volume +
        if sum(fingers) == 1 and fingers[0] == 1:
            return "Volume +"
        
        # 4 doigts (sans pouce) = Volume -
        if sum(fingers) == 4 and fingers[0] == 0:
            return "Volume -"
        
        # 5 doigts (main ouverte) = Plein écran
        if sum(fingers) == 5:
            return "Plein écran"
        
        return None
    
    def execute_gesture(self, gesture_name):
        """Exécute l'action correspondant au geste"""
        current_time = time.time()
        
        # Vérifier le cooldown
        if current_time - self.last_gesture_time < self.gesture_cooldown:
            return False
        
        # Éviter les détections répétées
        if gesture_name == self.previous_gesture:
            return False
        
        print(f"🎯 Geste détecté: {gesture_name}")
        
        # Actions disponibles
        actions = {
            "Pause/Play": ('space', "Pause/Play"),
            "Avancer 10s": ('right', "Avance de 10 secondes"),
            "Reculer 10s": ('left', "Recule de 10 secondes"),
            "Volume +": ('up', "Volume +"),
            "Volume -": ('down', "Volume -"),
            "Plein écran": ('f', "Plein écran")
        }
        
        if gesture_name in actions:
            key, description = actions[gesture_name]
            pyautogui.press(key)
            print(f"   Action: {description}")
        
        self.last_gesture_time = current_time
        self.previous_gesture = gesture_name
        return True
    
    def run(self):
        """Lance la détection de gestes en temps réel"""
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("❌ Impossible d'ouvrir la caméra")
            print("   Vérifiez que votre webcam est connectée et accessible")
            return
        
        print("=" * 60)
        print("🎮 CONTRÔLE VIDÉO PAR GESTES - Version CVZone")
        print("=" * 60)
        print("\n📋 GESTES DISPONIBLES:")
        print("  ✊ Poing fermé (0)   → Pause/Play")
        print("  ✌️  2 doigts         → Avancer 10 secondes")
        print("  🤟 3 doigts          → Reculer 10 secondes")
        print("  👍 Pouce seul        → Volume +")
        print("  🖖 4 doigts          → Volume -")
        print("  🖐️  5 doigts         → Plein écran")
        print("\n⌨️  Appuyez sur 'q' pour quitter")
        print("=" * 60 + "\n")
        
        try:
            while True:
                success, img = cap.read()
                if not success:
                    print("⚠️  Impossible de lire la caméra")
                    break
                
                # Effet miroir pour une utilisation naturelle
                img = cv2.flip(img, 1)
                
                # Détecter les mains
                hands, img = self.detector.findHands(img)
                
                if hands:
                    # Prendre la première main détectée
                    hand = hands[0]
                    
                    # Obtenir quels doigts sont levés
                    fingers = self.detector.fingersUp(hand)
                    
                    # Détecter le geste
                    gesture = self.detect_gesture(fingers)
                    
                    if gesture:
                        # Afficher le geste détecté
                        cv2.putText(img, f"Geste: {gesture}", (10, 50),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        
                        # Afficher le nombre de doigts levés
                        cv2.putText(img, f"Doigts: {sum(fingers)}", (10, 100),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
                        
                        # Exécuter l'action
                        self.execute_gesture(gesture)
                    else:
                        # Afficher juste le nombre de doigts
                        cv2.putText(img, f"Doigts: {sum(fingers)}", (10, 50),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 200), 2)
                        self.previous_gesture = None
                
                # Afficher les instructions
                cv2.putText(img, "Appuyez sur 'q' pour quitter", 
                            (10, img.shape[0] - 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                
                # Afficher l'image
                cv2.imshow('Controle Video par Gestes - CVZone', img)
                
                # Quitter avec 'q'
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        
        except KeyboardInterrupt:
            print("\n⚠️  Interruption par l'utilisateur")
        
        finally:
            cap.release()
            cv2.destroyAllWindows()
            print("\n✅ Programme terminé")


if __name__ == "__main__":
    print("🚀 Démarrage du contrôleur de gestes...")
    print("⏳ Initialisation de la caméra...\n")
    
    try:
        controller = HandGestureController()
        controller.run()
    except ImportError as e:
        print("\n❌ Erreur d'import - Packages manquants")
        print("\n📦 Installation requise:")
        print("   pip install cvzone opencv-python pyautogui numpy==1.26.4")
        print(f"\n🔍 Détails: {e}")
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        print("\n💡 Suggestions:")
        print("   1. Vérifiez que votre webcam est connectée")
        print("   2. Fermez les autres applications utilisant la caméra")
        print("   3. Vérifiez les permissions d'accès à la caméra")
