from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFormLayout,
    QSpinBox,
    QScrollArea,
    QMessageBox,
    QStatusBar,
)
from config import CORE_ATTRIBUTES
from data_handler import SaveDataHandler


class AttributeEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("人物属性修改器 (Sultan's Game)")
        self.setGeometry(100, 100, 600, 500)

        self.data_handler = SaveDataHandler()
        self.selected_card_index = -1
        self.attribute_widgets = {}

        self._init_ui()
        self.load_save_file()

    def _init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # 文件路径显示与加载
        file_layout = QHBoxLayout()
        self.file_path_label = QLineEdit(self.data_handler.save_file_path)
        self.file_path_label.setReadOnly(True)
        self.load_button = QPushButton("加载存档")
        self.load_button.clicked.connect(self.load_save_file)
        file_layout.addWidget(QLabel("存档路径:"))
        file_layout.addWidget(self.file_path_label, 1)
        file_layout.addWidget(self.load_button)
        main_layout.addLayout(file_layout)

        # 查找区域
        find_layout = QHBoxLayout()
        self.find_input = QLineEdit()
        self.find_input.setPlaceholderText("输入 UID 或 ID")
        self.find_button = QPushButton("查找角色")
        self.find_button.clicked.connect(self.find_card)
        find_layout.addWidget(QLabel("查找 (UID/ID):"))
        find_layout.addWidget(self.find_input)
        find_layout.addWidget(self.find_button)
        main_layout.addLayout(find_layout)

        # 选定角色信息
        self.selected_card_label = QLabel("当前未选择角色")
        main_layout.addWidget(self.selected_card_label)

        # 属性编辑区域
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.attr_widget = QWidget()
        self.attr_layout = QFormLayout(self.attr_widget)
        self.scroll_area.setWidget(self.attr_widget)
        main_layout.addWidget(self.scroll_area, 1)

        # 操作按钮区域
        action_layout = QHBoxLayout()
        self.set_99_button = QPushButton("核心属性设为 99")
        self.set_99_button.clicked.connect(self.set_core_attributes_to_99)
        self.set_99_button.setEnabled(False)
        self.save_changes_button = QPushButton("保存修改")
        self.save_changes_button.clicked.connect(self.save_changes)
        self.save_changes_button.setEnabled(False)
        action_layout.addWidget(self.set_99_button)
        action_layout.addStretch()
        action_layout.addWidget(self.save_changes_button)
        main_layout.addLayout(action_layout)

        # 状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("请先加载存档文件。")

    def update_status(self, message, timeout=5000):
        self.status_bar.showMessage(message, timeout)
        print(f"Status: {message}")

    def load_save_file(self):
        self.clear_attribute_display()
        self.selected_card_index = -1
        self.set_99_button.setEnabled(False)
        self.save_changes_button.setEnabled(False)
        self.selected_card_label.setText("当前未选择角色")

        success, message = self.data_handler.load_save_file()
        self.update_status(message)
        if not success:
            QMessageBox.warning(self, "错误", message)

    def find_card(self):
        if not self.data_handler.game_data:
            self.update_status("请先成功加载存档文件。")
            QMessageBox.warning(self, "提示", "请先加载存档文件。")
            return

        search_term = self.find_input.text().strip()
        if not search_term:
            self.update_status("请输入要查找的 UID 或 ID。")
            QMessageBox.warning(self, "提示", "请输入要查找的 UID 或 ID。")
            return

        try:
            search_value = int(search_term)
        except ValueError:
            self.update_status("输入无效，UID 和 ID 必须是数字。")
            QMessageBox.warning(self, "输入错误", "UID 和 ID 必须是数字。")
            return

        found_index, card_info = self.data_handler.find_card(search_value)
        if found_index != -1:
            self.selected_card_index = found_index
            uid = card_info.get("uid", "未知")
            card_id = card_info.get("id", "未知")
            self.selected_card_label.setText(f"已选择角色: UID={uid}, ID={card_id}")
            self.populate_attribute_display()
            self.set_99_button.setEnabled(True)
            self.save_changes_button.setEnabled(True)
            self.update_status(f"找到角色: UID={uid}, ID={card_id}")
        else:
            self.selected_card_index = -1
            self.selected_card_label.setText("未找到匹配的角色")
            self.clear_attribute_display()
            self.set_99_button.setEnabled(False)
            self.save_changes_button.setEnabled(False)
            self.update_status(f"未找到 UID 或 ID 为 {search_value} 的角色。")
            QMessageBox.information(
                self, "未找到", f"未能找到 UID 或 ID 为 {search_value} 的角色卡片。"
            )

    def clear_attribute_display(self):
        while self.attr_layout.count() > 0:
            item = self.attr_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.attribute_widgets = {}

    def populate_attribute_display(self):
        self.clear_attribute_display()

        if self.selected_card_index == -1 or not self.data_handler.game_data:
            return

        card_data = self.data_handler.game_data["cards"][self.selected_card_index]
        if "tag" not in card_data or not isinstance(card_data.get("tag"), dict):
            card_data["tag"] = {}
            self.update_status("注意：为选定角色创建了空的 'tag' 字典。", 3000)

        tags = card_data.get("tag", {})
        all_tag_keys = set(tags.keys())
        display_keys = set(CORE_ATTRIBUTES) | all_tag_keys

        sorted_keys = CORE_ATTRIBUTES + sorted(
            [k for k in display_keys if k not in CORE_ATTRIBUTES]
        )

        for key in sorted_keys:
            value = tags.get(key, 0)

            if isinstance(value, (int, float)):
                spin_box = QSpinBox()
                spin_box.setRange(-9999, 99999)
                spin_box.setValue(int(value))
                self.attr_layout.addRow(QLabel(f"{key}:"), spin_box)
                self.attribute_widgets[key] = spin_box
            else:
                display_value = str(value)
                if len(display_value) > 50:
                    display_value = display_value[:47] + "..."
                value_label = QLineEdit(display_value)
                value_label.setReadOnly(True)
                self.attr_layout.addRow(QLabel(f"{key} (非数值):"), value_label)

        self.update_status("已加载角色属性。")

    def set_core_attributes_to_99(self):
        if self.selected_card_index == -1:
            self.update_status("错误：没有选定的角色。")
            return

        if not self.attribute_widgets:
            self.update_status("错误：属性控件未加载。")
            return

        changed = False
        for attr_name in CORE_ATTRIBUTES:
            if attr_name in self.attribute_widgets:
                widget = self.attribute_widgets[attr_name]
                if isinstance(widget, QSpinBox):
                    widget.setValue(99)
                    changed = True

        if changed:
            self.update_status("核心属性值已在界面上设置为 99 (尚未保存)。", 3000)
        else:
            self.update_status("未找到可设置的核心属性控件。", 3000)

    def save_changes(self):
        if self.selected_card_index == -1 or not self.data_handler.game_data:
            self.update_status("错误：没有选定的角色或未加载存档。")
            QMessageBox.warning(self, "错误", "请先查找并选择一个角色。")
            return

        attributes = {}
        for attr_name, widget in self.attribute_widgets.items():
            if isinstance(widget, QSpinBox):
                attributes[attr_name] = widget.value()

        success, message = self.data_handler.save_changes(
            self.selected_card_index, attributes
        )
        self.update_status(message)

        if success:
            QMessageBox.information(
                self, "成功", f"修改已保存到:\n{self.data_handler.save_file_path}"
            )
        else:
            QMessageBox.critical(
                self, "保存失败", f"{message}\n\n请检查文件权限或磁盘空间。"
            )
