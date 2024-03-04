# A small amount of documentation for `infoinject`

## `InfoInjector` class

The info injector class is the main workhorse of this module.

This module solves a very common problem when using other debugging libraries or helpers.

Take the following code:

```python
import some_debugging_library

def foo(bar):
	x = bar + 1
	return bar / 0

some_debugging_library.debug(foo(5))
```

When you run this code, you'll get a `ZeroDivisionError` and the stack trace will point to the `foo` function.

In order to solve this error, we might insert some debug code in the `foo` function:

```python
import some_debugging_library

def foo(bar):
	x = bar + 1
	some_debugging_library.debug("bar:", bar)
	return x / 0
```

This will give us the value of `bar` when the error occurs.
But it does not give us the value of `x` when the error occurs.

So we modify the code again:

```python
import some_debugging_library

def foo(bar):
	x = bar + 1
	some_debugging_library.debug("bar:", bar)
	return some_debugging_library.debug_and_ret(x / 0)
```

As you can see, the debug code has now ruined the readability of the code.

This is really bad as we still might want all the debug information to stay for some lifetime of the project and still keep
all the codes readability.

This is where `infoinject` comes in.

```python
from infoinject import infoinject

@infoinject.inject_debug_info([
	{
	"line": 2,
	"prefix": "\t",
	"x": "print('x:', x)"
	},
	{
	"replace_line": 3,
	"prefix": "\t",
	"x": "return infoinject.debug_and_ret(x / 0)"
	}
])
def foo(bar):
	x = bar + 1
	return x / 0

```

This will give us the value of `x` when the error occurs and still keep the code readable.

## Debug modes

You may be thinking however, if we get the function decorator part wrong, we might end up with more errors than we started with.

This is fine because we have debug modes.

Currently we have the following default:

- [x] Debug
- [x] Release
- [x] Disabled

Disabled will completely remove all the debug code from runtime - so no side effects.
