import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QRect
import engine_py

ASSETS_DIR = os.path.join(os.path.dirname(__file__), 'U_CARDS')


class CardWidget(QtWidgets.QFrame):
    def __init__(self, color, value, index, main_window, parent=None):
        super().__init__(parent)
        self.index = index
        self.color = color
        self.value = value
        self.main_window = main_window
        self.setFixedSize(120, 160)
        self.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Raised)
        self.setLineWidth(2)
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 2)
        
        # Load card image from U_CARDS
        pixmap = self._load_card_image(color, value)
        if pixmap:
            self.img_label = QtWidgets.QLabel()
            self.img_label.setPixmap(pixmap.scaledToWidth(110, QtCore.Qt.FastTransformation))
            self.img_label.setAlignment(QtCore.Qt.AlignCenter)
            layout.addWidget(self.img_label)
        else:
            # Fallback text label
            label = QtWidgets.QLabel(f"{color} {value}")
            label.setAlignment(QtCore.Qt.AlignCenter)
            font = label.font()
            font.setBold(True)
            label.setFont(font)
            layout.addWidget(label)
        
        # Animation state
        self.is_highlighted = False

    def _load_card_image(self, color, value):
        # Map color names to filename prefixes
        color_map = {
            'Red': 'red',
            'Green': 'green',
            'Blue': 'blue',
            'Yellow': 'yellow'
        }
        color_prefix = color_map.get(color, color.lower())
        filename = f"{color_prefix}-{value}-card-clipart-lg.png"
        filepath = os.path.join(ASSETS_DIR, filename)
        
        if os.path.exists(filepath):
            return QtGui.QPixmap(filepath)
        return None

    def on_play(self):
        # delegate to main window
        self.main_window.play_card(self.index)

    def mousePressEvent(self, event):
        # clicking the card image acts as Play (only if playable)
        try:
            playable = self.main_window._is_card_playable(self.color, self.value)
        except Exception:
            playable = True
        if playable:
            self.on_play()
        else:
            # flash or show invalid cue
            QtWidgets.QToolTip.showText(event.globalPos(), 'Cannot play this card')
        super().mousePressEvent(event)

    def set_playable(self, is_playable):
        if is_playable:
            self.setStyleSheet("CardWidget { border: 3px solid #2ecc71; }")
            self.is_highlighted = True
        else:
            self.setStyleSheet("")
            self.is_highlighted = False

    def animate_fade(self):
        """Fade animation when card is played"""
        anim = QPropertyAnimation(self, b"windowOpacity")
        anim.setDuration(500)
        anim.setStartValue(1.0)
        anim.setEndValue(0.3)
        anim.start()


class WinOverlay(QtWidgets.QWidget):
    """A full-window overlay that shows the winner with a blurred background and zoom animation."""
    def __init__(self, parent, message, winner_index=None):
        super().__init__(parent)
        self.parent_win = parent
        self.message = message
        self.winner_index = winner_index

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Dialog)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setGeometry(self.parent_win.rect())

        # Capture background snapshot and blur it
        snapshot = self.parent_win.grab()
        self.bg_label = QtWidgets.QLabel(self)
        self.bg_label.setPixmap(snapshot)
        self.bg_label.setGeometry(self.rect())
        blur = QtWidgets.QGraphicsBlurEffect(self.bg_label)
        blur.setBlurRadius(12)
        self.bg_label.setGraphicsEffect(blur)

        # Dim layer
        self.dim = QtWidgets.QWidget(self)
        self.dim.setStyleSheet('background-color: rgba(0,0,0,120);')
        self.dim.setGeometry(self.rect())

        # Central message
        self.msg_label = QtWidgets.QLabel(self.message, self)
        font = QtGui.QFont()
        font.setPointSize(32)
        font.setBold(True)
        self.msg_label.setFont(font)
        self.msg_label.setWordWrap(True)
        self.msg_label.setStyleSheet('color: white; background-color: rgba(30,30,30,220); border-radius: 12px; padding: 28px;')
        self.msg_label.setAlignment(QtCore.Qt.AlignCenter)

        # Start tiny in center
        parent_rect = self.rect()
        start_w, start_h = 20, 20
        cx = parent_rect.width() // 2
        cy = parent_rect.height() // 2
        start_rect = QtCore.QRect(cx - start_w//2, cy - start_h//2, start_w, start_h)
        
        # Calculate end size based on text length with word wrap
        # First, estimate width based on text length (max 900px, min 600px)
        text_length = len(self.message)
        base_width = 700
        # Adjust width based on message length (longer messages get wider boxes for fewer lines)
        if text_length > 35:
            end_w = min(900, parent_rect.width() - 100)
        else:
            end_w = min(base_width, parent_rect.width() - 200)
        
        # Height: accommodate up to 3 lines comfortably
        end_h = min(320, parent_rect.height() - 180)
        end_rect = QtCore.QRect(cx - end_w//2, cy - end_h//2, end_w, end_h)
        self.msg_label.setGeometry(start_rect)

        # Opacity effect
        self.opacity_effect = QtWidgets.QGraphicsOpacityEffect(self.msg_label)
        self.msg_label.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0.0)

        # Animate geometry (zoom) and opacity
        self.geom_anim = QPropertyAnimation(self.msg_label, b"geometry")
        self.geom_anim.setDuration(650)
        self.geom_anim.setStartValue(start_rect)
        self.geom_anim.setEndValue(end_rect)
        self.geom_anim.setEasingCurve(QEasingCurve.OutBack)

        self.opacity_anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.opacity_anim.setDuration(650)
        self.opacity_anim.setStartValue(0.0)
        self.opacity_anim.setEndValue(1.0)

        self.geom_anim.finished.connect(self._on_anim_finished)

        # Show overlay and start animations
        self.show()
        self.geom_anim.start()
        self.opacity_anim.start()

        # (No close 'X' button — options are presented below after animation)

        # Option buttons (hidden until animation finishes)
        self.btn_new = QtWidgets.QPushButton('\n🔄 New Game\n', self)
        self.btn_exit = QtWidgets.QPushButton('\n⛔ Exit Game\n', self)
        for b in (self.btn_new, self.btn_exit):
            b.setFixedSize(280, 80)
            b.setStyleSheet('''
                QPushButton { background-color: #16c784; color: #042; border-radius: 10px; font-weight: 700; font-size: 18px; padding: 8px; }
                QPushButton:hover { background-color: #1fe090; }
            ''')
            b.hide()
        self.btn_new.clicked.connect(self._new_game_and_close)
        self.btn_exit.clicked.connect(QtWidgets.QApplication.instance().quit)

    def _on_anim_finished(self):
        # Show option buttons under the message after the zoom finishes
        mr = self.msg_label.geometry()
        spacing = 16
        total_w = self.btn_new.width() + spacing + self.btn_exit.width()
        cx = self.rect().width() // 2
        y = mr.bottom() + 24
        nx = cx - total_w // 2
        self.btn_new.move(nx, y)
        self.btn_exit.move(nx + self.btn_new.width() + spacing, y)
        self.btn_new.show()
        self.btn_exit.show()

    def _new_game_and_close(self):
        try:
            self.close()
            if hasattr(self.parent_win, 'on_new_game'):
                self.parent_win.on_new_game()
        except Exception:
            self.close()



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('UNO - Card Game (Production Edition)')
        self.resize(1200, 800)
        self.setWindowIcon(QtGui.QIcon())
        self.setStyleSheet("""
            QMainWindow { background-color: #1a1a2e; }
            QLabel { color: #eee; }
            QPushButton { 
                background-color: #0f3460; 
                color: white; 
                border: 2px solid #16c784;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #16c784; color: #000; }
            QScrollArea { border: 2px solid #16c784; }
        """)

        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        main_layout = QtWidgets.QVBoxLayout(central)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # Title
        title = QtWidgets.QLabel('🎴 UNO Card Game')
        font = title.font()
        font.setPointSize(20)
        font.setBold(True)
        title.setFont(font)
        title.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addWidget(title)

        # Game info layout
        info_layout = QtWidgets.QHBoxLayout()
        self.status_label = QtWidgets.QLabel('Game started. Your turn!')
        self.status_label.setStyleSheet("color: #2ecc71; font-weight: bold;")
        info_layout.addWidget(self.status_label)
        info_layout.addStretch()
        self.turn_counter = QtWidgets.QLabel('Turn: 1')
        self.turn_counter.setStyleSheet("color: #e74c3c; font-weight: bold;")
        info_layout.addWidget(self.turn_counter)
        main_layout.addLayout(info_layout)

        # Board area with top discard
        board_area = QtWidgets.QWidget()
        board_layout = QtWidgets.QVBoxLayout(board_area)
        board_layout.setContentsMargins(0, 0, 0, 0)
        
        discard_label = QtWidgets.QLabel('📍 Top Discard:')
        discard_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        board_layout.addWidget(discard_label)
        
        self.discard_card = QtWidgets.QLabel()
        self.discard_card.setMinimumSize(150, 200)
        self.discard_card.setAlignment(QtCore.Qt.AlignCenter)
        self.discard_card.setStyleSheet("border: 3px solid #f39c12;")
        board_layout.addWidget(self.discard_card)
        
        # AI area above board: show facedown cards
        self.ai_label = QtWidgets.QLabel("🤖 AI Hand:")
        self.ai_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        board_layout.addWidget(self.ai_label)
        self.ai_widget = QtWidgets.QWidget()
        self.ai_layout = QtWidgets.QHBoxLayout(self.ai_widget)
        self.ai_layout.setSpacing(6)
        board_layout.addWidget(self.ai_widget)

        main_layout.addWidget(board_area, 1)

        # Divider
        divider = QtWidgets.QFrame()
        divider.setFrameShape(QtWidgets.QFrame.HLine)
        divider.setFrameShadow(QtWidgets.QFrame.Raised)
        main_layout.addWidget(divider)

        # Player's hand area
        hand_label = QtWidgets.QLabel('🎯 Your Hand:')
        hand_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        main_layout.addWidget(hand_label)
        
        self.hand_scroll = QtWidgets.QScrollArea()
        self.hand_scroll.setMinimumHeight(200)
        self.hand_widget = QtWidgets.QWidget()
        self.hand_layout = QtWidgets.QHBoxLayout(self.hand_widget)
        self.hand_layout.setSpacing(12)
        self.hand_scroll.setWidget(self.hand_widget)
        self.hand_scroll.setWidgetResizable(True)
        main_layout.addWidget(self.hand_scroll, 1)

        # Move history area
        history_label = QtWidgets.QLabel('📋 Move History:')
        history_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        main_layout.addWidget(history_label)
        
        self.history_text = QtWidgets.QPlainTextEdit()
        self.history_text.setReadOnly(True)
        self.history_text.setMaximumHeight(100)
        self.history_text.setStyleSheet("background-color: #16213e; color: #00ff00; font-family: monospace; font-size: 10px;")
        main_layout.addWidget(self.history_text)

        # Control buttons (kept minimal; Draw and New Game moved into the hand/overlay)
        ctrl_layout = QtWidgets.QHBoxLayout()
        
        self.next_btn = QtWidgets.QPushButton('⏭️ End Turn')
        self.next_btn.setMinimumWidth(120)
        self.next_btn.clicked.connect(self.on_end_turn)
        ctrl_layout.addWidget(self.next_btn)
        
        ctrl_layout.addStretch()
        main_layout.addLayout(ctrl_layout)

        # initialize engine
        self.turn_count = 1
        self.move_history = []
        engine_py.init()
        self.refresh_ui()

    def refresh_ui(self):
        # update top discard card image
        color, value = engine_py.get_top_discard()
        pixmap = self._load_card_image(color, value)
        if pixmap:
            scaled = pixmap.scaledToHeight(180, QtCore.Qt.FastTransformation)
            self.discard_card.setPixmap(scaled)
        else:
            self.discard_card.setText(f'{color} {value}')

        # clear and refresh hand
        while self.hand_layout.count():
            item = self.hand_layout.takeAt(0)
            w = item.widget() if item is not None else None
            if w:
                w.deleteLater()

        # Add Draw card button as a plain card-sized button beside player's cards
        draw_btn = QtWidgets.QPushButton('\n🎲\nDRAW', self.hand_widget)
        draw_btn.setFixedSize(120, 160)
        draw_btn.setFlat(True)
        draw_btn.setStyleSheet('''
            QPushButton { background-color: #f6f6f6; color: #0b0b0b; border-radius: 8px; font-weight: bold; font-size: 16px; }
            QPushButton:hover { background-color: #e6e6e6; }
        ''')
        draw_btn.clicked.connect(self.on_draw)
        self.hand_layout.addWidget(draw_btn)

        hand = engine_py.get_hand(0)
        for i, (c, v) in enumerate(hand, start=1):
            w = CardWidget(c, v, i, self)
            # highlight playable cards
            if self._is_card_playable(c, v):
                w.set_playable(True)
            self.hand_layout.addWidget(w)

        self.hand_layout.addStretch()

        # Render AI facedown cards
        # clear ai layout
        while self.ai_layout.count():
            w = self.ai_layout.takeAt(0).widget()
            if w:
                w.deleteLater()
        ai_hand = engine_py.get_hand(1)
        back_pix = None
        back_path = os.path.join(ASSETS_DIR, 'uno_back.png')
        if os.path.exists(back_path):
            back_pix = QtGui.QPixmap(back_path).scaledToWidth(60, QtCore.Qt.FastTransformation)
        for _ in range(len(ai_hand)):
            lbl = QtWidgets.QLabel()
            if back_pix:
                lbl.setPixmap(back_pix)
            else:
                lbl.setText('🂠')
            self.ai_layout.addWidget(lbl)

        # update status and turn counter
        current = engine_py.get_current_player()
        if current == 0:
            self.status_label.setText('✅ Your turn!')
        else:
            self.status_label.setText('🤖 AI is thinking...')
        
        self.turn_counter.setText(f'Turn: {self.turn_count}')

    def _is_card_playable(self, color, value):
        top_color, top_val = engine_py.get_top_discard()
        return color == top_color or value == top_val

    def _load_card_image(self, color, value):
        color_map = {
            'Red': 'red',
            'Green': 'green',
            'Blue': 'blue',
            'Yellow': 'yellow'
        }
        color_prefix = color_map.get(color, color.lower())
        filename = f"{color_prefix}-{value}-card-clipart-lg.png"
        filepath = os.path.join(ASSETS_DIR, filename)
        if os.path.exists(filepath):
            return QtGui.QPixmap(filepath)
        return None

    def add_move_history(self, player_name, action):
        self.move_history.append(f"[{self.turn_count}] {player_name}: {action}")
        # Keep only last 10 moves
        if len(self.move_history) > 10:
            self.move_history.pop(0)
        self.history_text.setPlainText('\n'.join(self.move_history))

    def play_card(self, pos):
        ok = engine_py.play_card(0, pos)
        if not ok:
            QtWidgets.QMessageBox.warning(self, 'Invalid Move', 'That card cannot be played here.')
            return
        
        hand = engine_py.get_hand(0)
        if pos <= len(hand):
            color, value = hand[pos - 1]
            self.add_move_history('You', f'Played {color} {value}')
        
        self.status_label.setText('🤖 AI is playing...')
        QtWidgets.QApplication.processEvents()
        
        # AI moves
        engine_py.ai_move()
        self.turn_count += 1
        self.refresh_ui()
        
        ai_hand = engine_py.get_hand(1)
        if ai_hand:
            self.add_move_history('AI', f'Played a card (hand: {len(ai_hand)})')
        
        winner = engine_py.check_winner()
        if winner != -1:
            msg = '🎉 You win! Congratulations!' if winner == 0 else '🤖 AI wins! Better luck next time.'
            WinOverlay(self, msg, winner)

    def on_draw(self):
        res = engine_py.draw_card(0)
        self.add_move_history('You', 'Drew a card')
        self.status_label.setText('🤖 AI is playing...')
        QtWidgets.QApplication.processEvents()
        
        # AI moves
        engine_py.ai_move()
        self.turn_count += 1
        self.refresh_ui()
        
        winner = engine_py.check_winner()
        if winner != -1:
            msg = '🎉 You win! Congratulations!' if winner == 0 else '🤖 AI wins! Better luck next time.'
            WinOverlay(self, msg, winner)

    def on_end_turn(self):
        engine_py.next_turn()
        if engine_py.get_current_player() == 1:
            self.status_label.setText('🤖 AI is playing...')
            QtWidgets.QApplication.processEvents()
            engine_py.ai_move()
            self.add_move_history('AI', 'Played a card')
            engine_py.next_turn()
        self.turn_count += 1
        self.refresh_ui()
        
        winner = engine_py.check_winner()
        if winner != -1:
            msg = '🎉 You win! Congratulations!' if winner == 0 else '🤖 AI wins! Better luck next time.'
            WinOverlay(self, msg, winner)

    def on_new_game(self):
        engine_py.init()
        self.turn_count = 1
        self.move_history = []
        self.history_text.setPlainText('')
        self.refresh_ui()
        self.status_label.setText('✅ New game started. Your turn!')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
