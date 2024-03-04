from io import IOBase
from DebugMode import DebugMode
from formatters.Formatter import IFormatter
from formatters.FinalFormatter import IFinalFormatter
from formatters.defaults import DefaultFinalFormatter
from Direction import IODirection

import base64







def _debug_print(self, prefix:str, *args, **kwargs):

	"""
	DO NOT CALL THIS DIRECTLY.

	At the end of the day, this is our special function that actually prints to the screen (or file).

	Args:
		prefix (str): 	The prefix to the log message.
		*args: 		The log message, works like the `print` function.
		**kwargs: 	The keyword arguments to pass to the print function.
				  Currently, only the `end` keyword argument is supported.

	Raises:
	    Exception: If an unknown keyword argument is passed.
	"""

	str = f"{prefix}"
	for arg in args:
		str += f"{arg} "
	str += "\033[0m"

	for kwarg in kwargs:
		if kwarg == "end":
			continue
		else:
			raise Exception(f"Unknown keyword argument {kwarg}.")

	if "end" in kwargs:
		str += kwargs["end"]

	self._add_contents_to_log(str)







class DebugContext:



	def __init__(self, name:str) -> None:
		self.format_layers:"list[IFormatter]" = []
		self.final_formatter:"IFinalFormatter" = DefaultFinalFormatter()

		self.can_ever_write:"bool|None" = None
		self.directions:"list[IODirection]|None" = None



	def set_final_formatter(self, formatter:"IFinalFormatter") -> None:
		self.final_formatter = formatter



	def set_can_ever_write(self, can_ever_write:bool) -> None:
		self.can_ever_write = can_ever_write



	def add_direction(self, direction:IODirection) -> None:
		if self.directions is None:
			self.directions = []
		self.directions.append(direction)



	def add_format_layer(self, formatter):
		self.format_layers.append(formatter)




	def _evaluate_instruction(self, instruction_part, arg_part):
		if instruction_part == "can_ever_write":
			self.can_ever_write = eval(arg_part)
		
		elif instruction_part == "write_to_handle":
			self.write_to_handle = eval(arg_part)

		elif instruction_part == "write_to_file":
			self.write_to_file = eval(arg_part)



	def __add_contents_to_log(self, contents:str, direction: IODirection) -> None:
		try:

			f = None

			direction.validate()

			if direction.file_handle is not None:
				f = open(direction.file_handle, "w")
			
			elif direction.file_path is not None:
				f = open(direction.file_path, "a")

			if not isinstance(f, IOBase):
				raise Exception("No file handle to write to.")
			
			f.write(contents)
			f.write("\n")

		finally:
			if isinstance(f, IOBase) and not f.closed:
				f.close()



	def _add_contents_to_log(self, contents:str) -> None:
		assert self.directions is not None, "No directions to write to."
		for direction in self.directions:
			self.__add_contents_to_log(contents, direction)



	def handle(self, debug_mode:"DebugMode", active_debug_level:"DebugMode", *args, **kwargs):
		# QUICK NOTE: the `debug_mode` parameter should be used to change the output and the
		# `active_debug_mode` parameter should be used to determine if we should write to the output.

		# First check that this context is valid.
		if self.can_ever_write is None and self.write_to_handle is None:
			raise Exception("`can_ever_write` and `write_to_handle` cannot both be None.")

		str = ""
		
		for format_layer in self.format_layers:
			str = format_layer.handle(str)
		
		str = self.final_formatter.raw_handle(str)
		
		override_instructions = debug_mode.override_instructions or []

		for instruction in override_instructions:
			instruction_part, arg_part = instruction.split("=")
			self._evaluate_instruction(instruction_part, arg_part)

		# All conditions where we cannot write.
		if active_debug_level.level == -1 and debug_mode.level == -1:
			if not active_debug_level.name == debug_mode.name:
				return
		elif active_debug_level.level < debug_mode.level:
			return
		elif self.can_ever_write is None or (self.can_ever_write is not None and not self.can_ever_write):
			return

		if active_debug_level.level >= debug_mode.level:
			_debug_print(self, str, *args, **kwargs)
			return

		raise Exception("This should never happen.")
			
