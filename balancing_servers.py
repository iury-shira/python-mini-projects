import random


class Server(object):
	"""This class represents the Server instances.
		In this class id_connection attribute is the dict key.
		In this class load_connection is the dict value.
	"""

	def __init__(self):
		"""Just create a new Server instance, with no initial loads"""
		self.connections_loads = {}

	def __str__(self):
		"""Returns the total load of the Server instance"""
		return "{:.2f}%".format(self.load())

	def add_connection(self, id_connection):
		"""Adds a connection to the Server instance"""
		connection_load = random.random() * 10 + 1
		self.connections_loads[id_connection] = connection_load

	def close_connection(self, id_connection):
		"""Closes a specific connection from the Server instance"""
		del self.connections_loads[id_connection]

	def load(self):
		"""Calculates the total load connection of the Server instance"""
		total = 0
		for load in self.connections_loads.values():
			total += load
		return total


# Testing the Server class
print("-" * 100)
server = Server()
server.add_connection("192.168.1.1")
print(server)
server.close_connection("192.168.1.1")
print(server)
print("-" * 100)


class LoadBalancing(object):
	"""This class represents the Load Balancing Process itself.
		In this class the id_connection attribute is the dict key.
		In this class the server_instance attribute is the dict value.
	"""
	def __init__(self):
		"""Initialize the Load Balancing System with only one server"""
		self.connections_servers = {}
		self.servers = [Server()]

	def add_connection(self, id_connection):
		"""Randomly selects a server and add the connection to it"""
		server_instance = random.choice(self.servers)
		server_instance.add_connection(id_connection)
		self.connections_servers[id_connection] = server_instance
		self.ensure_availability()

	def close_connection(self, id_connection):
		"""Closes the specified connection and its load"""
		for connection in self.connections_servers.keys():
			if connection == id_connection:
				# the server instance where the specified connection are
				server_instance = self.connections_servers[connection]
				server_instance.close_connection(id_connection)
		del self.connections_servers[id_connection]

	def avg_load(self):
		"""Calculates the average load of the servers"""
		avg = 0
		for server_instance in self.servers:
			avg += server_instance.load()
		return avg / (len(self.servers))

	def ensure_availability(self):
		"""If the average load is greater than 50, we'll make available one more server"""
		if self.avg_load() > 50:
			self.servers.append(Server())

	def __str__(self):
		"""Returns the loads of each server"""
		loads = [str(server_instance.load()) for server_instance in self.servers]
		return "The loads of the servers are: [{}]".format(", ".join(loads))


# Testing the LoadBalancing class
test = LoadBalancing()
test.add_connection("fdca:83d2::f20d")
print("Average load: {}".format(test.avg_load()))
test.close_connection("fdca:83d2::f20d")
print("Average load: {}".format(test.avg_load()))
print("-" * 100)

# Testing multiple servers (to force the method "ensure_availability" works)
for i in range(20):
	test.add_connection(str(i))
print("Average load: {}".format(test.avg_load()))
print(test)
print("-" * 100)
