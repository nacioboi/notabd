import dataclasses

@dataclasses.dataclass
class IODirection:
	do_encode: bool
	file_handle: int|None
	file_path: str|None

	def validate(self):
		if self.file_handle and self.file_path:
			raise ValueError("Cannot have both file handle and file path set.")