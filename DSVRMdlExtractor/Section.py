import os
import struct
import io
import sys
from struct import *

class AnmSection:
	def __init__(self,start,length):
		self.start=start;
		self.length=length;

class JntSection:
	def __init__(self):
		self.foobar=1;