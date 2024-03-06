from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeView, QVBoxLayout, QWidget, QLabel, QComboBox, QPushButton
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import sys, os

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		self.setWindowTitle("notadb - Project Running & Testing Tool")
		self.setGeometry(100, 100, 800, 600)

		self.items_properties = {}
		self.commands_by_id = {}

		self.properties_layout = None

		self.initUI()

	def add_item_to_tree(self, item_model, text, properties):
		element = QStandardItem(text)


		self.items_properties[text] = properties

		item_model.appendRow(element)

		return element

	def add_action_step_to_interactive_element(self, element_id, command):
		if self.commands_by_id.get(element_id) is None:
			self.commands_by_id[element_id] = []
		self.commands_by_id[element_id] += [command]

	def add_all_items_to_tree(self, item_model):
		wsl_path = os.getcwd()
		wsl_path = wsl_path.replace("\\", "/")
		wsl_path = f"/mnt/{wsl_path[0].lower()}{wsl_path[2:]}"

		examples_item = self.add_item_to_tree(item_model, "Example Code", {})

		chat_app_desc = "An EXTREMELY basic chat app that uses our `supersocket` library for networking."
		self.add_item_to_tree(examples_item, "Chat App - Server", {
			"INFO": {
				"Exact Path": os.getcwd() + "/example/chat_app/server.py",
				"Type": "Example Code",
				"Description": chat_app_desc
			},
			"BUTTON": {
				"id": "chat_app.server.run_button",
				"text": "Run on WSL2 (Arch Linux)"
			}
		})
		self.add_action_step_to_interactive_element("chat_app.server.run_button", f"wsl -d Arch bash -c \"{wsl_path}/rsync_for_examples.sh\"")
		self.add_action_step_to_interactive_element("chat_app.server.run_button", f"python3.11.exe {os.getcwd()}\\example\\chat_app\\server.py")
		self.add_action_step_to_interactive_element("chat_app.server.run_button", f"wsl -d Arch \"{wsl_path}/kill_rsync_for_examples.sh\"")

		chat_app_desc = "An EXTREMELY basic chat app that uses our `supersocket` library for networking."
		self.add_item_to_tree(examples_item, "Chat App - Client", {
			"INFO": {
				"Exact Path": os.getcwd() + "/example/chat_app/client.py",
				"Type": "Example Code",
				"Description": chat_app_desc
			},
			"BUTTON": {
				"id": "chat_app.client.run_button",
				"text": "Run on WS2 (Arch Linux)"
			}
		})
		self.add_action_step_to_interactive_element("chat_app.client.run_button", f"wsl -d Arch bash -c \"{wsl_path}/rsync_for_examples.sh\"")
		self.add_action_step_to_interactive_element("chat_app.client.run_button", f"python3.11.exe {os.getcwd()}\\example\\chat_app\\client.py")
		self.add_action_step_to_interactive_element("chat_app.client.run_button", f"wsl -d Arch \"{wsl_path}/kill_rsync_for_examples.sh\"")

		injecting_desc = "An example of how to use the `InfoInjector` as part of our `pls` logging module."
		self.add_item_to_tree(examples_item, "Injecting", {
			"INFO": {
				"Exact Path": os.getcwd() + "/example/injecting/foo.py",
				"Type": "Example Code",
				"Description": injecting_desc
			},
			"BUTTON": {
				"id": "injecting.run_button",
				"text": "Run"
			}
		})
		self.add_action_step_to_interactive_element("tests.run_button", f"wsl -d Arch bash -c \"{wsl_path}/rsync_for_examples.sh\"")
		self.add_action_step_to_interactive_element("tests.run_button", f"python3.11.exe {os.getcwd()}\\example\\injecting\\foo.py")
		self.add_action_step_to_interactive_element("tests.run_button", f"wsl -d Arch \"{wsl_path}/kill_rsync_for_examples.sh\"")

		tests_desc = "A TEMPORARY FILE USED FOR TESTING."
		self.add_item_to_tree(item_model, "Temporary Testing @ `./src/tests.py`", {
			"INFO": {
				"Exact Path": os.getcwd() + "/src/tests.py",
				"Type": "TEMPORARY TESTING FILE",
				"Description": tests_desc
			},
			"BUTTON": {
				"id": "tests.run_button",
				"text": "Run on Windows"
			}
		})
		self.add_action_step_to_interactive_element("tests.run_button", f"python3.11.exe {os.getcwd()}\\src\\tests.py")

	def initUI(self):
		layout = QVBoxLayout()

		tree_view = QTreeView()
		model = QStandardItemModel()
		root_item = model.invisibleRootItem()

		self.add_all_items_to_tree(root_item)

		tree_view.setModel(model)
		tree_view.selectionModel().selectionChanged.connect( # type: ignore
			lambda selected, deselected: self.update_properties_panel(selected.indexes()[0], model) # type: ignore
		)
		layout.addWidget(tree_view)

		properties_panel = QWidget()
		properties_layout = QVBoxLayout()
		properties_panel.setLayout(properties_layout)

		properties_label = QLabel("Properties Panel")
		properties_layout.addWidget(properties_label)

		layout.addWidget(properties_panel)

		central_widget = QWidget()
		central_widget.setLayout(layout)

		self.setCentralWidget(central_widget)

		self.properties_layout = properties_layout

	def run_command(self, command_id):
		commands = self.commands_by_id[command_id]

		# Open in a new terminal
		cmd = " && ".join(commands)
		cmd = cmd.replace("\"", "\\\"")

		print(f"Running command: {cmd}")

		os.system(f"wt cmd.exe /k \"cd {os.getcwd()} && {cmd}\"")

	def update_properties_panel(self, selected_index, model):
		selected_item = model.itemFromIndex(selected_index)
		properties_layout = self.properties_layout

		for i in range(0, properties_layout.count()): # type: ignore
			properties_layout.itemAt(i).widget().deleteLater() # type: ignore

		properties_label = QLabel("Properties for {}".format(selected_item.text()))
		properties_layout.addWidget(properties_label) # type: ignore

		properties = self.items_properties[selected_item.text()]

		info = properties.get("INFO")

		if not info:
			return

		info = QLabel("Type: {}\nPath: {}\nDescription: {}".format(
			info["Type"],
			info["Exact Path"],
			info["Description"]
		))
		properties_layout.addWidget(info) # type: ignore

		props = [x for x in properties.keys() if x != "INFO"]
		for prop in props:
			item = properties[prop]
			if prop == "COMBO_BOX":
				item_id = item["id"]
				item_text = item["text"]
				item_choices = item["choices"]
				item = QComboBox()
				for choice in item_choices:
					item.addItem(choice)
				properties_layout.addWidget(item) # type: ignore
			elif prop == "BUTTON":
				item_id = item["id"]
				item_text = item["text"]
				item = QPushButton(item_text)
				item.clicked.connect(lambda: self.run_command(item_id))
				properties_layout.addWidget(item) # type: ignore




if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	sys.exit(app.exec_())
