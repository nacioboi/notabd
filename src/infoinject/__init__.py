"""
info inject is a module allowing you to compile python source code with added debug information.
this means that the interesting parts of the code stay separate from printing and other debug code.
"""

from typing import Callable
from enum import Enum
import json, os

from ._ai import ensure_ai_is_initialized
from ._ai import get_ai_response



class DebugMode(Enum):
	Release = 0
	Debug = 1


class InfoInjector:
	def __init__(self, **kwargs):
		self.compilation_result_path = kwargs["compilation_result_path"]
		self.dont_save_compilation = kwargs["dont_save_compilation"]
		self.debug_mode = DebugMode.Release
		self.test_args_for_active_functions = {}

	def _ensure_compilation_result_exists(self):
		if self.dont_save_compilation:
			os.remove(self.compilation_result_path)
		if not os.path.exists(self.compilation_result_path):
			with open(self.compilation_result_path, "w") as f:
				json.dump({
					"compiled_functions": {},
				}, f)

	def _add_compiled_function(self, name, code):
		self._ensure_compilation_result_exists()
		if self.dont_save_compilation:
			return
		json_data = None
		with open(self.compilation_result_path, "r") as f:
			json_data = json.load(f)
		json_data["compiled_functions"][name] = code
		with open(self.compilation_result_path, "w") as f:
			json.dump(json_data, f)

	def _check_function_name_in_compiled_functions(self, name):
		self._ensure_compilation_result_exists()
		if self.dont_save_compilation:
			return False
		json_data = None
		with open(self.compilation_result_path, "r") as f:
			json_data = json.load(f)
		return name in json_data["compiled_functions"]
	
	def _get_compiled_function(self, name):
		self._ensure_compilation_result_exists()
		if self.dont_save_compilation:
			raise Exception("Cannot get compiled function when dont_save_compilation is True")
		json_data = None
		with open(self.compilation_result_path, "r") as f:
			json_data = json.load(f)
		return json_data["compiled_functions"][name]

	def set_debug_mode(self, debug_mode:"DebugMode"):
		self.debug_mode = debug_mode

	def inject_debug_info_using_AI(self, ai_prompt) -> "Callable":
		# NOTE: Notes for self.
		# this function is a decorator factory.
		# it replaces the original function with this one.
		# meaning that any reference to the original function will use this function instead.

		# this enabled decorators to be used with arguments.
		# it works because this will be returned before the starting parenthesis.
		# so `@InfoInjector.inject_debug_info` will be `wrapper_one``, and
		# then `wrapper_one` will be called when the opening parenthesis is reached.
		def wrapper_one(original_func):
			def wrapper_two(*args, **kwargs):
				print("one")
				ai_response = None
				ensure_ai_is_initialized()
				ai_response = get_ai_response(self, original_func, ai_prompt, self.test_args_for_active_functions[original_func.__name__])
				print(f"ai_response: [\n{ai_response}\n]", flush=True)
				self._add_compiled_function(original_func.__name__, ai_response)
				if not ai_response:
					raise Exception("ai_response is empty")
				exec(ai_response)
				eval(f"__ret__ = __{original_func.__name__}__(*args, **kwargs)", locals(), globals())
				return locals()["__ret__"]
			return wrapper_two
		return wrapper_one
	
	def provide_test_args(self, *args, **kwargs):
		def wrapper_one(original_func):
			self.test_args_for_active_functions[original_func.__name__] = (args, kwargs)
			return original_func
		return wrapper_one



def initialize(**kwargs):
	if not "compilation_result_path" in kwargs:
		raise Exception("compilation_result_path not specified")
	return InfoInjector(**kwargs)