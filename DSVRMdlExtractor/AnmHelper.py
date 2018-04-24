import os
import struct
import io
import sys
from struct import *
from Section import *

class AnmHelper:
	@staticmethod
	def HalfFloat(bytes):
		res=[];
		for i in range(len(bytes)//2):
			bins=[];
			tl=bytes[2*i];
			th=bytes[2*i+1];
			while (tl>0):
				bins.append(tl%2);
				tl//=2;
			while (len(bins)<8):bins.append(0);
			while (th>0):
				bins.append(th%2);
				th//=2;
			while (len(bins)<16):bins.append(0);

			xiao=0;
			for i in range(10):
				xiao/=2;
				xiao+=bins[i];
			xiao/=2;
			xiao+=1;

			mi=0;
			for i in range(10,15):
				mi*=2;
				mi+=bins[14-(i-10)];
			mi-=15;

			fu=1;
			if (bins[15]==1):fu=-1;

			newhalf=fu*xiao*pow(2,mi);
		
			res.append(newhalf);
		return res;

	@staticmethod
	def HalfFloatNum(num):
		
		bins=[];
		tl=num&255;
		th=num>>8;
		while (tl>0):
			bins.append(tl%2);
			tl//=2;
		while (len(bins)<8):bins.append(0);
		while (th>0):
			bins.append(th%2);
			th//=2;
		while (len(bins)<16):bins.append(0);

		xiao=0;
		for i in range(10):
			xiao/=2;
			xiao+=bins[i];
		xiao/=2;
		xiao+=1;

		mi=0;
		for i in range(10,15):
			mi*=2;
			mi+=bins[14-(i-10)];
		mi-=15;

		fu=1;
		if (bins[15]==1):fu=-1;

		newhalf=fu*xiao*pow(2,mi);
		return newhalf;

	@staticmethod
	def RatioNum(num):
		#if num&16384>0:
		#	return -(num-16384)/16384;
		return num/16384;

	@staticmethod
	def Read28(bytes):
		foobar=0;
		byth=(bytes[5]*256+bytes[4]);
		bytm=(bytes[3]*256+bytes[2])>>1;
		bytl=((bytes[2]&1)*65536+bytes[1]*256+bytes[0])>>2;
		bytx=bytes[0]&3;
		#return [AnmHelper.HalfFloatNum(byth),AnmHelper.HalfFloatNum(bytm),AnmHelper.HalfFloatNum(bytl),bytx];
		return [AnmHelper.RatioNum(byth),AnmHelper.RatioNum(bytm),AnmHelper.RatioNum(bytl),bytx];

	@staticmethod
	def ReadJoint(filepath,filepath2):
		statinfo = os.stat(filepath);
		filelength=statinfo.st_size;
		file=open(filepath,'rb');
		file.seek(24,0);
		countj=unpack("I",file.read(4))[0];
		addrj=unpack("I",file.read(4))[0];

		file.seek(addrj,0);
		jntsections=[];
		for i in range(countj):
			tmpjnt=JntSection();
			tmpjnt.a_line0=unpack("4I",file.read(16));
			tmpjnt.a_line1=unpack("4f",file.read(16));
			tmpjnt.a_line2=unpack("4f",file.read(16));
			tmpjnt.a_line3=unpack("4f",file.read(16));
			tmpjnt.a_line4=unpack("4f",file.read(16));
			tmpjnt.a_line5=unpack("4f",file.read(16));
			tmpjnt.a_line6=unpack("4f",file.read(16));
			tmpjnt.a_line7=unpack("4f",file.read(16));
			tmpjnt.a_line8=unpack("4f",file.read(16));
			tmpjnt.a_line9=unpack("4f",file.read(16));
			tmpjnt.a_line9_10=unpack("3f",file.read(12));
			tmpjnt.a_line9_11=unpack("I",file.read(4))[0];
			jntsections.append(tmpjnt);
		file.close();

		file=open(filepath2,'rb');
		file.seek(16,0);
		countj=unpack("I",file.read(4))[0];
		addrj=unpack("I",file.read(4))[0];
		addri=unpack("I",file.read(4))[0];
		for i in range(countj):
			file.seek(addrj+i*4,0);
			addrt=unpack("I",file.read(4))[0];
			file.seek(addrt,0);
			t="";
			ch=unpack("B",file.read(1))[0];
			while (ch!=0):
				t+=chr(ch);
				ch=unpack("B",file.read(1))[0];
			file.seek(addri+i*4,0);
			index=unpack("I",file.read(4))[0];
			jntsections[index].possiblename=t;
		file.close();

		return jntsections;

		#xsxscount=0;
		#file=open("F:\\JointList.txt",'w');
		#for jnt in jntsections:
		#	file.write("%d\t%d\t%s\n"%(xsxscount,jnt.a_line9_11,jnt.possiblename));
		#	xsxscount+=1;
		#file.close();

	@staticmethod
	def Go(filepath):
		statinfo = os.stat(filepath);
		filelength=statinfo.st_size;
		file=open(filepath,'rb');
	
		file.seek(4,0);
		totaltime=unpack("I",file.read(4))[0];

		file.seek(16,0);
		addr02=unpack("I",file.read(4))[0];
		addr03=unpack("I",file.read(4))[0];

		#GET SECTIONS
		file.seek(addr03+8,0);
		sectionaddr=[];
		nextsec=unpack("I",file.read(4))[0];
		while(nextsec!=0):
			sectionaddr.append(nextsec+addr03);
			nextsec=unpack("I",file.read(4))[0];
		sectionaddr.append(filelength);
		print(len(sectionaddr)-1);
		print(sectionaddr);

		sections=[];
		for i in range(len(sectionaddr)-1):
			currsec=AnmSection(sectionaddr[i],sectionaddr[i+1]-sectionaddr[i]);
			sections.append(currsec);
			file.seek(sectionaddr[i],0);
			currsec.tp1,currsec.tp2,currsec.datalen,currsec.tp4,currsec.tp5,currsec.tp6=unpack("6H",file.read(12));
			rdataoffset=unpack("I",file.read(4))[0];

			file.seek(sectionaddr[i]+rdataoffset,0);
			print(str(i)+" "+str(currsec.tp1)+" "+str(currsec.tp2)+" "+str(currsec.tp4)+" "+str(currsec.tp5)+" "+str(currsec.tp6)+":"+str(sectionaddr[i+1]-sectionaddr[i]-rdataoffset)+" "+str(currsec.datalen)+" "+str((sectionaddr[i+1]-sectionaddr[i]-rdataoffset)/currsec.datalen));
			currsec.data=[];
			currsec.raw=[];
			currsec.raw2=[];
			currsec.testdata=[];
			for irdata in range(currsec.datalen):
				if (currsec.tp1==29):
					currsec.raw.append(file.read(12));
					currsec.data.append(unpack("3f",currsec.raw[-1]));
				elif (currsec.tp1==31):
					currsec.raw.append(file.read(24));
					currsec.data.append(unpack("6f",currsec.raw[-1]));
				elif (currsec.tp1==30):
					currsec.raw.append(file.read(6));
					#currsec.data.append(unpack("3H",currsec.raw[-1]));
					currsec.data.append(AnmHelper.HalfFloat(unpack("6B",currsec.raw[-1])));
				elif (currsec.tp1==28):
					currsec.raw.append(file.read(6));
					#currsec.data.append(unpack("3H",currsec.raw[-1]));
					currsec.data.append(AnmHelper.Read28(unpack("6B",currsec.raw[-1])));
					currsec.testdata.append(list(map(lambda x:hex(x),unpack("6B",currsec.raw[-1]))));
				else:
					currsec.raw.append(file.read(6));
					currsec.data.append(AnmHelper.Read28(unpack("6B",currsec.raw[-1])));
					#currsec.data.append(unpack("6B",file.read(6)));
					#currsec.data.append([unpack("h",currsec.raw[-1][0:2])[0],unpack("f",currsec.raw[-1][2:6])[0]]);
				
			if (currsec.tp1==28):# or currsec.tp1==28):
				#AnmHelper.tongji(currsec.raw);
				#AnmHelper.tongji28(currsec.data);
				foobar=1;

			foobar=1;

		file.close();

		return [totaltime,sections];

	@staticmethod
	def tongji28(datas):
		tongji28_last=-1;
		tongji28_datalast=None;
		print("===TONGJI28===");
		min_bor=[999999.0,999999.0,999999.0,999999.0];
		max_bor=[-999999.0,-999999.0,-999999.0,-999999.0];
		sum_bor=[0.0,0.0,0.0,0.0];
		sdataset=[None,None,None,None];
		for data in datas:
			for i in range(len(data)):
				if min_bor[i]>data[i]:min_bor[i]=data[i];
				if max_bor[i]<data[i]:max_bor[i]=data[i];
				sum_bor[i]+=data[i];
			#if sdataset[data[3]]==None:
			#	sdataset[data[3]]=data;
			if tongji28_last==-1:
				tongji28_last=data[3];
			if tongji28_last!=data[3]:
				print("Sample:\t%.4f\t%.4f\t%.4f\t%.4f"%(tongji28_datalast[0],tongji28_datalast[1],tongji28_datalast[2],tongji28_datalast[3]));
				print("Sample:\t%.4f\t%.4f\t%.4f\t%.4f"%(data[0],data[1],data[2],data[3]));
				tongji28_last=data[3];

			tongji28_datalast=data;
				
		avg_bor=list(map(lambda x:x/len(datas),sum_bor));
		print("MIN:\t%.4f\t%.4f\t%.4f\t%.4f"%(min_bor[0],min_bor[1],min_bor[2],min_bor[3]));
		print("MAX:\t%.4f\t%.4f\t%.4f\t%.4f"%(max_bor[0],max_bor[1],max_bor[2],max_bor[3]));
		print("AVG:\t%.4f\t%.4f\t%.4f\t%.4f"%(avg_bor[0],avg_bor[1],avg_bor[2],avg_bor[3]));
		print("%d"%len(datas));
		#for sdata in sdataset:
		#	if sdata:
		#		print("Sample:\t%.4f\t%.4f\t%.4f\t%.4f"%(sdata[0],sdata[1],sdata[2],sdata[3]));

	@staticmethod
	def tongji(bins):
		lenbins=len(bins[0]);
		db=[]
		for i in range(lenbins):
			db.append([0]*256);
		for bin in bins:
			binnum=unpack("6B",bin);
			for i in range(len(binnum)):
				db[i][binnum[i]]+=1;
		
		for wei in db:
			count=0;
			heikin=0;
			hindofang=0;
			mst=0;
			fang=0;
			flag_rng=0;
			rng0=-1;
			rng1=-1;
			for i in range(len(wei)):
				heikin+=wei[i]*i;
				count+=wei[i];
				if wei[i]>wei[mst]:
					mst=i;
				if flag_rng==0:
					if wei[i]!=0:
						flag_rng=1;
						rng0=i;
				elif flag_rng==1:
					if wei[i]==0:
						flag_rng=2;
						rng1=i;
			heikin/=count;
			for i in range(len(wei)):
				fang+=wei[i]*(i-heikin)*(i-heikin);
				hindofang+=(wei[i]-count/255)*(wei[i]-count/255);
			fang=pow(fang,0.5);
			hindofang=pow(hindofang,0.5);
			#print(wei);
			print("Count: Avr:%.2f\tFng:%.2f\tHfg:%.2f\tMst:%s"%(heikin,fang,hindofang,format(mst,'02x')));
			print("Count: AVG: %s - %s"%(format(rng0,'02x'),format(rng1,'02x')));
		print("--------");
		foobar=1;
						
