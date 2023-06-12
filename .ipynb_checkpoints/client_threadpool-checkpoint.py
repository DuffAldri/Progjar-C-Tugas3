import sys
import socket
import logging
import concurrent.futures
import time

#set basic logging
logging.basicConfig(level=logging.INFO)

def send_data():
	try:
		# Create a TCP/IP socket
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# Connect the socket to the port where the server is listening
		server_address = ('172.16.16.101', 45000)
		logging.info(f"connecting to {server_address}")
		sock.connect(server_address)

		# Send data
		message = 'TIME INI ADALAH DATA YANG DIKIRIM\r\n'
		logging.info(f"sending {message}")
		sock.sendall(message.encode())
		# Look for the response
		amount_received = 0
		amount_expected = 5
		while amount_received < amount_expected:
			data = sock.recv(64)
			amount_received += len(data)
			logging.info(f"{data}")

	except Exception as ee:
		logging.info(f"ERROR: {str(ee)}")
		exit(0)
	finally:
		logging.info("closing")
		sock.close()
		

def main():
	count = 0
	max_time = 10
	iteration = 0
	with concurrent.futures.ThreadPoolExecutor() as executor:
		end_time = time.time() + max_time
		container = set()
		while time.time() < end_time:
			try:
				future = executor.submit(send_data)
				container.add(future)
				completed = {x for x in container if x.done()}
				count += len(completed)
				container -= completed
				iteration += 1
			except KeyboardInterrupt:
				break
	logging.info(f"Max request dalam {max_time} detik adalah {count} dalam {iteration} iterasi")

if __name__ == "__main__":
	main()