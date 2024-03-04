# Into more detail: `debug_context.py`

---

## 2.1 `DebugContext` elements

### > `def _always(self)`

This function is called on basically every other function below.

It basically just makes sure the current debug context, stored in a global variable, is set whenever a function is called.

### > `def set_color_on(self)`

.

### > `def set_color_off(self)`

.

### > `def set_class_name(self, class_name)`

The class name is a bit more difficult to automatically get, so, for now, it has to be set manually.

### > `def __get_caller_function(self, position) -> str`

Used by the `def set_caller_function(self)` function to get the name of the function that called the debug function.

This is done using the `inspect` module.

### > `def _get_colored_time(self) -> str`

.

### > `def _get_colored_class_name(self) -> str`

.

### > `def _get_colored_caller_function(self) -> str`

Returns a formatted string that contains the caller name which is fetched using the inspect module.

### > `def get_time(self) -> str`

.

### > `def get_class_name(self) -> str`

.

### > `def get_caller_function(self) -> str`

.

### > `def log_line(self, *args, **kwargs)`

This function is used to log a line of debug output.

You can pass the message in a coma separated list (*args).

Supported kwargs are:

- `end` (default: '\n')

### > `def get_reset_poison(self) -> str`

returns "\033[1m~\033[0m" which can be used to negate automated coloring.

### > `def __sequence_occurs_after(self, sequence, string, index) -> bool`

You pass in:

- a sequence of characters, lets say this is x,
- a string, lets say this is s,
- and an index, lets say this is i.

The function will return if x is found in s after i index of s.

else false.

### > `def simple_log_line(self, *args, **kwargs)`
