import dataclasses
from typing import Any, Callable







DEBUG_MODES:"dict[str,ADebugMode]" = {}
LOGGER_INSTANCE = None
IO_WRAPPER_INSTANCE = None






# NOTE: `io_based_on_context`
# -- if `True`, then the `write_to_file` and `write_to_io` will be assigned in the debug context instead.
# -- if `False`, 

@dataclasses.dataclass
class ADebugMode:
	io_based_on_context: bool
	write_to_file: str|None
	write_to_io: int|None
	extends_from: str|None







class _DebugMode:
	def __getattribute__(self, __name: str) -> Any:
		global DEBUG_MODES
		if __name in DEBUG_MODES:
			return DEBUG_MODES[__name]
		else:
			raise AttributeError(f"DebugMode has no attribute {__name}")







DebugMode = _DebugMode()



# TODO:
# a few more things to add to our debug system:
# 1. different formats for the debug output.
# 2. different categories like in unreal engine.
# -- unreal engine has a system where you can filter out different categories like "rendering", "physics", "ai", etc.
# -- this would be useful for a large project.
# 3. a way to save the debug output to a file.
# 4. a way to decode the file.
# 5. and a way to easily filter the debug output from the file.
