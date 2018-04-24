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
	def LoadJoint(self,modelfilepath,b2itfilepath):
		self.joints=AnmHelper.ReadJoint(modelfilepath,b2itfilepath);
		print("Loaded %d joint data in this file."%len(self.joints));
	
	def LoadMotion(self,motionpath):
		self.totaltime, self.motions=AnmHelper.Go(motionpath);
		print("Loaded %d motion data in this file."%len(self.motions));

	def SaveMotion(self,filepath):
		file=open(filepath,'wb');

		#Params
		jointcnt=len(self.joints);
		file03pos=28;
		file03len=jointcnt*2+16;
		file02pos=file03pos+file03len;
		timelength=self.totaltime;
		while (file02pos%4!=0):
			file02pos+=1;
		
		#FileHead
		fileFFhead=pack("4c6L",b'\x01',b'\x00',b'\x01',b'\xFF',timelength,1,0,file03pos,file02pos,0);
		file.write(fileFFhead);

		#File03
		file03head=pack("4c3L",b'\x03',b'\x00',b'\x01',b'\xFF',jointcnt,16,file03len);
		file03body=[];
		jc=0;
		for joint in self.joints:
			file03body.append(jc);
			file03body.append(255 if joint.a_line9_11>255 else joint.a_line9_11);
			jc+=1;
		file.write(file03head);
		file.write(bytes(file03body));
		for i in range(file02pos-file03len-file03pos):
			file.write(b'\x00');

		#File02
		file02head=pack("4c",b'\x02',b'\x00',b'\x01',b'\xFF');
		file02offs=[];

		file02offslen=4*len(self.motions)+12;
		file02offs.append(0);
		curroffs=file02offslen;
		for motion in self.motions:
			file02offs.append(curroffs);
			curroffs+=16;
			mul=12 if motion.tp1==29 else (24 if motion.tp1==31 else 6);
			while (curroffs+file02pos)%16!=0:curroffs+=1;
			curroffs+=motion.datalen*mul;
			while (curroffs+file02pos)%16!=0:curroffs+=1;
		file02offs.append(0);

		file.write(file02head);
		for off in file02offs:
			file.write(off.to_bytes(4,byteorder='little'));

		#File02-Data
		for i in range(len(self.motions)):
			print("Write Motion No %d"%(i));
			motion=self.motions[i];
			mul=12 if motion.tp1==29 else (24 if motion.tp1==31 else 6);
			file.write(pack("6H",motion.tp1,motion.tp2,motion.datalen,motion.tp4,motion.tp5,motion.tp6));
			dataoff=16;
			if ((file02pos+file02offs[i+1]+dataoff)%16!=0):
				dataoff+=1;
			file.write(dataoff.to_bytes(4,byteorder='little'));
			for j in range((dataoff-16)):
				file.write(b'\x00');
			timecount=0;
			for singleraw in motion.raw:
				file.write(singleraw);
				timecount+=1;
			for j in range(file02offs[i+2]-file02offs[i+1]-dataoff-mul*motion.datalen):
				file.write(b'\x00');
		endzero=file02offs[-2];
		while (endzero+file02pos)%16!=0:
			file.write(b'\x00');

		file.close();

	def CombineMotion(self,motionpath):
		print();

#USAGE
#aaz=AniAnalyzer();
#aaz.LoadJoint("Model File Path Goes Here(*.mdl)","Joint File Path Goes Here(*.jnt)");
#aaz.LoadMotion("Animation File Path Goes Here(*.anm)")
