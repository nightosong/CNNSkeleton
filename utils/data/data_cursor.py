import os
import random
import threading
from utils import path_utils 


class DataCursor:
	def top(self): pass
	
	def down(self, span=1): pass
	
	def up(self, span=1): pass
	
	def point(self, spec_dir): pass
	
	def __iter__(self): pass
	
	def __next__(self): pass
	
	def reset_iter(self): pass
	
	def next(self):
		return self.__next__()
		

class FsCursor(DataCursor):
	def __init__(self, root_dir):
		self.__local = threading.local()
		self.root_dir = root_dir
		self.cache = {}
		self.__reset_pointer()
		self._iterator = None
		self.reset_iter()
		
	def __check_local(self):
		if not hasattr(self.__local, 'has_inited'):
			self.__local.has_inited = True
			self.__reset_pointer()
			
	def __reset_pointer(self):
		self.__local.current_file = self.root_dir
		self.__local.current_parent = None
		return self.__local.current_file
		
	def top(self):
		return self.__reset_pointer()
		
	def down(self, span=1):
		self.__check_local()
		result = None
		for _ in range(span):
			result = self.__down()
		return result
		
	def up(self, span=1):
		self.__check_local()
		result = None
		for _ in range(span):
			result = self.__up()
		return result	
	
	def point(self, spec_dir):
		self.__check_local()
		self.__local.current_file = spec_dir
		self.__local.current_parent = path_utils.parent_dir_path(self.__local.current_file)
		return self.floating()
	
	def floating(self):
		self.__check_local()
		if self.__local.current_parent is not None:
			sub_file_list = self.__get_sub_file_list(self.__local.current_parent)
			self.__local.current_file = random.choice(sub_file_list)
			reutrn self.__local.current_file
	
	def __down(self):
		sub_file_list = self.__get_sub_file_list(self.__local.current_file)
		sub_file = random.choice(sub_file_list)
		self.__local.current_parent = self.__local.current_file
		self.__local.current_file = sub_file
		return self.__local.current_file
	
	def __up(self):
		self.__local.current_file = path.utils.parent_dir_path(self.__local.current_file)
		if self.__local.current_file == self.root_dir:
			self.__local.current_parent = None
		else:
			self.__local.current_parent = path_utils.parent_dir_path(self.__local.current_file)
		return self.floating()
	
	def __get_sub_file_list(self, current_dir):
		sub_file_list = self.cache.get(current_dir)
		if sub_file_list is None:
			file_list = os.listdir(current_dir)
			sub_file_list = [os.path.join(current_dir, filename) for filename in file_list]
			self.cache[current_dir] = sub_file_list
		return sub_file_list
		
	def __iter__(self):
		return self._iterator
		
	def __next__(self):
		return self._iterator.__next__()
		
	def _create_iter(self):
		for root, _, files in os.walk(self.root_dir):
			for f in files:
				path = os.path.join(root, f)
				yield path
		
	def reset_iter(self):
		self._iterator = self._create_iter()
