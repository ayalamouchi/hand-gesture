import cv2
import mediapipe as mp
import pyautogui
import math
import time

class HandGestureController:
    def __init__(self):
        # Initialisation de MediaPipe avec la nouvelle API (0.10.32+)
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        
        # Variables de contrôle
        self.last_gesture_time = 0
        self.gesture_cooldown = 1.5  # Cooldown de 1.5 secondes entre les gestes
        self.previous_gesture = None
        
    def calculate_distance(self, point1, point2):
        """Calcule la distance euclidienne entre deux points"""
        return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)
    
    def count_fingers(self, landmarks):
        """Compte le nombre de doigts levés"""
        fingers = []
        
        # Pouce (compare x car mouvement latéral)
        if landmarks[4].x < landmarks[3].x:  # Pouce gauche
            fingers.append(1)
        else:
            fingers.append(0)
        
        # Autres doigts (index, majeur, annulaire, auriculaire)
        finger_tips = [8, 12, 16, 20]
        finger_pips = [6, 10, 14, 18]
        
        for tip, pip in zip(finger_tips, finger_pips):
            if landmarks[tip].y < landmarks[pip].y:  # Doigt levé
                fingers.append(1)
            else:
                fingers.append(0)
        
        return fingers.count(1)
    
    def detect_fist(self, landmarks):
        """Détecte si la main est fermée (poing)"""
        finger_tips = [4, 8, 12, 16, 20]
        palm_base = landmarks[0]
        
        # Vérifier si tous les doigts sont proches de la paume
        distances = [self.calculate_distance(landmarks[tip], palm_base) for tip in finger_tips]
        avg_distance = sum(distances) / len(distances)
        
        return avg_distance < 0.15
    
    def detect_peace_sign(self, landmarks):
        """Détecte le signe de la paix (index et majeur levés)"""
        # Index levé
        index_up = landmarks[8].y < landmarks[6].y
        # Majeur levé
        middle_up = landmarks[12].y < landmarks[10].y
        # Annulaire baissé
        ring_down = landmarks[16].y > landmarks[14].y
        # Auriculaire baissé
        pinky_down = landmarks[20].y > landmarks[18].y
        
        return index_up and middle_up and ring_down and pinky_down
    
    def detect_thumbs_up(self, landmarks):
        """Détecte le pouce levé"""
        # Pouce levé (le plus haut point)
        thumb_up = landmarks[4].y < landmarks[3].y < landmarks[2].y
        # Autres doigts repliés
        fingers_down = all(landmarks[tip].y > landmarks[tip-2].y for tip in [8, 12, 16, 20])
        
        return thumb_up and fingers_down
    
    def detect_thumbs_down(self, landmarks):
        """Détecte le pouce vers le bas"""
        # Pouce vers le bas
        thumb_down = landmarks[4].y > landmarks[3].y > landmarks[2].y
        # Autres doigts repliés
        fingers_down = all(landmarks[tip].y > landmarks[tip-2].y for tip in [8, 12, 16, 20])
        
        return thumb_down and fingers_down
    
    def detect_pinch(self, landmarks):
        """Détecte un pincement (pouce et index proches)"""
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        distance = self.calculate_distance(thumb_tip, index_tip)
        
        return distance < 0.05
    
    def execute_gesture(self, gesture_name):
        """Exécute l'action correspondant au geste"""
        current_time = time.time()
        
        # Vérifier le cooldown
        if current_time - self.last_gesture_time < self.gesture_cooldown:
            return False
        
        # Éviter les détections répétées du même geste
        if gesture_name == self.previous_gesture:
            return False
        
        print(f"🎯 Geste détecté: {gesture_name}")
        
        if gesture_name == "Pause/Play":
            pyautogui.press('space')
            print("   Action: Pause/Play")
        
        elif gesture_name == "Avancer 10s":
            pyautogui.press('right')
            print("   Action: Avance de 10 secondes")
        
        elif gesture_name == "Reculer 10s":
            pyautogui.press('left')
            print("   Action: Recule de 10 secondes")
        
        elif gesture_name == "Volume +":
            pyautogui.press('up')
            print("   Action: Volume +")
        
        elif gesture_name == "Volume -":
            pyautogui.press('down')
            print("   Action: Volume -")
        
        elif gesture_name == "Plein écran":
            pyautogui.press('f')
            print("   Action: Plein écran")
        
        self.last_gesture_time = current_time
        self.previous_gesture = gesture_name
        return True
    
    def detect_gesture(self, landmarks):
        """Détecte le type de geste effectué"""
        
        # Poing fermé = Pause/Play
        if self.detect_fist(landmarks):
            return "Pause/Play"
        
        # Signe de paix (2 doigts) = Avancer de 10s
        if self.detect_peace_sign(landmarks):
            return "Avancer 10s"
        
        # Pouce levé = Volume +
        if self.detect_thumbs_up(landmarks):
            return "Volume +"
        
        # Pouce vers le bas = Volume -
        if self.detect_thumbs_down(landmarks):
            return "Volume -"
        
        # Pincement = Plein écran
        if self.detect_pinch(landmarks):
            return "Plein écran"
        
        # Compter les doigts
        num_fingers = self.count_fingers(landmarks)
        
        # 3 doigts = Reculer de 10s
        if num_fingers == 3:
            return "Reculer 10s"
        
        return None
    
    def run(self):
        """Lance la détection de gestes en temps réel"""
        cap = cv2.VideoCapture(0)
        
        print("=" * 60)
        print("🎮 CONTRÔLE VIDÉO PAR GESTES DE LA MAIN")
        print("=" * 60)
        print("\n📋 GESTES DISPONIBLES:")
        print("  ✊ Poing fermé       → Pause/Play")
        print("  ✌️  2 doigts (paix)  → Avancer 10 secondes")
        print("  🤟 3 doigts          → Reculer 10 secondes")
        print("  👍 Pouce levé        → Volume +")
        print("  👎 Pouce baissé      → Volume -")
        print("  🤏 Pincement         → Plein écran")
        print("\n⌨️  Appuyez sur 'q' pour quitter")
        print("=" * 60 + "\n")
        
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Impossible de lire la caméra")
                break
            
            # Retourner l'image horizontalement pour un effet miroir
            image = cv2.flip(image, 1)
            
            # Convertir BGR en RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Améliorer les performances
            image_rgb.flags.writeable = False
            
            # Traiter l'image
            results = self.hands.process(image_rgb)
            
            # Restaurer la modification
            image_rgb.flags.writeable = True
            
            # Dessiner les annotations
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Dessiner les points de repère de la main avec les nouveaux styles
                    self.mp_drawing.draw_landmarks(
                        image, 
                        hand_landmarks, 
                        self.mp_hands.HAND_CONNECTIONS,
                        self.mp_drawing_styles.get_default_hand_landmarks_style(),
                        self.mp_drawing_styles.get_default_hand_connections_style()
                    )
                    
                    # Détecter le geste
                    gesture = self.detect_gesture(hand_landmarks.landmark)
                    
                    if gesture:
                        # Afficher le geste détecté
                        cv2.putText(image, f"Geste: {gesture}", (10, 50), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        
                        # Exécuter l'action
                        self.execute_gesture(gesture)
                    else:
                        self.previous_gesture = None
            
            # Afficher les instructions
            cv2.putText(image, "Appuyez sur 'q' pour quitter", (10, image.shape[0] - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            
            # Afficher l'image
            cv2.imshow('Controle Video par Gestes', image)
            
            # Quitter avec 'q'
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        print("\n✅ Programme terminé")

if __name__ == "__main__":
    controller = HandGestureController()
    controller.run()