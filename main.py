import time
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QWidget, 
                             QGridLayout, QVBoxLayout, QHBoxLayout, QLabel, 
                             QComboBox, QFrame, QGraphicsDropShadowEffect, QLineEdit, QMessageBox)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor
import sys
from puzzle_solver import PuzzleSolver
from complexity_analyzer import ComplexityAnalyzer


class GlassTile(QPushButton):
    def __init__(self, value):
        super().__init__()
        self.value = value
        self.setFixedSize(100, 100)
        self.setFont(QFont('Poppins', 28, QFont.Bold))
        self.setCursor(Qt.PointingHandCursor)
        self.setObjectName('glassTile')
        self.updateStyle()
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(255, 255, 255, 80))
        shadow.setOffset(-3, -3)
        self.setGraphicsEffect(shadow)

    def updateStyle(self):
        if self.value == 0:
            self.setStyleSheet("""
                QPushButton#glassTile {
                    background-color: rgba(255, 255, 255, 0.1);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: 15px;
                }
            """)
            self.setText("")
        else:
            self.setText(str(self.value))
            self.setStyleSheet("""
                QPushButton#glassTile {
                    color: white;
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                              stop:0 rgba(106, 17, 203, 0.9), 
                                              stop:1 rgba(37, 117, 252, 0.9));
                    border: 1px solid rgba(255, 255, 255, 0.3);
                    border-radius: 15px;
                }
            """)


class ModernBoard(QFrame):
    def __init__(self):
        super().__init__()
        self.tiles = []
        self.initUI()
        
    def initUI(self):
        self.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 25px;
                padding: 20px;
            }
        """)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 40))
        shadow.setOffset(8, 8)
        self.setGraphicsEffect(shadow)
        
        layout = QGridLayout()
        layout.setSpacing(12)
        
        for i in range(3):
            for j in range(3):
                tile = GlassTile(0)
                layout.addWidget(tile, i, j, Qt.AlignCenter)
                self.tiles.append(tile)
                
        self.setLayout(layout)
        
    def updateState(self, state):
        for tile, value in zip(self.tiles, state):
            tile.value = value
            tile.updateStyle()


class NeumorphicButton(QPushButton):
    def __init__(self, text, color="#6a11cb"):
        super().__init__(text)
        self.color = color
        self.setFont(QFont('Poppins', 16))  # Increased font size
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(60)  # Increased height
        self.setMinimumWidth(150)  # Increased width
        self.updateStyle(False)
        self.setToolTip(text)  # Tooltip for button

    def updateStyle(self, pressed):
        if pressed:
            style = f"""
                QPushButton {{
                    color: white;
                    background: {self.color};
                    border: none;
                    border-radius: 30px;
                    padding: 0 30px;
                }}
            """
        else:
            style = f"""
                QPushButton {{
                    color: white;
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                              stop:0 {self.color}, stop:1 #2575fc);
                    border: none;
                    border-radius: 30px;
                    padding: 0 30px;
                }}
                QPushButton:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                              stop:0 #2575fc, stop:1 {self.color});
                }}
                QPushButton:disabled {{
                    background: #cccccc;
                }}
            """
        self.setStyleSheet(style)

    def mousePressEvent(self, event):
        self.updateStyle(True)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.updateStyle(False)
        super().mouseReleaseEvent(event)


class ModernPuzzleGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("8-Puzzle Solver")
        self.analyzer = ComplexityAnalyzer()
        self.initUI()

    def initUI(self):
        self.setMinimumSize(900, 700)
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                          stop:0 #0F2027, 
                                          stop:0.5 #203A43, 
                                          stop:1 #2C5364);
            }
            QLabel {
                color: white;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(25)
        main_layout.setContentsMargins(40, 40, 40, 40)

        title = QLabel("8-Puzzle Solver")
        title.setFont(QFont('Poppins', 36, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: white; margin-bottom: 20px;")
        main_layout.addWidget(title)

        subtitle = QLabel("A visual demonstration of search algorithms")
        subtitle.setFont(QFont('Poppins', 14))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: rgba(255, 255, 255, 0.7);")
        main_layout.addWidget(subtitle)

        self.board = ModernBoard()
        main_layout.addWidget(self.board, alignment=Qt.AlignCenter)

        state_input_frame = QFrame()
        state_input_layout = QVBoxLayout(state_input_frame)
        state_input_label = QLabel("Enter Initial State (comma-separated, 0-8):")
        state_input_label.setFont(QFont('Poppins', 12))
        state_input_label.setStyleSheet("color: white;")
        self.state_input = QLineEdit()
        self.state_input.setFont(QFont('Poppins', 12))
        self.state_input.setPlaceholderText("e.g., 1,2,3,4,5,6,7,8,0")
        self.state_input.setStyleSheet("background: rgba(255, 255, 255, 0.1); color: white; padding: 5px;")
        self.state_input.setToolTip("Enter initial state as comma-separated values (0-8, e.g., 1,2,3,4,5,6,7,8,0)")
        state_input_layout.addWidget(state_input_label)
        state_input_layout.addWidget(self.state_input)
        main_layout.addWidget(state_input_frame)

        self.state_input.returnPressed.connect(self.validate_and_set_initial_state)

        controls_frame = QFrame()
        controls_frame.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 25px;
                padding: 20px;
            }
        """)

        controls_layout = QHBoxLayout(controls_frame)
        controls_layout.setSpacing(20)

        algo_label = QLabel("Select Algorithm:")
        algo_label.setFont(QFont('Poppins', 12))

        # ComboBox for selecting algorithm
        self.algo_combo = QComboBox()
        self.algo_combo.addItems(["BFS", "DFS", "UCS"])
        self.algo_combo.setStyleSheet("""
            QComboBox {
                font-size: 32px;
                padding: 6px;
                background-color: #2C5364;
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
            }

            QComboBox QAbstractItemView {
                font-size: 28px;
                min-width: 180px;
                background-color: #203A43;
                color: white;
                selection-background-color: #2575fc;
                border-radius: 10px;
            }

            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
        """)

        self.solve_button = NeumorphicButton("Solve Puzzle")
        self.solve_button.setToolTip("Click to solve the puzzle using the selected algorithm")
        self.reset_button = NeumorphicButton("Reset", "#e74c3c")
        self.reset_button.setToolTip("Click to reset the puzzle to a random solvable state")

        controls_layout.addWidget(algo_label)
        controls_layout.addWidget(self.algo_combo)
        controls_layout.addStretch()
        controls_layout.addWidget(self.solve_button)
        controls_layout.addWidget(self.reset_button)

        main_layout.addWidget(controls_frame)

        stats_layout = QVBoxLayout()

        # Time Complexity
        time_layout = QHBoxLayout()
        self.time_label = QLabel("Time Complexity:")
        self.time_label.setFont(QFont('Poppins', 12))
        self.time_complexity = QLabel("N/A")
        self.time_complexity.setFont(QFont('Poppins', 12, QFont.Bold))
        time_layout.addWidget(self.time_label)
        time_layout.addWidget(self.time_complexity)
        stats_layout.addLayout(time_layout)

        # Space Complexity
        space_layout = QHBoxLayout()
        self.space_label = QLabel("Space Complexity:")
        self.space_label.setFont(QFont('Poppins', 12))
        self.space_complexity = QLabel("N/A")
        self.space_complexity.setFont(QFont('Poppins', 12, QFont.Bold))
        space_layout.addWidget(self.space_label)
        space_layout.addWidget(self.space_complexity)
        stats_layout.addLayout(space_layout)

        # Elapsed Time
        elapsed_time_layout = QHBoxLayout()
        elapsed_time_label = QLabel("Elapsed Time:")
        elapsed_time_label.setFont(QFont('Poppins', 12))
        self.elapsed_time = QLabel("N/A")
        self.elapsed_time.setFont(QFont('Poppins', 12, QFont.Bold))
        elapsed_time_layout.addWidget(elapsed_time_label)
        elapsed_time_layout.addWidget(self.elapsed_time)
        stats_layout.addLayout(elapsed_time_layout)

        main_layout.addLayout(stats_layout)

        self.solve_button.clicked.connect(self.solvePuzzle)
        self.reset_button.clicked.connect(self.resetPuzzle)
        self.resetPuzzle()

    def validate_and_set_initial_state(self):
        try:
            input_state = list(map(int, self.state_input.text().split(',')))
            # Check if input contains numbers from 0 to 8 (unordered)
            if len(input_state) != 9 or set(input_state) != set(range(9)):
                raise ValueError("State must contain numbers from 0 to 8 in any order.")
            if not PuzzleSolver.is_solvable(input_state):
                raise ValueError("The state is not solvable.")

            self.state_input.setStyleSheet("background: rgba(255, 255, 255, 0.1); color: white;")  # Reset color
            self.current_state = input_state
            self.board.updateState(self.current_state)
            self.time_complexity.setText("N/A")
            self.space_complexity.setText("N/A")
            self.elapsed_time.setText("N/A")
        except ValueError as e:
            QMessageBox.warning(self, "Invalid Input", str(e))
            self.state_input.setStyleSheet("background: rgba(255, 0, 0, 0.3);")  # Change color on error

    def resetPuzzle(self):
        self.current_state = PuzzleSolver.generate_solvable_state()
        self.board.updateState(self.current_state)
        self.time_complexity.setText("N/A")
        self.space_complexity.setText("N/A")
        self.elapsed_time.setText("N/A")

    def solvePuzzle(self):
        self.solve_button.setEnabled(False)
        algorithm = self.algo_combo.currentText()

        solve_function = {
            "BFS": PuzzleSolver.bfs,
            "DFS": PuzzleSolver.dfs,
            "UCS": PuzzleSolver.ucs
        }.get(algorithm)

        if not solve_function:
            QMessageBox.warning(self, "Algorithm Error", "Please select a valid algorithm.")
            self.solve_button.setEnabled(True)
            return

        start_time = time.time()
        result = solve_function(self.current_state)
        elapsed_time = time.time() - start_time

        if result:
            path, states, nodes_explored = result
            complexity = self.analyzer.analyze(algorithm, nodes_explored, len(path))
            self.animateSolution(states)
            QTimer.singleShot(500 * len(states), lambda: self.updateComplexity(complexity, elapsed_time))  # Wait for the animation to complete
        else:
            self.time_complexity.setText("No solution found!")
            self.space_complexity.setText("N/A")
            self.elapsed_time.setText("N/A")
            self.solve_button.setEnabled(True)

    def animateSolution(self, states):
        if states:
            self.board.updateState(states.pop(0))
            QTimer.singleShot(500, lambda: self.animateSolution(states))
        else:
            self.solve_button.setEnabled(True)

    def updateComplexity(self, complexity, elapsed_time):
        """Update complexity values after animation."""
        self.time_complexity.setText(complexity['time'])
        self.space_complexity.setText(complexity['space'])
        self.elapsed_time.setText(f"{elapsed_time*100:.2f} seconds")

    def animateSolution(self, states):
        if states:
            self.board.updateState(states.pop(0))
            QTimer.singleShot(500, lambda: self.animateSolution(states))
        else:
            self.solve_button.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    gui = ModernPuzzleGUI()
    gui.show()
    sys.exit(app.exec_())