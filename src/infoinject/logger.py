import base64
from typing import Any, Callable

from .debug_mode import ADebugMode, DEBUG_MODES




"""


"""






def _debug_print(self, prefix:str, *args, **kwargs):
	str = f"{prefix}"
	for arg in args:
		str += f"{arg} "
	str += "\033[0m"
	if self.do_print_logs:
		print(str, **kwargs)
	for kwarg in kwargs:
		if kwarg == "end":
			continue
		else:
			raise Exception(f"Unknown keyword argument {kwarg}.")
	if "end" in kwargs:
		str += kwargs["end"]
	self._add_contents_to_log(base64.b64encode(str.encode("utf-8")).decode("utf-8"))





LOGGER_INSTANCE = None







class Logger:



	def __init__(self) -> None:
		global LOGGER_INSTANCE
		if LOGGER_INSTANCE is not None:
			raise Exception("Logger already initialized")
		LOGGER_INSTANCE = self

		self.add_debug_mode("Disabled", None, None, None)



	def add_debug_mode(self, name:"str", write_to_file:"str|None", write_to_io:"int|None", extends_from:"str|None"):
		global DEBUG_MODES

		if name in DEBUG_MODES:
			raise Exception(f"Debug mode {name} already exists.")

		if extends_from == name:
			raise Exception(f"OK, now you're just being silly!")

		if extends_from is not None:
			if extends_from not in DEBUG_MODES:
				raise Exception(f"Debug mode {extends_from} does not exist.")
			base_write_to_file = DEBUG_MODES[extends_from].write_to_file
			base_write_to_io = DEBUG_MODES[extends_from].write_to_io
			if write_to_file is not None and base_write_to_file is not None:
				raise Exception(f"A DebugMode must inherit the `write_to_file` attribute from its parent.")
			if write_to_io is not None and base_write_to_io is not None:
				raise Exception(f"A DebugMode must inherit the `write_to_io` attribute from its parent.")
			if write_to_file is None:
				write_to_file = base_write_to_file
			if write_to_io is None:
				write_to_io = base_write_to_io

		DEBUG_MODES[name] = ADebugMode(write_to_file, write_to_io, extends_from)





LOGGER_INSTANCE = Logger()



# TODO:
# a few more things to add to our debug system:
# 1. different formats for the debug output.
# 2. different categories like in unreal engine.
# -- unreal engine has a system where you can filter out different categories like "rendering", "physics", "ai", etc.
# -- this would be useful for a large project.
# 3. a way to save the debug output to a file.
# 4. a way to decode the file.
# 5. and a way to easily filter the debug output from the file.
