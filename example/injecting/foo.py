from pls import pls
from pls.Direction import IODirection
import sys



# The below sets the global context to generic.
pls.set("global_context", "generic")



# Below is adding a debug context.
# It is a bit more complicated than setting up debug contexts so you dont have to set all the parameters at once.
pls.add_debug_context("generic")



# Below is adding a debug mode.
# You can:
# - Use the `write_to_file` parameter to specify a file to write to.
# - Use the `write_to_io` parameter to specify an io object to write to.
# - Use the `separate` parameter to specify if this is a standalone debug mode, meaning, if this mode is active,
#     the previous debug mode will not be active.
pls.add_debug_mode("info")
pls.add_debug_mode("error", separate=True)



# You may modify the debug contexts after they are created.
# Access the debug context by using the `Logger.debug_contexts` dictionary.
pls.get_debug_context("generic").set_can_ever_write(True)
pls.get_debug_context("generic").add_direction(IODirection(False, sys.stdout.fileno(), None))



# Now we can use the debug contexts to log messages.
pls.set_debug_mode("info")



@InfoInjector.add_instruction(line=1, debug_mode="", debug_context="", args_to_logger=( # type:ignore
	f"n = {InfoInjector.VariableReference("n")}" # type:ignore
))
@InfoInjector.add_instruction(line=2, debug_mode="", debug_context="", args_to_logger=( # type:ignore
	"n is less than or equal to 1",
	"\n",
	"because of this we must `return n`"
))
@InfoInjector.inject(globals(), locals()) # type:ignore
def fib(n):
	if n <= 1:
		return n
	else:
		return fib(n-1) + fib(n-2)	


print(fib(10))
