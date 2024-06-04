import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QColor, QFont

class Overlay(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.start_timer()

    def initUI(self):
        # Configuration de la fenêtre
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.width = 70
        self.height = 40
        self.setGeometry(990 - int(self.width/2), 10, self.width, self.height)

        self.time_left = 40

        closeButton = QPushButton('Close', self)
        closeButton.setGeometry(700, 10, 80, 40)
        closeButton.clicked.connect(self.close)
        self.show()

    def start_timer(self):
        # Configurer le timer pour le compte à rebours
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)  # Mettre à jour toutes les secondes

    def update_timer(self):
        # Mettre à jour le temps restant
        self.time_left -= 1
        if self.time_left <= 0:
            self.close()
        self.update()  # Redessiner l'interface
    
    def paintEvent(self, event):
        # Dessiner l'interface de l'overlay
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(0, 0, 0, 160))  # Couleur avec transparence
        painter.drawRect(self.rect())
        
        # Ajouter du texte ou d'autres éléments graphiques
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(QFont('Arial', 30))
        painter.drawText(self.rect(), Qt.AlignCenter, f'{self.time_left}')

    def mousePressEvent(self, event):
        # Gestion des événements de la souris
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        # Permettre de déplacer la fenêtre
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def keyPressEvent(self, event):
        # Fermer la fenêtre en appuyant sur Échap
        if event.key() == Qt.Key_Escape:
            self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    overlay = Overlay()
    sys.exit(app.exec_())
