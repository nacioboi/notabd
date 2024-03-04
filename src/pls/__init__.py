"""
info inject is a module allowing you to compile python source code with added debug information.
this means that the interesting parts of the code stay separate from printing and other debug code.
"""







from ._OLD_InfoInjector import _InfoInjector

_OLD_InfoInjector = _InfoInjector()

from Logger import pls


"""

=====================
Pieces of the puzzle.
=====================

Logger 			- The piece that does the logging.

DebugContext 		- Use this along side with the logger to separate different areas of an application.
			- For example, you may have a rendering context and a physics context inside a game engine.

DebugMode 		- Use this to specify different levels of debug information.
			- For example, you may have a "info" mode and a "detail" mode.
			- If the "info" mode is active, any messages that are in the "detail" mode will not be printed.
			- This is because the "detail" mode extends from the "info" mode.
			- If the "detail" mode is active, any messages that are in the "info"
			-   and "detail" mode will be printed.

ColorConfiguration 	- Use this to specify the colors of the debug information.
			- For example, you may want to have the rendering context to be in green
			-   and the physics context to be in red.

InfoInjector 		- The piece that injects the debug information into the source code.
			- Uses the Logger to log the debug information.

formatters/ 		- The pieces that format the debug information.
			- For example, you may want to have the time of the debug information to
			-   be formatted in a specific way.
			- You may also want to have the caller of the debug information to be formatted in a specific way.
			- The formatters may be added onto any specified debug context. Then, when the Logger is used
			-   by said context, the formatters will be used to format the debug information.
formatters/TimeFormatter.py
formatters/CallerFormatter.py



====================================
How the pieces relate to each other.
====================================

> Nodes A that is down from node B means that A depends on, or is used by, B.

	Logger
	/ \
	+  +--------------------+
	| 			|
	Debug Context 		Debug Mode
	/ \
	+  +--------------------+
	| 			|
	Color Configuration	formatters/
 

"""