from typing import Callable
import inspect
import re







class _InfoInjector:



	def __init__(self):

		self._instruction_stack = []

		# End of `__init__`



	def inject(self, globals, locals):
		def wrapper_one(original_func):
			def wrapper_two(*args, **kwargs):
				
				code = self._get_generated_func(original_func, self._instruction_stack)

				# For some edge cases, we must sanitize the generated function.
				# For example, if, in the instructions, we call the original function...
				# This will throw an error, because the original function doesn't exist in this context.
				complete = False
				while not complete:
					code, complete = self._sanitize_generated_func(code, original_func)

				# NOTE: FOR DEBUGGING PURPOSES...
				print(code)

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
		# End of `def inject(self, globals, locals):`



	def add_instruction(self, line:"int", debug_mode:"str", debug_context:"str",
		     		  args_for_logger:"tuple", **kwargs_for_logger
	):
		def wrapper_one(original_func):
			self._instruction_stack.append({
				"line": line,
				"debug_mode": debug_mode,
				"debug_context": debug_context,
				"args_for_logger": args_for_logger,
				"kwargs_for_logger": kwargs_for_logger
			})
			return original_func
		return wrapper_one
		# End of `add_instruction`
	


	class VariableReference:
		"""
		When calling `InfoInjector.add_instruction`, you may use this class to reference variables.

		For example:
		```python
		@InfoInjector.add_instruction(line=1, debug_mode="info", debug_context="generic", args_to_logger=(
			f"n = {InfoInjector.VariableReference("n")}"
		))
		@InfoInjector.inject(globals(), locals())
		def fib(n):
			if n <= 1:
				return n
			else:
				return fib(n-1) + fib(n-2)
		```
		
		> When the code is put together to create our new function:

		```python
		def fib(n):
			Logger().generic.info(f"n = {n}")
			if n <= 1:
				return n
			else:
				return fib(n-1) + fib(n-2)
		```

		> Notice the new line that was added.

		Basically, the `VariableReference` class is used as a placeholder for the variable `n`.
		It does not actually fetch anything at any time.

		This is because python does the fetching when the newly compiled function is called.
		"""

		SALT = "|`VARIABLE_REFERENCE`|"

		def __init__(self, name:"str"):
			self.name = name

		def __repr__(self):
			return f"{self.SALT}{self.name}{self.SALT}"



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
	


	def _get_generated_func(self, original_func, instruction_stack) -> "str":
		for instruction in instruction_stack:
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
		while len(instruction_stack) > 0:
			instruction = instruction_stack.pop(-1)
			line_no = instruction["line"]
			debug_mode = instruction["debug_mode"]
			debug_context = instruction["debug_context"]
			args_for_logger = instruction["args_for_logger"]
			kwargs_for_logger = instruction["kwargs_for_logger"]
			
			# Replace the newline character with the repr for such.
			for i, arg in enumerate(args_for_logger):
				for y, c in enumerate(arg):
					if c == "\n":
						args_for_logger[i] = arg[:y-1] + "\\n" + arg[y+1:]
			for key in kwargs_for_logger.keys():
				value = kwargs_for_logger[key]
				i = 0
				while True:
					try:
						c = value[i]
					except IndexError:
						break
					if c == "\n":
						value = value[:i] + "\\n" + value[i+1:]
						i += 2
					else:
						i += 1
				kwargs_for_logger[key] = value

			args_for_logger = self._parse_variable_references(args_for_logger)
			args_for_logger = [f"f\"{arg}\"" for arg in args_for_logger]

			line_no += j
			prefix = indentation_type*self._get_indentation_level(lines, line_no, indentation_type)

			# Step 5: inject the code...
			new_line = f"{prefix}pls().{debug_context}.{debug_mode}("
			new_line += ", ".join(args_for_logger)

			for key, value in kwargs_for_logger.items():
				new_line += f", {key}=\"{value}\""

			new_line += ")"

			for line in new_line.split("\n"):
				lines.insert(line_no, line)
				line_no += 1
				j += 1

		# Step 6: rename the function...
		self._rename_function(lines, original_func_name)

		return "\n".join(lines)

		# End of `def _get_generated_func(self, original_func, instructions):`
			


	def _parse_variable_references(self, args_for_logger:"tuple") -> "list[str]":
		list_copy = []

		for arg in args_for_logger:
			list_copy.append(arg)

		for i, arg in enumerate(list_copy):
			if isinstance(arg, self.VariableReference):
				list_copy[i] = f"{{{arg.name}}}"
			new = list_copy[i]
			x = 0
			assert isinstance(new, str)
			while self.VariableReference.SALT in new:
				x += 1
				pos = new.find(self.VariableReference.SALT)
				if x == 1:
					new = new[:pos] + "{" + new[pos+len(self.VariableReference.SALT):]
				else:
					new = new[:pos] + "}" + new[pos+len(self.VariableReference.SALT):]
				if x == 2:
					x = 0
			list_copy[i] = new

		return list_copy

		# End of `def _parse_variable_references(self, args_for_logger):`



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

		# TODO: do we need this function?

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




InfoInjector = _InfoInjector()