from ColorConfiguration import ColorConfiguration
from DebugMode import DEBUG_MODES, ADebugMode






DEBUG_CONTEXTS = {}
ACTIVE_DEBUG_CONTEXT = None







class DebugContext:



	def __init__(self, name:str) -> None:
		self.format_layers = []
		self.color_config = None



	def add_format_layer(self, formatter):
		self.format_layers.append(formatter)



	def set_color_configuration(self, color_config:ColorConfiguration):
		self.color_config = color_config

	

	def handle(self, write_to_file, write_to_io, level, message):
		if write_to_io is None and write_to_file is None:
			raise Exception("write_to_io and write_to_file cannot both be None.")

		modes = []
		for item in DEBUG_MODES.items():
			if type(item) != ADebugMode:
				raise Exception("item is not an ADebugMode.")
			modes.append(item)
		mode_list =  sorted(modes, key=lambda x: x[1].extends_from)

		for i, mode in enumerate(mode_list):
			print(i, mode[0], mode[1].extends_from)

		if write_to_file is not None:
			with open(write_to_file, "a") as f:
				f.write
			
