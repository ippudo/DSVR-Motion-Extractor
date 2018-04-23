import os
import struct
import io
import sys
from struct import *
from Section import *
from AnmHelper import *


class AniAnalyzer:
	def __init__(self):
		foobar=1;

	def LoadJoint(self,modelfilepath,b2itfilepath):
		joints=AnmHelper.ReadJoint(modelfilepath,b2itfilepath);
		print("Loaded %d joint data in this file."%len(joints));
	
	def LoadMotion(self,motionpath):
		motions=AnmHelper.Go(motionpath);
		print("Loaded %d motion data in this file."%len(motions));
	#UNAF-LUKA take care of 42

	def SaveMotion(self,motionpath):
		file=open(filepath,'wb');

		#key = b'\xFF\x7F\xFF\xFE\xFF\x3F';
		
		#FileHead
		timelength=9999;
		file03pos=28;
		file02pos=9999;
		fileFFhead=pack("4BLLLLLL",b'\x01\x00\x01\xFF',timelength,1,0,file03pos,file02pos,0);
		file.write(fileFFhead);

		#File03
		file03len=9999;
		jointcnt=9999;
		file03head=pack("4BLLL",b'\x03\x00\x01\xFF',jointcnt,16,file03len);
		file03body=0;
		file.write(file03head);
		#file.write(file03body);

		#File02
		file02head=pack("4B",b'\x02\x00\x01\xFF');
		file02offs=0;
		file02body=0;
		file.write(file02head);
		#file.write(file02offs);
		#file.write(file02body);

		file.close();

	def CombineMotion(self,motionpath):
		print();

#USAGE
#aaz=AniAnalyzer();
#aaz.LoadJoint("Model File Path Goes Here(*.mdl)","Joint File Path Goes Here(*.jnt)");
#aaz.LoadMotion("Animation File Path Goes Here(*.anm)")