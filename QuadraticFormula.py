import sys
import cmath
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QFormLayout, QLabel, QLineEdit, QPushButton, QComboBox, QStyleFactory, QApplication, QMessageBox, 
)
from PyQt6.QtGui import QDoubleValidator, QFont
from PyQt6.QtCore import Qt

from pyqtgraph import mkPen, PlotWidget

class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle('Quadratic Formula')
        self.setGeometry(100, 100, 600, 800)

        layout = QVBoxLayout()

        # Grouping input fields and labels
        input_group_box = QGroupBox('Enter Coefficients')
        input_layout = QFormLayout()
        input_group_box.setLayout(input_layout)

        # QLabel widget for 'a'
        a_label = QLabel('a:')
        self.a_line_edit = QLineEdit()
        self.a_line_edit.setValidator(QDoubleValidator())
        input_layout.addRow(a_label, self.a_line_edit)

        # QLabel widget for 'b'
        b_label = QLabel('b:')
        self.b_line_edit = QLineEdit()
        self.b_line_edit.setValidator(QDoubleValidator())
        input_layout.addRow(b_label, self.b_line_edit)

        # QLabel widget for 'c'
        c_label = QLabel('c:')
        self.c_line_edit = QLineEdit()
        self.c_line_edit.setValidator(QDoubleValidator())
        input_layout.addRow(c_label, self.c_line_edit)

        layout.addWidget(input_group_box)

        # QPushButton to get values
        button = QPushButton("Get Values")
        button.clicked.connect(self.get_values)
        layout.addWidget(button)

        # Button to show steps to answer
        button = QPushButton("Steps to Answer")
        button.clicked.connect(self.steps_to_answer)
        layout.addWidget(button)
        
        # QLabel to display the roots
        self.display_result1_label = QLabel()
        self.display_result1_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.display_result1_label)
        self.display_result2_label = QLabel()
        self.display_result2_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.display_result2_label)
        
        # result display
        font = QFont("Arial", 11)
        self.display_result1_label.setFont(font)
        self.display_result2_label.setFont(font)

        # QComboBox for theme selection
        theme_combo_box = QComboBox()
        theme_combo_box.addItem("Light Theme")
        theme_combo_box.addItem("Dark Theme")
        theme_combo_box.addItem("Sepia Theme")
        theme_combo_box.currentIndexChanged.connect(self.change_theme)
        layout.addWidget(theme_combo_box)

        # QComboBox for the style selection
        style_combo_box = QComboBox()
        styles = QStyleFactory.keys()
        fusion_index = styles.index("Fusion")
        style_combo_box.addItems(styles)
        style_combo_box.setCurrentIndex(fusion_index)
        style_combo_box.currentIndexChanged.connect(self.change_style)
        layout.addWidget(style_combo_box)

        # Graph
        self.plot_widget = PlotWidget(background="w")
        layout.addWidget(self.plot_widget)
        self.setLayout(layout)
        # Show the window
        self.show()

    ######################  LOGIC  #########################
    ##### Show Answers ########
    def get_values(self):
        a_text = self.a_line_edit.text()
        b_text = self.b_line_edit.text()
        c_text = self.c_line_edit.text()

        try:
            # Validate input
            if not a_text or not b_text or not c_text:
                raise ValueError("Values not entered")

            global a,b,c
            
            a = float(a_text)
            b = float(b_text)
            c = float(c_text)

            if a == 0:
                raise ValueError("'a' cannot be zero")
        
            # Calculate roots
            discriminant = (b * b) - (4 * a * c)
            global sol1, sol2
            sol1 = str((-b - cmath.sqrt(discriminant)) / (2 * a))
            sol2 = str((-b + cmath.sqrt(discriminant)) / (2 * a))
            sol1 = sol1.replace("(", "").replace(")", "").replace("j", " i")
            sol2 = sol2.replace("(", "").replace(")", "").replace("j", " i")
            self.display_result1_label.setText(f"Root 1: {sol1}") # Display Root 1
            self.display_result2_label.setText(f"Root 2: {sol2}") # Display Root 2
            
            # Graph
            x_values = [i for i in range(-50, 51)]
            y_values = [(a * (xi ** 2) + b * xi + c)for xi in x_values]
            self.plot_widget.clear()
            self.plot_widget.plotItem.showGrid(True, True, 0.7)  # Show grid lines
            # Set the x-axis range
            self.plot_widget.plotItem.setXRange(-50, 50)
            # Set the y-axis range
            self.plot_widget.plotItem.setYRange(-50, 50)
            self.plot_widget.plotItem.getAxis("bottom").setPen(mkPen(color="#000000"))  # Set x-axis color
            self.plot_widget.plotItem.getAxis("left").setPen(mkPen(color="#000000"))  # Set y-axis color
            self.plot_widget.plot(x_values, y_values,
                                  symbol='o')  # Plot the function

        except ValueError as e:
            # Handle specific value-related errors using QMessageBox
            self.display_result1_label.setText("Values not entered")

        except ZeroDivisionError:
            self.display_result1_label.setText("'a' cannot be zero")

        except Exception as e:
            # Handle other exceptions
            self.display_result1_label.setText("An error occurred")
            print(f"Error: {e}")

    ######## Steps to answers ########
    
    def steps_to_answer(self):
        try: 
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Pop-up Window")
            
            # Set multiple lines of detailed text
            detailed_text = "ax^2 + bx + c\n"
            detailed_text += f"{a}x^2 + {b}x + {c}\n"
            detailed_text += "-b ± sqrt(b^2 - 4ac) / 2a\n"
            detailed_text += f"-{b} ± sqrt({b}^2 - 4*{a}*{c}) / 2*{a}\n"
            detailed_text += f"Result 1: {sol1}\n"
            detailed_text += f"Result 2:{sol2}"
            
            msg_box.setText(detailed_text)
            msg_box.setIcon(QMessageBox.Icon.Information)
            
            # Add buttons to the pop-up
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            
            # Set the default button to Ok
            msg_box.setDefaultButton(QMessageBox.StandardButton.Ok)
            
            # Display the pop-up
            msg_box.exec()
        
        except ValueError as e:
            # Handle specific value-related errors using QMessageBox
            self.display_result1_label.setText("Values not entered")

        except ZeroDivisionError:
            self.display_result1_label.setText("'a' cannot be zero")

        except Exception as e:
            # Handle other exceptions
            self.display_result1_label.setText("An error occurred \n Have all values been entered?")
        

    ######################  THEME #########################

    def change_theme(self, index):
        if index == 0:
            # Apply light theme -- the code is repeated so it changes when either option is selected
            self.setStyleSheet("background-color: #FFFFFF; color: #000000;")
            self.plot_widget.plotItem.showGrid(True, True, 0.7)  # grid colour and transparency
            # Set the graph's background color to white
            self.plot_widget.setBackground("w")
            self.plot_widget.getAxis("bottom").setPen(mkPen(color="#000000"))  # Set the bottom axis color to black
            self.plot_widget.getAxis("left").setPen(mkPen(color="#000000"))  # Set the left axis color to black
            self.plot_widget.getAxis("bottom").setStyle(tickTextOffset=10)  # Adjust the tick text offset

        elif index == 1:
            # Apply dark theme
            self.setStyleSheet("background-color: #121212; color: #FFFFFF;")
            self.plot_widget.plotItem.showGrid(True, True, 0.7)  # grid colour and transparency
            # Set the graph's background color to black
            self.plot_widget.setBackground("k")
            self.plot_widget.getAxis("bottom").setPen(mkPen(color="#FFFFFF"))  # Set the bottom axis color to white
            self.plot_widget.getAxis("left").setPen(mkPen(color="#FFFFFF"))  # Set the left axis color to white
            self.plot_widget.getAxis("bottom").setStyle(tickTextOffset=10)  # Adjust the tick text offset
            
        elif index == 2:
            # Apply sepia theme
            self.setStyleSheet("background-color: #F5DEB3; color: #704214;")
            self.plot_widget.plotItem.showGrid(True, True, 0.7)  # grid colour and transparency
            # Set the graph's background color to sepia
            self.plot_widget.setBackground("#D2B48C")
            self.plot_widget.getAxis("bottom").setPen(mkPen(color="#704214"))  # Set the bottom      axis color to a dark brown
            self.plot_widget.getAxis("left").setPen(mkPen(color="#704214"))  # Set the left axis         color to a dark brown
            self.plot_widget.getAxis("bottom").setStyle(tickTextOffset=10)  # Adjust the tick text offset

    ######################  STYLE #########################

    def change_style(self, index):
        # Store the selected style index
        self.selected_style_index = index
        styles = QStyleFactory.keys()
        selected_style = styles[self.selected_style_index]
        QApplication.setStyle(selected_style)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Create the main window
    window = MainWindow()

    # Make the style start as fusion
    app.setStyle("Fusion")

    # Start the event loop
    sys.exit(app.exec())
