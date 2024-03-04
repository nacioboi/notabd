from DebugMode import DebugMode

from typing import Callable
import inspect
import re



# NOTE: to illustrate that this is the old version of the class and we're updating to use the Logger class.
print = None



class _InfoInjector:



	def inject(self, globals, locals):
		def wrapper_one(original_func):
			def wrapper_two(*args, **kwargs):
				pass
			return wrapper_two
		return wrapper_one

	def add_instruction(self, instruction:"dict"):
		def wrapper_one(original_func):
			def wrapper_two(*args, **kwargs):
				pass
			return wrapper_two
		return wrapper_one



	def inject_debug_info(self, instructions:"list[dict]", globals, locals) -> "Callable":
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
				
				code = self._get_generated_func(original_func, instructions)

				# For some edge cases, we must sanitize the generated function.
				# For example, if, in the instructions, we call the original function...
				# This will throw an error, because the original function doesn't exist in this context.
				complete = False
				while not complete:
					code, complete = self._sanitize_generated_func(code, original_func)

				# NOTE: FOR DEBUGGING PURPOSES...
				print(code)

				externals = instructions[0].get("externals", [])

				# The below loads the generated function into the global scope.
				# We force it to save the function as a global variable.
				exec(code, globals, locals)

				locals["args"] = args
				locals["kwargs"] = kwargs

				# The below runs the generated function and saves the return value.
				exec(f"__ret__ = __{original_func.__name__}__(*args, **kwargs)", globals, locals)

				return locals["__ret__"]

			return wrapper_two
		return wrapper_one
		# End of `def inject_debug_info(self, instructions:"list[dict]") -> "Callable"`



	###########
	# HELPERS #
	###########



	def _sanitize_generated_func(self, generated_func, original_func) -> "tuple[str,bool]":
		try:

			completely_sanitized = True

			# Pass 1: if the original function is called, replace it with the modified function name.
			compiled = re.compile(rf"\b{original_func.__name__}\b\s*\(")
			line_of_original_func_call = None
			lines = generated_func.split("\n")
			for i, line in enumerate(lines):
				if compiled.search(line):
					completely_sanitized = False
					lines[i] = compiled.sub(f"__{original_func.__name__}__(", line)
					line_of_original_func_call = i
					break
			

			# We must wrap this in an exec statement.
			#prefix_i = None
			#for i, c in enumerate(lines[line_of_original_func_call]):
			#	if c not in [" ", "\t"]:
			#		prefix_i = i
			#		break
			#assert prefix_i is not None
			#new = ""
			#new += lines[line_of_original_func_call][:prefix_i] 
			#new += f"exec('{lines[line_of_original_func_call][prefix_i:]}', globals(), locals())"
			#lines[line_of_original_func_call] = new
			## Then we run into even more problems, because if inside the exec statement is more "'" characters,
			##   it will break.
			## So we must escape all "'" characters.
			#line = lines[line_of_original_func_call][prefix_i+6:-23]
			#j = 0
			#for i, char in enumerate(line):
			#	if char == "'":
			#		new = ""
			#		new += line[:i+j]
			#		new += "\\"
			#		new += line[i+j:]
			#		line = new
			#		j += 1
			#new = ""
			#new += lines[line_of_original_func_call][:prefix_i+6]
			#new += line
			#new += lines[line_of_original_func_call][-23:]
			#lines[line_of_original_func_call] = new

			return "\n".join(lines), completely_sanitized
		
		except Exception as e:
			print(e)
			return generated_func, True
		# End of `def _sanitize_generated_func(self, generated_func, original_func) -> "str":`
	


	def _get_generated_func(self, original_func, instructions) -> "str":
		for instruction in instructions:
			if not self._is_valid_instruction(instruction):
				raise Exception("Invalid instruction")

		# Step 1: get original function source code...
		source = inspect.getsource(original_func)
		original_func_name = original_func.__name__

		# Step 2: remove the function decorator call from the original source code...
		source = self._remove_decorator_call(source, original_func_name)
		lines = source.split("\n")

		# Step 4: find the indentation type...
		# TODO: TEST THIS WITH DIFFERENT INDENTATIONS...
		# I use tabs, idk if it works with spaces...
		indentation_type = self._get_indentation_type(lines)
		
		# If we have multiple instructions, we need to add some value j to the line number.
		# This is because we are adding lines to the source code, and the line numbers will change.
		j = 0
		for instruction in instructions:
			if instruction.get("externals") is not None:
				continue
			line, code = instruction["line"], instruction["code"]
			line += j
			prefix = indentation_type*self._get_indentation_level(lines, line, indentation_type)
			# Step 5: inject the code...
			for l in code:
				lines.insert(line, f"{prefix}{l}")
				j += 1
				line += 1

		# Step 6: rename the function...
		self._rename_function(lines, original_func_name)

		return "\n".join(lines)

		# End of `def _get_generated_func(self, original_func, instructions):`
			


	def _get_indentation_level(self, lines, line, indentation_type) -> "int":

		indentation_level = 0
		compare_buff = ""

		for c in lines[line-1]:
			keep_going = True
			while keep_going:
				if compare_buff == indentation_type:
					indentation_level += 1
					compare_buff = ""
					break

				if c == indentation_type[len(compare_buff)]:
					compare_buff += c
					continue
				else:
					compare_buff = ""
				
				keep_going = False

		# check if the previous line has a ":" at the end.
		prev_line = lines[line-1]
		if prev_line[-1] == ":":
			indentation_level += 1

		return indentation_level

		# End of `def _get_indentation_level(self, lines, line):`



	def _is_valid_instruction(self, instruction) -> "bool":
		ret = True
		contains_line_or_code = False

		for key in ["line", "code"]:
			if not key in instruction:
				ret = False
			else:
				contains_line_or_code = True

		if not contains_line_or_code:
			if len(instruction) == 1 and instruction.get("externals") is not None:
				ret = True

		return ret
	
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



	def _get_indentation_type(self, lines) -> "str":
		indentation_type = None

		for li in range(len(lines)):
			for j, c in enumerate(lines[li]):
				if c not in [" ", "\t"]:
					break
				if c == "\t":
					indentation_type = "\t"
					break

		if indentation_type is None:
			raise Exception("Unsupported indentation type.")

		return indentation_type
	
		# End of `def _get_indentation_type(self, lines):`



	def _rename_function(self, lines, original_func_name):
		for li in range(len(lines)):
			for j, c in enumerate(lines[li]):
				if self._find_if_str_ahead(lines[li], j, f"def {original_func_name}"):

					new_line = lines[li][:j]
					new_line += f"def __{original_func_name}__" + lines[li][j+len(f"def {original_func_name}"):]
					lines[li] = new_line

		# End of `def _rename_function(self, lines, original_func_name):`



	def _find_if_str_ahead(self, source, i, str) -> "bool":

		s = source[i:i+len(str)]
		return s == str

		# End of `def _find_if_str_ahead(self, source, i, str):`

