from typing import Callable
import inspect
import re







class _InfoInjector:



	def inject(self, globals, locals):
		def wrapper_one(original_func):
			def wrapper_two(*args, **kwargs):
				pass
			return wrapper_two
		return wrapper_one
	


	def add_instruction(self, line:"int", debug_mode:"str", debug_context:"str",
		     		  args_for_logger:"tuple", **kwargs_for_logger
	):
		def wrapper_one(original_func):
			def wrapper_two(*args, **kwargs):
				pass
			return wrapper_two
		return wrapper_one
	


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


InfoInjector = _InfoInjector()