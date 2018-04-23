import os
import struct
import io
import sys
from struct import *
from Section import *
from AnmHelper import *

for i in range(48,80):
	for j in range(0,256):
		b=bytes([i,j,0,0][::-1]);
		t1=unpack("1f",b)[0];
		b=bytes([i,j][::-1]);
		t2=AnmHelper.HalfFloat(b)[0];
		b=bytes([i,j,0,0,0,0,0,0][::-1]);
		t3=unpack("1d",b)[0];
		print("%s,%s:\t%.5f\t%.5f\t%.5f"%(format(i,"02x"),format(j,"02x"),t1,t2,t3));


	foobar=1;