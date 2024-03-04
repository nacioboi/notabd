from DebugContext import DebugContext, DebugMode

from typing import Any







DYNAMIC_PIE = {}
class DynamicVariableContainer:



	"""
	Represents a container for dynamically managing variables.

	This class allows you to dynamically set and retrieve variables without explicitly defining them in the class definition.

	Usage:
	```python
	# Create a DynamicVariableContainer instance
	container = DynamicVariableContainer("container1")

	# Dynamically set a variable in the container
	container.set("variable1", 10)

	# Dynamically get the value of a variable from the container
	value = container.variable1
	print(value)  # Output: 10

	# Dynamically get all the variables in the container
	variables = container.get_children()

	# Dynamically delete a variable from the container
	container.del("variable1")
	```

	Attributes:
		name (str): The name of the container.

	Notes on the hackiness of this class:
	- This class uses a global dictionary to store the variables.
	- This class uses a static method to set and delete the variables, among other things.

	Because of this, please DO NOT EVER call the static methods directly.
	Instead, use the `set`, `del`, and `get_children` methods of the instance of this class.
	Beware that you will not get good intellisense support but it WILL work, trust me bro. ^_^
	"""



	def __init__(self, name):
		global DYNAMIC_PIE

		self.name = name

		DYNAMIC_PIE[name] = {}
		DynamicVariableContainer._post_setup(name)
	


	@staticmethod
	def _post_setup(__name:str):
		global DYNAMIC_PIE

		def __wrapper_for_set(*args, **kwargs):
			DynamicVariableContainer._set(__name, *args, **kwargs)

		def __wrapper_for_del(*args, **kwargs):
			DynamicVariableContainer._del(__name, *args, **kwargs)

		def __wrapper_for_get_children(*args, **kwargs):
			return DynamicVariableContainer._get_children(__name, *args, **kwargs)

		def __wrapper_for_get_name(*args, **kwargs):
			return DynamicVariableContainer._get_name(__name, *args, **kwargs)

		DYNAMIC_PIE[__name]["set"] = __wrapper_for_set
		DYNAMIC_PIE[__name]["del"] = __wrapper_for_del
		DYNAMIC_PIE[__name]["get_children"] = __wrapper_for_get_children
		DYNAMIC_PIE[__name]["get_name"] = __wrapper_for_get_name
	


	@staticmethod
	def _set(__name_of_self:str, name: str, value) -> None:
		global DYNAMIC_PIE

		name_of_self = __name_of_self
		piece_of_pie = DYNAMIC_PIE[name_of_self]

		piece_of_pie[name] = value



	@staticmethod
	def _del(__name_of_self:str, name: str) -> None:
		global DYNAMIC_PIE

		name_of_self = __name_of_self
		piece_of_pie = DYNAMIC_PIE[name_of_self]

		del piece_of_pie[name]



	@staticmethod
	def _get_children(__name_of_self:str) -> dict:
		global DYNAMIC_PIE

		name_of_self = __name_of_self
		piece_of_pie = DYNAMIC_PIE[name_of_self]

		return piece_of_pie
	


	@staticmethod
	def _get_name(__name_of_self:str) -> str:
		return __name_of_self



	def __getattribute__(self, __name: str):
		global DYNAMIC_PIE

		name_of_self = super().__getattribute__("name")
		piece_of_pie = DYNAMIC_PIE[name_of_self]

		if __name in piece_of_pie:
			return piece_of_pie[__name]
		
		err_str = f"'{name_of_self}' object has no attribute '{__name}'"
		raise AttributeError(err_str)







class Logger:



	"""
	ACTUAL MASSIVE DISCLAIMER: THIS ENTIRE LIBRARY IS SUBJECT TO CHANGE.

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

		self.configuration_vars = {}
		self.debug_modes:"dict[str,DebugMode]" = {}
		self.debug_contexts = {}
		self.active_debug_mode = None

		self.LOGGER_HELPER = DynamicVariableContainer("LOGGER_HELPER")

		pls._add_debug_mode("disabled", 0)
		pls.get_debug_mode("disabled").set_override_do_ever_write(False)


	
	def __call__(self, *args: Any, **kwds: Any) -> Any:
		return self.LOGGER_HELPER



	def set_debug_mode(self, name:"str") -> None:
		"""
		Sets the active debug mode.

		Args:
		    name (str): The name of the debug mode to set as active.
		"""
		self.active_debug_mode = self.debug_modes[name]



	def _add_debug_mode(self, name:"str", level:"int"):
		"""
		YOU MUST NEVER CALL THIS DIRECTLY.

		This is an inner function used by the `add_debug_mode` method (note without the underscore).
		"""

		# Check that the name isn't already in use.
		if name in self.debug_modes:
			raise Exception(f"Debug mode {name} already exists.")

		# Construct the debug mode.
		self.debug_modes[name] = DebugMode(name, level, None)

		self._update_state_after_adding_debug_mode(
			name,
			level
		)

	

	def _update_state_after_adding_debug_mode(self, name_of_debug_mode, level):
		# The below wrapper is what actually gets called when you do `pls().<insert name of debug mode>(...)`
		# NOTE: Remember, this is only for the global context.
		def wrapper_for_global_handler(*args, **kwargs):
			context = self.debug_contexts[self.configuration_vars["global_context"]]
			mode = self.debug_modes[name_of_debug_mode]
			context.handle(mode, self.active_debug_mode, *args, **kwargs)

		# And here is the wrapper for when we specify a context.
		# E.g., `pls().our_context.our_debug_mode(...)`...
		# This wrapper is the `our_debug_mode` part.
		# The actual `our_context` is made in the `add_debug_context` method and it is a `DynamicVariableContainer`
		#  instance that is a child of the `LOGGER_HELPER` instance.
		def wrapper_for_context_specified_handler(context, *args, **kwargs):
			mode = self.debug_modes[name_of_debug_mode]
			context.handle(mode, self.active_debug_mode, *args, **kwargs)

		# We only want to use the `wrapper_for_global_handler` if the global context is set.
		if self.configuration_vars.get("global_context") is not None:
			self.LOGGER_HELPER.set(name_of_debug_mode, wrapper_for_global_handler)

		# Now to update the context-specific wrappers.
		keys_no_globals = [k for k in self.LOGGER_HELPER.get_children().keys() if k not in self.debug_modes.keys()]
		keys_no_globals = [k for k in keys_no_globals if k not in ["set", "del", "get_children", "get_name"]]
		for child_key in keys_no_globals:
			container = self.LOGGER_HELPER.get_children()[child_key]
			def _wrapper_for_the_wrapper(*args, **kwargs):
				nonlocal container
				context = self.debug_contexts[container.get_name()]
				wrapper_for_context_specified_handler(context, *args, **kwargs)
			container.set(name_of_debug_mode, _wrapper_for_the_wrapper)



	def add_debug_mode(self, name:"str", separate=False):
		"""
		Adds a debug mode to the system.

		Args:
		    name (str): The name of the debug mode.
		
		Optional Keyword Args:
		- write_to_file (str|None): 	The file to write to (if any).
		- write_to_io (int|None): 	The io object to write to (if any).
		- separate (bool): 		If this is a standalone debug mode, meaning, if this mode is active,
					  	  all other debug mode will not be active.

		NOTE: You must specify at least one of `write_to_file` or `write_to_io`.
		"""

		if separate:
			level = -1
		else:
			level = len(self.debug_modes)+1

		self._add_debug_mode(name, level)



	def add_debug_context(self, name:"str"):
		if name in self.debug_contexts:
			raise Exception(f"Debug context {name} already exists.")
		self.debug_contexts[name] = DebugContext(name)
		self.LOGGER_HELPER.set(name, DynamicVariableContainer(name))



	def get_debug_context(self, name:"str") -> "DebugContext":
		return self.debug_contexts[name]
	


	def get_debug_mode(self, name:"str") -> "DebugMode":
		return self.debug_modes[name]



	def set(self, name:"str", value) -> None:
		accepted_vars = ["global_context"]

		if name not in accepted_vars:
			raise Exception(f"Variable {name} not accepted.")

		self.configuration_vars[name] = value







"""
Below is the Logger global variable.
We are doing things a bit different.

We are using the `pls` as a singleton class of `Logger`.
Its a bit of a hack but it makes the usage of this API pretty nice.
"""
pls:"Logger" = Logger()