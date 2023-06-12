import sys
import socket
import logging
import multiprocessing
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
	start_time = time.time()
	end_time = start_time + max_time
	with multiprocessing.Pool() as pool:
		while time.time() < end_time:
			try:
				result = pool.apply_async(send_data)
				process_count = multiprocessing.active_children()
				count += 1
			except KeyboardInterrupt:
				break
	logging.info(f"Max process dalam {max_time} detik adalah {count}")
			
if __name__ == "__main__":
	main()