# Minimal Documentation for `infoinject`

`infoinject` is a minimal yet powerful logging utility.

Mainly, what distinguishes it from the various other logging utilities is that it can be used in such a way
to separate a functions code from the logging calls that would otherwise clutter the functions normal code.

This is achieved by using a decorator to inject the logging calls into the function.

---

## Features

> Note: A checkmark means that the feature has been implemented, otherwise it is a work in progress.

- [ ] Minimalistic
- [ ] Easy to use
- [ ] Customizable
- [x] Separation of logging calls from the functions code
- [x] Support for different levels of debug output (Debug Modes)
- [x] Support for different Debug Contexts. A context is a way to group debug output
  - for example, two different parts of a game engine could have different contexts.
- [ ] Support for different output streams (e.g. file, console, etc.)
- [ ] Support for different output formats (e.g. JSON, XML, etc.)

---

## Files

### 1. `color_config.py`

- `ColorConfiguration` class

A color configuration is a way to define the colors used for a different debug context.

for example, set:

- normal color,
- color of the timestamp,
- color of the class that called the debug function,
- color of the function within said class that called the debug function,
- color of the debug message itself.

### 2. `debug_context.py`

imports `ColorConfiguration`.

- `DebugContext` class

A debug context is a way to group debug output.

**SEE ALSO**: `!infoinject-debug_context.md`

---

## Design

Say we have a game engine with two debug contexts,

- rendering, and
- physics

We start by defining the debug modes and the debug contexts.

```python
from infoinject import Logger
from infoinject.extras import TimeFormatter, CallerFormatter

# use below to separate log files based on debug mode instead of debug context.
#Logger.set("io_based_on_mode", True)

Logger.add_debug_mode("info")
Logger.add_debug_mode("detail", extends_from="info")
Logger.add_debug_mode("debug", extends_from="detail")

Logger.add_debug_context("rendering")
Logger.add_debug_context("physics")

# The below will add the time before each log message.

Logger.debug_contexts["physics"].add_format_layer(TimeFormatter)

# The below will add which ever function called the log message.
Logger.debug_contexts["rendering"].add_format_layer(CallerFormatter)
Logger.debug_contexts["physics"].add_format_layer(CallerFormatter)
```

Now we can use the debug contexts to log messages.

```python
class renderer:
	def __init__(self):
		Logger.detail("rendering", "The rendering engine in this engine is pretty simple!")
```

Output:

```text
12:00:00.0000 [renderer.__init__] The rendering engine in this engine is pretty simple!
```

> NOTE: this is an exploration of how the design might be and is not final.

### To decide weather this design is good

We should ask a few questions:

- GQ1: Is it easy to use?
- GQ2: Is it easy to understand?
- GQ3: Is it easy to extend?
- GQ4: Is it easy to maintain?

We should also ask some more specific questions:

- SQ1: Why are we implementing the DebugContext and DebugMode into the Logger class instead of something more like this:

```python
from infoinject import Logger, DebugContext, DebugMode

my_context = DebugContext("my_context")

Logger.add_debug_context(my_context)
```

- SQ2: Should we use a public class variable to store the debug contexts and debug modes like in the following example?

```python
Logger.debug_contexts["rendering"].add_format_layer(TimeFormatter)
```

- SQ3: Or should we do something more like this?

```python
Logger.debug_contexts.rendering.add_format_layer(TimeFormatter)
```

- SQ4: How are we going to handle global options across all the debug contexts? For example, say we want to apply formatting to all debug contexts.

- SQ5: When calling to print, is what we are doing okay? Should we do something more like this?

```python
Logger.o.rendering.info("The rendering engine in this engine is pretty simple!")
```

### Answers

#### Questions that cannot be answered

- GQ1: Is it easy to use?
  - In order to answer this we would actually have to finish it and use it for a few days at least.

- GQ3: Is it easy to extend?
  - In order to answer this we would need to design the rest of the system and see how it fits in. And to be real, we would probably want to use a working version for a while before we could answer this.

- GQ4: Is it easy to maintain?
  - Again, we need to finish all the parts and use it for a while before we can answer this.

#### Questions that can be answered

> checked box means yes, unchecked box means no.

- [x] GQ2: Is it easy to understand?
  - For what has been shown, yes.

- [x] SQ1: Why are we implementing the DebugContext and DebugMode into the Logger class instead of something more like this:
  - This could be a way of abstracting away some of the other parameters of the init method for these classes.
  - For example, we only need to pass in the name of the debug mode and if it extends from another debug mode. Then, later on (as seen in the example above), we can add other information like weather we want to separate log files based on debug mode or debug context.
  - Positive:
    - Abstracts away,
    - Integrates everything in a nice and tidy way.
  - Negative:
    - It means that when importing the Logger class, we are importing the DebugContext and DebugMode classes as well. This uses more memory and maybe even for no reason.
  - In general, python is already a horribly inefficient language, so we really shouldn't care that much about the memory consumption of a few extra classes.

- [x] SQ2: Should we use a public class variable to store the debug contexts and debug modes like in the following example?
  - This is a good way to do it because intellisense will not bother us.

- [ ] SQ3: Or should we do something more like this?
  - This is not that much more readable than the previous example and it will most likely throw intellisense off.

- [ ] SQ4: How are we going to handle global options across all the debug contexts? For example, say we want to apply formatting to all debug contexts.
  - TODO: **WE NEED TO FIND AN ANSWER FOR THIS**

- [x] SQ5: When calling to print, is what we are doing okay? Should we do something more like this?
  - YES. i think that the other way is better. It is more condense which a lot of the time is super important.
  - It can throw off intellisense, but there is ways to hack around that, and, if we do hack it, it will be so worth it.
