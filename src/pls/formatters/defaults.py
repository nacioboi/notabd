from formatters.Formatter import IFormatter
from formatters.FinalFormatter import IFinalFormatter







class DefaultFinalFormatter(IFinalFormatter):



	def raw_handle(self, string:str) -> str:
		return self._strip_postfixes(string)
	





