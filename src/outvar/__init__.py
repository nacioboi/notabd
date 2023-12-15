from typing import Any
from typing import TypeVar, Generic

T = TypeVar("T")

class OutputVar(Generic[T]):
	def __init__(self, value:T) -> None:
		self._value = {"0": value}

	def set(self, value:T) -> None:
		self._value["0"] = value

	def __call__(self, *args: Any, **kwds: Any) -> T:
		if len(args) != 0 or len(kwds) != 0:
			raise TypeError("OutputVar object is not callable with arguments")
		return self._value["0"]
