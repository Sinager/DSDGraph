import sys
import os
import re

# -*- coding: utf-8 -*-

fileorig = 'DSDPlus.event'
rorig = ''
rdest = ''
talkgroup = 0

dsdfile = open(fileorig, 'r', encoding="UTF-8", errors='ignore')
graphile = open('DSDPlus.gexf','w', encoding="UTF-8")

node = []
edge = []
comtype = []
tgt = re.compile('(Tgt|TG)=\w{1,7}')
src = re.compile('(Src|RID)=\w{1,7}')
alg = re.compile('Alg=\w{2,6}')

# scan the file
for line in dsdfile:
	e_date = line[:10:]
	e_date = e_date.replace("/","-",)
	e_time = line[12:20:]
	what = line[22::]
	events = what.split(';')
	if events[0] != what:
		msgtype = events[0]
		if msgtype not in comtype:
			comtype.append(msgtype)
		print(msgtype, ' ', end='')
		msgdetails = events[1][1::]
		
		# add SRC if not already in list
		orig = src.search(msgdetails)
		if orig:
			rorig = orig.group()[4::]	
			print('Origin: ', rorig, end='')
			if [rorig,0] not in node:
				node.append([rorig,0])
		
		# add TGT if not already in list
		dest = tgt.search(msgdetails)
		if dest:
			if (msgtype == 'Group call') or (msgtype == 'Enc Group call'):
				rdest = dest.group()[3::]
				talkgroup = 1
			else: 
				rdest = dest.group()[4::]
				talkgroup = 0
			print(' Destination: ', rdest, end='')
			if [rdest,talkgroup] not in node:
				node.append([rdest,talkgroup])
				print('  - appending: ', rdest, '-', talkgroup, '\n')
			else:
				print('\n')
		# store edge in list
		weight = 1
		if msgtype == 'LRRP':
			weight = 2
		elif msgtype == 'LRRP Control':
			weight = 2
		elif msgtype == 'LRRP Control ACK':
			weight = 2
		elif msgtype == 'Group call':
			weight = 8
		elif msgtype == 'Enc Group call':
			weight = 8
		
		encryption = alg.search(msgdetails)
		if (encryption == None):
			encr = 'clear'
		else:
			encr = encryption.group(0)[4::]
	
		
		print('Encryption: ', encr)

			
		tstamp = e_date + 'T' + e_time
		if (rorig != '') and (rdest != ''):
			oridx = node.index([rorig,0])
			deidx = node.index([rdest,talkgroup])
			typeidx = comtype.index(msgtype)
			edge.append([oridx, deidx, weight, typeidx, tstamp, encr])

# print .gexf header
graphile.write('<?xml version="1.0" encoding="UTF-8"?>\n')
graphile.write('<gexf xmlns:viz="http://www.gexf.net/1.3/viz" version="1.3" xmlns="http://www.gexf.net/1.3">\n')
graphile.write('<meta lastmodifieddate="2021-02-11+16:00">')
graphile.write('<creator>DSDGraph</creator>\n')
graphile.write('</meta>\n')
graphile.write('<graph defaultedgetype="directed" idtype="string" mode="dynamic" timeformat="datetime" start="')
graphile.write(str(edge[0][4]))
graphile.write('" end="')
graphile.write(str(edge[-1][4]))
graphile.write('">\n')
graphile.write('<attributes class="node">\n')
graphile.write('     <attribute id="0" title="talkgroup" type="boolean">\n')
graphile.write('<default>0</default>\n</attribute>\n')
graphile.write('</attributes>\n')
graphile.write('<attributes class="edge">\n')
graphile.write('     <attribute id="0" title="msg_type" type="string">\n')
graphile.write('<default>"unspec"</default>\n</attribute>\n')
graphile.write('     <attribute id="1" title="encryption" type="string">\n')
graphile.write('<default>"clear"</default>\n</attribute>\n')
graphile.write('</attributes>\n')
			
# dump nodes into file
graphile.write('<nodes count="')
graphile.write(str(len(node)))
graphile.write('">\n')
for x in range(len(node)):
	print(x, ' - ', node[x], ' > ')
	nodeentry = '<node id="' + str(x) + '.0" label="' + str(node[x][0]) + '">\n   <attvalues><attvalue for="0" value="' +str(node[x][1]) + '"/></attvalues>\n</node>\n'
	graphile.write(nodeentry)
graphile.write('</nodes>\n')

# dump edges into file
graphile.write('<edges count="')
graphile.write(str(len(edge)))
graphile.write('">\n')
for x in range(len(edge)):
	#print(edge[x])
	edgeentry = '<edge id="' + str(x) + '.0" source="' + str(edge[x][0]) + '.0" target="' + str(edge[x][1]) + '.0" weight="' + str(edge[x][2]) + '.0" start="'+ str(edge[x][4]) + '" end="' + str(edge[x][4]) + '">\n' + '<attvalues>\n   <attvalue for="0" value="' + comtype[edge[x][3]] + '"/>\n   <attvalue for="1" value="' + str(edge[x][5]) + '"/>\n</attvalues></edge>\n'
	graphile.write(edgeentry)
graphile.write('</edges>\n')


graphile.write('</graph>\n</gexf>')

