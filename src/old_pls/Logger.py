from typing import Any, Callable

from DebugMode import ADebugMode, DEBUG_MODES
from DebugContext import DebugContext, DEBUG_CONTEXTS







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

	# TODO: this code was taken from a similar project of mine.
	# TODO:   We need to adjust the commented out sections to apply to this project.
	#if self.do_print_logs:
	#	print(str, **kwargs)

	for kwarg in kwargs:
		if kwarg == "end":
			continue
		else:
			raise Exception(f"Unknown keyword argument {kwarg}.")

	if "end" in kwargs:
		str += kwargs["end"]

	# TODO: this code was taken from a similar project of mine.
	# TODO:   We need to adjust the commented out sections to apply to this project.
	#self._add_contents_to_log(base64.b64encode(str.encode("utf-8")).decode("utf-8"))







RUNTIME_HELPER_INSTANCE = None
"""
THIS GLOBAL VARIABLE IS NONE OF YOUR CONCERN!!
See the documentation attached to the `_Logger` class for more info.
"""
RUNTIME_HELPER_CHILDREN = {}
"""
THIS GLOBAL VARIABLE IS NONE OF YOUR CONCERN!!
See the documentation attached to the `_Logger` class for more info.
"""







class RUNTIME_HELPER:



	"""
	THIS CLASS IS NONE OF YOUR CONCERN!!
	"""



	def __init__(self, initial=False) -> None:
		if not initial:
			return
		global RUNTIME_HELPER_INSTANCE
		if RUNTIME_HELPER_INSTANCE is not None:
			raise Exception("Logger already initialized")
		RUNTIME_HELPER_INSTANCE = self



	def __getattribute__(self, __name: str) -> Any:
		global RUNTIME_HELPER_CHILDREN

		if __name in RUNTIME_HELPER_CHILDREN:
			return RUNTIME_HELPER_CHILDREN[__name]
		
		raise AttributeError(f"no attribute {__name}.")
		






class _Logger:



	"""
	The actual meat and potatoes of the amazing infoinject library. ^_^

	Short NOTE: This is using a singleton class to make the usage of this API a bit more user-friendly.

	Attributes:
	- vars (dict): 	A dictionary of variables that are used to store, among other configurations, 
			  the global context and the global mode.
	
	Methods:
	- __call__: 		Used to return the `RUNTIME_HELPER_INSTANCE` variable. [SEE] below for more info.
	- _add_debug_mode: 	Used by `add_debug_mode`, underscores usually denote an inner function.
	- add_debug_mode: 	Used to add a debug mode to the system. [SEE] `ADebugMode` in `DebugMode.py`.
				  It takes `name`(str) and any of `write_to_file`(str|None), `write_to_io`(int|None), and
				  `extends_from`(str|None).
				  `write_to_file` is the file to write to (if any).
				  `write_to_io` is the io object to write to (if any).
				  NOTE: You must specify at least one of `write_to_file` or `write_to_io`.
				  `level` should be stated here even though it is not a parameter. [SEE] below.
	- add_debug_context: 	Used to add a debug context to the system. [SEE] `DebugContext` in `DebugContext.py`.
				  This works a bit differently than `add_debug_mode` because contexts are a bit more
				  complicated than modes.
				  You simply pass the `name`(str) of the context and then later on you can modify it.
	- get_debug_context: 	Used to get a debug context by its key.
				  Like i said, you can modify the debug contexts after they are created. [SEE] below!
	- set: 			Used to set a variable in the `vars` dictionary. [SEE] below for more info.

	More info on the `RUNTIME_HELPER_INSTANCE`:

	> Take the following code for example:
	```py
	Logger.set("global_context", "generic")
	Logger.set("global_mode", "info")

	Logger.add_debug_mode("info", write_to_io=1)
	Logger.add_debug_context("generic")
	```
	> Here, we have set the global context to "generic" and the global mode to "info".
	> We have also set the global mode to "info" and added a debug context called "generic".

	> So when we go:
	```py
	Logger().info("This is using the generic context.")
	```

	> The `Logger()` part returns the `RUNTIME_HELPER_INSTANCE` variable.

	> This way we can have dynamic debug modes and debug contexts and the intellisense will not throw a fit. ^_^

	More info on the `level` attribute of the `ADebugMode` class:

	> The `level` attribute is automatically assigned when calling the `add_debug_mode` method.
	> This means you must specify the precedence based on the order you call the `add_debug_mode` method.
	> You can (but should not) make your own debug mode with the `ADebugMode` class.

	More info on the `get_debug_context` method:

	> Take the following code for example:
	```py
	Logger.add_debug_context("generic")
	```
	> We've seen this before. We've added a debug context called "generic".
	> Now if we want to access the debug context in order to change it, for example, add a format layer:
	```py
	Logger.get_debug_context("generic").add_format_layer(TimeFormatter)
	```
	> This uses the included time formatter to add the time before each log message.
	> There is other things you can do but that's the basic idea.

	More info on the `set` method:
	> The currently supported variables are:
	- `global_context` (str): 	The global context to use.
	> Take the following code:
	```py
	Logger.add_debug_mode("info", write_to_io=1)
	Logger.add_debug_context("generic")
	Logger().generic.info("This is using the generic context.")
	```
	> This might become tedious if you have to specify the context every time.
	> So you can set the global context and mode like so:
	```py
	Logger.set("global_context", "generic")
	Logger.set("global_mode", "info")
	```
	> Now you can just do:
	```py
	Logger().info("This is using the generic context.")
	```

	"""



	def __init__(self) -> None:
		"""
		YOU MUST NEVER CALL THIS DIRECTLY.

		Raises:
		    Exception: If the Logger is already initialized. Hence why i said never call this directly.

		Side Effects:
		- Adds a "disabled" debug mode to the system.
		"""
		global pls
		try:
			if pls is not None:
				raise Exception("Logger already initialized")
		except NameError:
			pass
		pls = self

		self.vars = {}

		pls._add_debug_mode("disabled", None, None, 0)


	def __call__(self, *args: Any, **kwds: Any) -> Any:
		return RUNTIME_HELPER_INSTANCE


	def _add_debug_mode(self, name:"str", write_to_file:"str|None", write_to_io:"int|None", level:"int"):
		"""
		YOU MUST NEVER CALL THIS DIRECTLY.

		This is an inner function used by the `add_debug_mode` method (note without the underscore).
		"""

		global DEBUG_MODES, RUNTIME_HELPER_CHILDREN

		if name in DEBUG_MODES:
			raise Exception(f"Debug mode {name} already exists.")

		DEBUG_MODES[name] = ADebugMode(write_to_file, write_to_io, level)
		def mylittlehandler(message):
			context = DEBUG_CONTEXTS[self.vars["global_context"]]
			mode = DEBUG_MODES[name]
			DEBUG_MODES[name].handle_global(context, mode, message)

		if self.vars.get("global_context") is not None:
			# If we have a global context AMD we have not set that up yet, we need to set it up.
			assert RUNTIME_HELPER_INSTANCE is not None

			already_set = False

			for child in RUNTIME_HELPER_CHILDREN:
				if not child.startswith("-"):
					already_set = True
					break
			
			if not already_set:
				RUNTIME_HELPER_CHILDREN[name] = mylittlehandler
				return

		def myotherhandler(context, message):
			context["obj"].handle(write_to_file, write_to_io, level, message)

		# update all the contexts.
		for child in RUNTIME_HELPER_CHILDREN:
			if not child.startswith("-"):
				continue
			context = RUNTIME_HELPER_CHILDREN[child]
			def x(message):
				nonlocal context
				myotherhandler(context, message)
			context[name] = x



					


	
	def add_debug_mode(self, name:"str", **kwargs):
		"""
		Adds a debug mode to the system.

		Args:
		    name (str): The name of the debug mode.
		
		Optional Keyword Args:
		- write_to_file (str|None): 	The file to write to (if any).
		- write_to_io (int|None): 	The io object to write to (if any).

		NOTE: You must specify at least one of `write_to_file` or `write_to_io`.
		"""

		global DEBUG_MODES
		write_to_file = kwargs.get("write_to_file", None)
		write_to_io = kwargs.get("write_to_io", None)
		separate = kwargs.get("separate", False)
		if separate:
			level = 0
		else:
			level = len(DEBUG_MODES)+1
		self._add_debug_mode(name, write_to_file, write_to_io, level)

	

	def add_debug_context(self, name:"str"):
		global DEBUG_CONTEXTS
		if name in DEBUG_CONTEXTS:
			raise Exception(f"Debug context {name} already exists.")
		DEBUG_CONTEXTS[name] = DebugContext(name)
		RUNTIME_HELPER_CHILDREN[f"-{name}"] = RUNTIME_HELPER()
		setattr(RUNTIME_HELPER_CHILDREN[f"-{name}"], "obj", DEBUG_CONTEXTS[name])


	

	def get_debug_context(self, key) -> DebugContext:
		global DEBUG_CONTEXTS
		return DEBUG_CONTEXTS[key]
	


	def set(self, key, value):
		acceptable_var_keys = ["global_context"]

		if key not in acceptable_var_keys:
			raise Exception(f"Unknown variable {key}.")

		self.vars[key] = value

		





RUNTIME_HELPER(True)

"""
Below is the Logger global variable.
We are doing things a bit different.

We are using the Logger as a singleton class of `_Logger`.
Its a bit of a hack but it makes the usage of this API pretty nice.
"""
pls:"_Logger" = _Logger()



# TODO:
# a few more things to add to our debug system:
# 1. different formats for the debug output.
# 2. different categories like in unreal engine.
# -- unreal engine has a system where you can filter out different categories like "rendering", "physics", "ai", etc.
# -- this would be useful for a large project.
# 3. a way to save the debug output to a file.
# 4. a way to decode the file.
# 5. and a way to easily filter the debug output from the file.
