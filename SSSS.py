from bluetooth import *
import json

server_sock=BluetoothSocket(RFCOMM)
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port=server_sock.getsockname()[1]

uuid="Your UUID goes here. Google bluetooth uuid generator"
name="Your Clever Scouting Server Name Goes here (not super important). Remember to pair the devices being used with this server beforehand."

advertise_service(server_sock, name,
	service_id = uuid,
	service_classes = [ uuid, SERIAL_PORT_CLASS ],
	profiles = [ SERIAL_PORT_PROFILE ]
)

def doClient():
	print("Waiting for connection on RFCOMM channel %d" % port)

	client_sock, client_info = server_sock.accept()
	print("Accepted connection from "+client_info[0])


	try:
		data = client_sock.recv(1024)
		print("Data recieved.")
		print(data)
		matchDataFile=open("/var/www/html/matchData.json","a")
		dataJSON = json.loads(data.rstrip())
		matchDataString=","+json.dumps(dataJSON["matchData"])[1:-1]
		if len(matchDataString)>1:
			matchDataFile.write(matchDataString)
		matchDataFile.close()
		teamDataFile = open("/var/www/html/teamData.json","a")
		teamDataString=","+json.dumps(dataJSON["teamData"])[1:-1]
		if len(teamDataString)>1:
			teamDataFile.write(teamDataString)
		teamDataFile.close()
		teamDataFile = open("/var/www/html/teamData.json","r")
		
		client_sock.send("["+teamDataFile.read()+"]\n")
		teamDataFile.close()
		print("Data sent.")
	except IOError:
		print("An IOError occurred")
		pass

	print("Disconnected.\n")

	client_sock.close()

try:
	while True:
		doClient()
except KeyboardInterrupt:
	server_sock.close()
	print("\nAll done.")
except:
	server_sock.close()
	print("An error occurred.")
	raise
print("End of Program")
