from Logger import pls
#from formatters import TimeFormatter, CallerFormatter
#from ColorConfiguration import ColorConfiguration
from DebugMode import DebugMode
from Direction import IODirection

import sys

# use below to separate log files based on debug mode instead of debug context.
#pls.set("io_based_on_mode", True)



# The below sets the global context to generic.
pls.set("global_context", "generic")



# Below is adding a debug context.
# It is a bit more complicated than setting up debug contexts so you dont have to set all the parameters at once.
pls.add_debug_context("generic")
pls.add_debug_context("rendering")
pls.add_debug_context("physics")



# Below is adding a debug mode.
# You can:
# - Use the `write_to_file` parameter to specify a file to write to.
# - Use the `write_to_io` parameter to specify an io object to write to.
# - Use the `separate` parameter to specify if this is a standalone debug mode, meaning, if this mode is active,
#     the previous debug mode will not be active.
pls.add_debug_mode("info")
pls.add_debug_mode("detail")
pls.add_debug_mode("debug")
pls.add_debug_mode("error", separate=True)



# START OF MODIFYING DEBUG CONTEXTS #

# You may modify the debug contexts after they are created.
# Access the debug context by using the `Logger.debug_contexts` dictionary.

pls.get_debug_context("generic").set_can_ever_write(True)
pls.get_debug_context("generic").add_direction(IODirection(False, sys.stdout.fileno(), None))
pls.get_debug_context("rendering").set_can_ever_write(True)
pls.get_debug_context("rendering").add_direction(IODirection(False, sys.stdout.fileno(), None))
pls.get_debug_context("physics").set_can_ever_write(True)
pls.get_debug_context("physics").add_direction(IODirection(False, sys.stdout.fileno(), None))
					       
# The below will add the time before each log message.
#pls.get_debug_context("generic").add_format_layer(TimeFormatter)
#pls.get_debug_context("rendering").add_format_layer(TimeFormatter)
#pls.get_debug_context("physics").add_format_layer(TimeFormatter)
#
## The below will add which ever function called the log message.
#pls.get_debug_context("generic").add_format_layer(CallerFormatter)
#pls.get_debug_context("rendering").add_format_layer(CallerFormatter)
#pls.get_debug_context("physics").add_format_layer(CallerFormatter)
#
## You may specify color configurations for the debug contexts.
#pls.get_debug_context("generic").set_color_configuration(ColorConfiguration._default())

# END OF MODIFYING DEBUG CONTEXTS #



# Now we can use the debug contexts to log messages.
pls.set_debug_mode("info")

pls().info("This is using the generic context.")
pls().info("It works since we set a global context.")



class renderer:
	def __init__(self):
		pls().rendering.detail("The rendering engine in this engine is pretty simple!")



class physics:
	def __init__(self):
		pls().physics.detail("The physics engine in this engine is pretty simple!")


#my_renderer = renderer()
my_physics = physics()

pls.set_debug_mode("detail")

my_physics = physics()







from infoinject import InfoInjector

@InfoInjector.add_instruction(line=1, debug_mode="info", debug_context="generic", args_for_logger=(
	f"n = {InfoInjector.VariableReference('n')}",
))
@InfoInjector.add_instruction(line=2, debug_mode="detail", debug_context="generic", args_for_logger=(
	f"n is", "less than or equal to 1"
),
	end="\n.\n"
)
@InfoInjector.add_instruction(line=4, debug_mode="info", debug_context="generic", args_for_logger=(
	f"n is greater than 1",
	f"Now actually calculating... n-1 and n-2"
))
@InfoInjector.inject(globals(), locals())
def fib(n):
	if n <= 1:
		return n
	else:
		return fib(n-1) + fib(n-2)

fib(5)