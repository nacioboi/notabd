from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeView, QVBoxLayout, QWidget, QLabel, QComboBox, QPushButton
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import sys, os







PLATFORM = os.name

if PLATFORM == "nt":
	PLATFORM = "windows"
elif PLATFORM == "posix":
	PLATFORM = "unix"
else:
	raise Exception("Unknown platform: {}".format(PLATFORM))







print("When we launch commands, we will need to know the terminal emulator you use.")
print("You MUST enter the exact system command that launches your terminal emulator.")
print("NOTE: Some terminals will not work since our implementation is not perfect.")
print("NOTE: Confirmed working terminals are:\n\t- `wt` (Windows Terminal)")
TERM = input("Enter the command that launches your terminal emulator: ")







class MainWindow(QMainWindow):



	def __init__(self):
		super().__init__()

		self.setWindowTitle("notadb - Project Running & Testing Tool")
		self.setGeometry(100, 100, 800, 600)

		self.items_properties = {}
		self.commands_by_id_for_windows = {}
		self.commands_by_id_for_unix = {}

		self.properties_layout = None

		self.initUI()



	def add_item_to_tree(self, item_model, text, properties):
		element = QStandardItem(text)

		self.items_properties[text] = properties

		item_model.appendRow(element)

		return element



	def add_action_step_to_button(self, platform, element_id, command):
		if platform == "windows":
			if self.commands_by_id_for_windows.get(element_id) is None:
				self.commands_by_id_for_windows[element_id] = []
			self.commands_by_id_for_windows[element_id] += [command]
		elif platform == "unix":
			if self.commands_by_id_for_unix.get(element_id) is None:
				self.commands_by_id_for_unix[element_id] = []
			self.commands_by_id_for_unix[element_id] += [command]



	def _add_chat_app_server_to_tree(self, item_model, wsl_path_of_cwd, root_of_proj_dir):
		chat_app_desc = "An EXTREMELY basic chat app that uses our `supersocket` library for networking."

		self.add_item_to_tree(item_model, "Chat App - Server", {
			"INFO": {
				"Exact Path": f"{root_of_proj_dir}/example/chat_app/server.py",
				"Type": "Example Code",
				"Description": chat_app_desc
			},
			"BUTTON": {
				"id": "chat_app.server.run_button",
				"text": "Run (Needs WSL (Arch) for `rsync` to work)" if PLATFORM == "windows" else "Run"
			}
		})

		# Windows commands.
		chat_app_subroutines_dir = f"{root_of_proj_dir}\\proj_tester\\chat_app_subroutines\\windows"
		self.add_action_step_to_button("windows", "chat_app.server.run_button",
			f"{chat_app_subroutines_dir}\\launch_server.bat " +
			f"{chat_app_subroutines_dir} {wsl_path_of_cwd} {root_of_proj_dir}"
		)

		# Unix commands.
		self.add_action_step_to_button("unix", "chat_app.server.run_button",
			f"bash -c \"cd {wsl_path_of_cwd} && ./rsync_for_examples.sh\""
		)
		self.add_action_step_to_button("unix", "chat_app.server.run_button",
			f"python3 {root_of_proj_dir}/example/chat_app/server.py"
		)
		self.add_action_step_to_button("unix", "chat_app.server.run_button",
			f"bash -c \" cd {wsl_path_of_cwd} && ./kill_rsync_for_examples.sh\""
		)



	def _add_chat_app_client_to_tree(self, item_model, wsl_path_of_cwd, root_of_proj_dir):
		chat_app_desc = "An EXTREMELY basic chat app that uses our `supersocket` library for networking."

		self.add_item_to_tree(item_model, "Chat App - Client", {
			"INFO": {
				"Exact Path": f"{root_of_proj_dir}/example/chat_app/client.py",
				"Type": "Example Code",
				"Description": chat_app_desc
			},
			"BUTTON": {
				"id": "chat_app.client.run_button",
				"text": "Run (Needs WSL (Arch) for `rsync` to work)" if PLATFORM == "windows" else "Run"
			}
		})

		# Windows commands.
		chat_app_subroutines_dir = f"{root_of_proj_dir}\\proj_tester\\chat_app_subroutines\\windows"
		self.add_action_step_to_button("windows", "chat_app.client.run_button",
			f"{chat_app_subroutines_dir}\\launch_client.bat " +
			f"{chat_app_subroutines_dir} {wsl_path_of_cwd} {root_of_proj_dir}"
		)

		# Unix commands.
		self.add_action_step_to_button("unix", "chat_app.client.run_button",
			f"bash -c \"cd {wsl_path_of_cwd} && ./rsync_for_examples.sh\""
		)
		self.add_action_step_to_button("unix", "chat_app.client.run_button",
			f"python3 {root_of_proj_dir}/example/chat_app/client.py"
		)
		self.add_action_step_to_button("unix", "chat_app.client.run_button",
			f"bash -c \"cd {wsl_path_of_cwd} && ./kill_rsync_for_examples.sh\""
		)



	def _add_injecting_to_tree(self, item_model, wsl_path_of_cwd, root_of_proj_dir):
		injecting_desc = "An example of how to use the `InfoInjector` as part of our `pls` logging module."

		self.add_item_to_tree(item_model, "Injecting", {
			"INFO": {
				"Exact Path": f"{root_of_proj_dir}/example/injecting/foo.py",
				"Type": "Example Code",
				"Description": injecting_desc
			},
			"BUTTON": {
				"id": "injecting.run_button",
				"text": "Run (Needs WSL (Arch) for `rsync` to work)" if PLATFORM == "windows" else "Run"
			}
		})

		# Windows commands.
		self.add_action_step_to_button("windows", "injecting.run_button",
			f"wsl -d Arch bash -c \"cd {wsl_path_of_cwd} && ./rsync_for_examples.sh\""
		)
		self.add_action_step_to_button("windows", "injecting.run_button",
			f"python3.11.exe {root_of_proj_dir}\\example\\injecting\\foo.py"
		)
		self.add_action_step_to_button("windows", "injecting.run_button",
			f"wsl -d Arch \"cd {wsl_path_of_cwd} && ./kill_rsync_for_examples.sh\""
		)

		# Unix commands.
		self.add_action_step_to_button("unix", "injecting.run_button",
			f"bash -c \"cd {wsl_path_of_cwd} && ./rsync_for_examples.sh\""
		)
		self.add_action_step_to_button("unix", "injecting.run_button",
			f"python3 {root_of_proj_dir}/example/injecting/foo.py"
		)
		self.add_action_step_to_button("unix", "injecting.run_button",
			f"bash -c \"cd {wsl_path_of_cwd} ./kill_rsync_for_examples.sh\""
		)



	def add_all_items_to_tree(self, item_model):
		wsl_path_of_cwd = os.path.abspath(".")
		wsl_path_of_cwd = wsl_path_of_cwd.replace("\\", "/")
		wsl_path_of_cwd = f"/mnt/{wsl_path_of_cwd[0].lower()}{wsl_path_of_cwd[2:]}"

		root_of_proj_dir = os.path.abspath("..")

		examples_item = self.add_item_to_tree(item_model, "Example Code", {})

		self._add_chat_app_server_to_tree(examples_item, wsl_path_of_cwd, root_of_proj_dir)
		self._add_chat_app_client_to_tree(examples_item, wsl_path_of_cwd, root_of_proj_dir)
		
		self._add_injecting_to_tree(examples_item, wsl_path_of_cwd, root_of_proj_dir)



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
		commands = None

		if PLATFORM == "windows":
			commands = self.commands_by_id_for_windows[command_id]
		elif PLATFORM == "unix":
			commands = self.commands_by_id_for_unix[command_id]

		assert commands is not None

		# Open in a new terminal
		cmd = " && ".join(commands)
		cmd = cmd.replace("\"", "\\\"")

		if PLATFORM == "windows":
			print(f"Running command: `{TERM} cmd.exe /k \"{cmd}\"`...")
		elif PLATFORM == "unix":
			print(f"Running command: `{TERM} -e \"{cmd}\"`...")

		root_proj_dir = os.path.abspath("..")

		if PLATFORM == "windows":
			try:
				os.chdir("..")
				os.system(f"{TERM} cmd.exe /k \"{cmd}\"")
			finally:
				os.chdir(f"{root_proj_dir}/proj_tester")
		elif PLATFORM == "unix":
			try:
				os.chdir("..")
				os.system(f"{TERM} -e \"{cmd}\"")
			finally:
				os.chdir(f"{root_proj_dir}/proj_tester")



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
