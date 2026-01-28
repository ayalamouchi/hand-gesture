@echo off
echo ============================================================
echo   INSTALLATION CVZONE - Hand Gesture Controller
echo ============================================================
echo.
echo Cette installation est BEAUCOUP plus simple que MediaPipe !
echo.
pause

echo.
echo [1/5] Nettoyage des anciens packages...
pip uninstall mediapipe tensorflow tensorflow-intel -y

echo.
echo [2/5] Installation de NumPy 1.26.4...
pip install numpy==1.26.4

echo.
echo [3/5] Installation de CVZone...
pip install cvzone==1.6.1

echo.
echo [4/5] Installation d'OpenCV...
pip install opencv-python==4.10.0.84

echo.
echo [5/5] Installation de PyAutoGUI...
pip install pyautogui==0.9.54

echo.
echo ============================================================
echo   VERIFICATION DES INSTALLATIONS
echo ============================================================
echo.

python -c "import numpy; print('✓ NumPy:', numpy.__version__)" 2>nul || echo ✗ NumPy - ERREUR
python -c "import cvzone; print('✓ CVZone installe')" 2>nul || echo ✗ CVZone - ERREUR
python -c "import cv2; print('✓ OpenCV:', cv2.__version__)" 2>nul || echo ✗ OpenCV - ERREUR
python -c "import pyautogui; print('✓ PyAutoGUI installe')" 2>nul || echo ✗ PyAutoGUI - ERREUR

echo.
echo ============================================================
echo   Installation terminee !
echo ============================================================
echo.
echo Vous pouvez maintenant lancer : python hand-gesture-cvzone.py
echo.
pause
