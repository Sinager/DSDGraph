import sys
import os
import re

# -*- coding: utf-8 -*-

fileorig = 'DSDPlus.event'
rorig = ''
rdest = ''

dsdfile = open(fileorig, 'r', encoding="UTF-8")
graphile = open('DSDPlus.gexf','w', encoding="UTF-8")

# print .gexf header
graphile.write('<?xml version="1.0" encoding="UTF-8"?>\n')
graphile.write('<gexf xmlns:viz="http://www.gexf.net/1.3/viz" version="1.3" xmlns="http://www.gexf.net/1.3">\n')
graphile.write('<meta lastmodifieddate="2010-03-03+23:44">')
graphile.write('<creator>DSDGraph</creator>\n')
graphile.write('</meta>\n')
graphile.write('<graph defaultedgetype="undirected" idtype="string" type="static">\n')
graphile.write('<attributes class="edge">\n')
graphile.write('<attribute id="0" title="msg_type" type="string">\n')
graphile.write('<default>"unspec"</default>\n')
graphile.write('</attribute>\n</attributes>\n')

node = []
edge = []
comtype = []
tgt = re.compile('(Tgt|TG)=\d{1,7}')
src = re.compile('(Src|RID)=\d{1,7}')

# scan the file
for line in dsdfile:
	print(line, " - ")
	e_date = line[:11:]
	e_time = line[13:22:]
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
			if rorig not in node:
				node.append(rorig)
		
		# add TGT if not already in list
		dest = tgt.search(msgdetails)
		if dest:
			if (msgtype == 'Group call') or (msgtype == 'Enc Group call'):
				rdest = dest.group()[3::]
			else: 
				rdest = dest.group()[4::]
			print(' Destination: ', rdest)
			if rdest not in node:
				node.append(rdest)
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

		if (rorig != '') and (rdest != ''):
			oridx = node.index(rorig)
			deidx = node.index(rdest)
			typeidx = comtype.index(msgtype)
			edge.append([oridx, deidx, weight, typeidx])
		
# dump nodes into file
graphile.write('<nodes count="')
graphile.write(str(len(node)))
graphile.write('">\n')
for x in range(len(node)):
	#print(node[x])
	nodeentry = '<node id="' + str(x) + '.0" label="' + node[x] + '"/>\n'
	graphile.write(nodeentry)
graphile.write('</nodes>\n')

# dump edges into file
graphile.write('<edges count="')
graphile.write(str(len(edge)))
graphile.write('">\n')
for x in range(len(edge)):
	#print(edge[x])
	#edgeentry = '<edge id="' + str(x) + '.0" source="' + str(edge[x][0]) + '.0" target="' + str(edge[x][1]) + '.0" weight="' + str(edge[x][2]) + '.0"/>\n'
	edgeentry = '<edge id="' + str(x) + '.0" source="' + str(edge[x][0]) + '.0" target="' + str(edge[x][1]) + '.0" weight="' + str(edge[x][2]) + '.0">\n' + '<attvalues><attvalue for="0" value="' + comtype[edge[x][3]] + '"/></attvalues></edge>'
	graphile.write(edgeentry)
graphile.write('</edges>\n')


graphile.write('</graph>\n</gexf>')

print 