"""
info inject is a module allowing you to compile python source code with added debug information.
this means that the interesting parts of the code stay separate from printing and other debug code.
"""







from typing import Any, Callable
from enum import Enum
import inspect
import json, os
import re

class DebugMode(Enum):
	Disabled = 0
	Release = 1
	Debug = 2







class _InfoInjector:



	def __init__(self, debug_mode_:"DebugMode"=DebugMode.Disabled) -> None:

		self.debug_mode = debug_mode_

		# End of `def __init__(self, debug_mode_:"DebugMode"=DebugMode.Disabled) -> None:`
	


	def set_debug_mode(self, new_debug_mode:"DebugMode"):

		self.debug_mode = new_debug_mode

		# End of `def set_debug_mode(self, new_debug_mode:"DebugMode"):`



	def inject_debug_info(self, instructions:"list[dict]") -> "Callable":
		"""
		summary goes here
		
		Args:
			instructions (list[dict]): _description_

		Returns:
			Callable: _description_

		# NOTE: Notes for self.
		# this function is a decorator factory.
		# it replaces the original function with this one.
		# meaning that any reference to the original function will use this function instead.

		# this enabled decorators to be used with arguments.
		# it works because this will be returned before the starting parenthesis.
		# so `@InfoInjector.inject_debug_info` will be `wrapper_one``, and
		# then `wrapper_one` will be called when the opening parenthesis is reached.
		"""
		def wrapper_one(original_func):
			def wrapper_two(*args, **kwargs):

				generated_func = self._get_generated_func(original_func, instructions)

				# TODO: DEBUG
				lines = generated_func.split("\n")
				for li in range(len(lines)):
					lines[li] = lines[li][1:]
				generated_func = "\n".join(lines)
				print(generated_func)
				# TODO: END DEBUG

				exec(generated_func)

				# The below piece of black magic actually allows returning any kind of value from the 
				#   generated function.
				exec(f"__ret__ = __{original_func.__name__}__(*args, **kwargs)")
				return locals()["__ret__"]

			return wrapper_two
		return wrapper_one
		# End of `def inject_debug_info(self, instructions:"list[dict]") -> "Callable"`



	###########
	# HELPERS #
	###########


	def _get_generated_func(self, original_func, instructions) -> "str":
		# Step 1: get original function source code...
		source = inspect.getsource(original_func)
		original_func_name = original_func.__name__

		# Step 2: remove the function decorator call from the original source code...
		source = self._remove_decorator_call(source, original_func_name)
		lines = source.split("\n")

		# Step 3: get the min indentation...
		min_indentation_level = None
		for li in range(len(lines)):
			if lines[li].strip().endswith(":"):
				min_indentation_level = len(lines[li]) - len(lines[li].lstrip())
				break
		assert min_indentation_level is not None

		# Step 4: find the indentation type...Q
		# TODO: TEST THIS WITH DIFFERENT INDENTATIONS...
		# I use tabs, idk if it works with spaces...
		indentation_type = None
		for li in range(len(lines)):
			for j, c in enumerate(lines[li]):
				if c == " ":
					indentation_type = " "
					break
				elif c == "\t":
					indentation_type = "\t"
					break
		assert indentation_type is not None

		for instruction in instructions:
			if not self._is_valid_instruction(instruction):
				raise Exception("Invalid instruction")
			line, x = instruction["line"], instruction["x"]
			x_is_list = isinstance(x, list)
			prefix = indentation_type*(min_indentation_level+1)
			if x_is_list:
				x = f"\n{prefix}".join(x)
				x = f"{prefix}{x}"
			# Step 5: inject the code...
			lines.insert(line, x)

		# Step 6: rename the function...
		for li in range(len(lines)):
			for j, c in enumerate(lines[li]):
				if self._find_if_str_ahead(lines[li], j, f"def {original_func_name}"):
					new_line = lines[li][:j]
					new_line += f"def __{original_func_name}__" + lines[li][j+len(f"def {original_func_name}"):]
					lines[li] = new_line

		return "\n".join(lines)

		# End of `def _get_generated_func(self, original_func, instructions):`
			


	def _is_valid_instruction(self, instruction) -> "bool":

		for key in ["line", "x"]:
			if not key in instruction:
				return False

		return True
	
		# End of `def _is_valid_instruction(self, instruction):`



	def _remove_decorator_call(self, source, original_func_name) -> "str":

		lines = source.split("\n")
		line_no_of_end_of_decorator_call = None

		# compile our regex pattern
		pattern = r"\bdef\s+" + re.escape(original_func_name) + r"\s*\("
		compiled = re.compile(pattern)

		for i, line in enumerate(lines):
			# check if the line contains the pattern
			if compiled.search(line):
				line_no_of_end_of_decorator_call = i
				break

		if line_no_of_end_of_decorator_call is None:
			raise Exception("Failure of regex")
		
		lines = lines[line_no_of_end_of_decorator_call:]
		return "\n".join(lines)

		# End of `def _remove_decorator_call(self, source, original_func_name):`



	def _find_if_str_ahead(self, source, i, str) -> "bool":

		s = source[i:i+len(str)]
		return s == str

		# End of `def _find_if_str_ahead(self, source, i, str):`






InfoInjector = _InfoInjector()