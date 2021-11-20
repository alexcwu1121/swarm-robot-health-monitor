"""
Interface.py
Main file for our Graphical User Interface.
"""

import gui
import json
from tkinter import * 
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog
from ttkthemes import ThemedTk


class Interface():
	def __init__(self):
		"""
		Attributes:
			- root: tkinter root instance
				the root for the gui elements
			- lom: dict<String:String>
				holds data from configuration file
			- loaded_file: Dict<String:String>
				loaded data directly from config json
			- started: Boolean
				indicates whether GUI has started or not
            - data: dict<String:String>
                The data that is being used
            - reloded_required: Boolean
                Indicated if a relode is needed
		"""
		self.root = self.intialization()
		self.lom = {}
		self.loaded_file = ""
		self.data = {}
		self.reloadd_required = False
		self.started = False
		self.root.update()

	def refresh_gui(self):
		"""Update the gui with changes"""
		self.root.update()        

	def make_cpane(self, name, data, graph):
		"""
		return collapsiblepane object representing a machine
		Arguments: 
			name: String
				name of the machine
			data: Dict<String:String>
				The data the infodisplay object should contain
            graph: Dict<String:String>
                The parameters for graphs
		"""
		cpane = gui.cp(self.root, name, name)
		cpane.grid(row = 0, column = 0, sticky = 'w')
		status = gui.light(self.root)
		status.grid(row = 0, column = 1, sticky = 'w')
		info = gui.infd(cpane.frame, data, graph, self)
		info.grid(row = 1, column = 0)
		return cpane, info, graph, status

	def load_file(self):
		"""Load a new config file and update GUI"""
		old_loaded = self.loaded_file
		filename = filedialog.askopenfilename(initialdir='./config',
												title = 'Select a swarm config',
												filetypes=[("Json", '*.json')])
		try:
			self.loaded_file = filename
			with open(filename) as f:
				self.data = json.load(f)
		except:
			self.loaded_file = old_loaded
			messagebox.showinfo("Config Error", "config json not in correct format!")
			return

		self.reload()

	def save_file(self):
		"""saves the current self.dict to a json config"""
		old_loaded = self.loaded_file
		file = filedialog.asksaveasfile(initialdir='./config',
												title = 'Save swarm config',
												filetypes=[("Json", '*.json')])
		try:
			json.dump(self.data, file,  indent=4)
			self.loaded_file = file.name
		except:
			messagebox.showinfo("Config Error", "failed to save config file!")
			return

	def add_robot(self):
		"""prompts the user to enter infromation to create a new machine in self.dict"""
		name = simpledialog.askstring(title="Name", prompt="Enter machine name:")
		ip = simpledialog.askstring(title="IP", prompt="Enter machine IP:")
		port = simpledialog.askstring(title="Port", prompt="Enter machine Port:")
		if name != None and ip != None and port != None:
			self.data['mlist'].append({ 'ip': ip, 
										'port': port, 
										'name': name,             
										'update_interval': '0.1',
										'agg_interval': '0.1',
										'data': {}})
			self.reload()

	def rmv_robot(self):
		"""prompts user name a machine to remove"""
		name = simpledialog.askstring(title="Name", prompt="Enter machine name to remove:")
		if name != None:
			for item in self.data['mlist']:
				if item['name'] == name:
					self.data['mlist'].remove(item)
			self.reload()

	def add_value(self, ip):
		"""
        Prompts user to add a value to a machine at ip
        Arguments: 
            ip: String
                The ip of the machine to add a value too
        """
		name = simpledialog.askstring(title="Name", prompt="Enter the name of the data stream:")
		unit = simpledialog.askstring(title="Units", prompt="Enter units it is measured in:")
		if name != None and unit != None:
			for item in self.data['mlist']:
				if item['ip'] == ip:
					item['data'][name] = unit
			self.reload()

	def rmv_value(self, ip):
		"""
        Prompts user to remove a value on machine at ip
        Arguments: 
            ip: String
                The ip of the machine to remove a value from
        """
		name = simpledialog.askstring(title="Name", prompt="Enter the name of the data stream to remove:")
		if name != None:
			for item in self.data['mlist']:
				if item['ip'] == ip:
					if name in item['data'].keys():
						del item['data'][name]
			self.reload()

	def reload(self):
		"""reloads based off of current self.dict"""
		for v in self.lom.values():
			v["cpane"].destroy()
			v["info"].destroy()
			v["status"].destroy()
		self.lom.clear()

		big_dict = self.data["mlist"]
		for i in range(0, len(big_dict)):
			ip = big_dict[i]["ip"]
			cpane, info, graph, status = self.make_cpane(big_dict[i]["name"], big_dict[i], big_dict[i].get("graph", {}))
			self.lom[ip] = {"name":big_dict[i]["name"], "cpane":cpane, "info":info, "graph":graph, "status":status, "ip":ip}
			self.lom[ip]["cpane"].grid(row=i, column=0, sticky='nsew')
			self.lom[ip]["status"].grid(row=i, column=1, sticky='nsew')
		self.reloadd_required = True


	def get_reload(self):
		"""returns true if reload has been performed"""
		return self.reloadd_required

	def inform_reload(self):
		"""Display aknoledging that it has reloadd"""
		self.reloadd_required = False

	def get_config(self):
		"""return the currently loaded config file"""
		return self.data

	def update_display(self, updates):
		"""
		Update the gui with updates
		Arguments: 
			- updates: dict<String:String>
				dictionary of updates for the GUI
		"""
		ip = list(updates.keys())[0]
		content = updates[ip]
		try:
			info = self.lom[ip]["info"].get_data()
		except KeyError:
			return
		for k in info:
			try:
				self.lom[ip]["info"].set_data(k, content[k])
			except KeyError:
				pass
		status = "disconnect"
		try:
			status = updates[ip]['Status']
		except KeyError:
			pass
		try:
			self.lom[ip]["status"].set_status(status)
		except KeyError:
			pass
		self.root.update()

	def change_name(self, ip, newname):
		"""
		change the name of a machine
		Arguments: 
			- ip: String
				The ip of the machine
			- newname: String
				The name to change the machine to
		"""
		self.lom[ip]["name"] = newname
		self.lom[ip]["cpane"].setName(newname)
		self.root.update()


	def intialization(self):
		"""create the root and options of the GUI"""
		root = ThemedTk(theme="equilux")
		root.geometry('1000x1000')
		root.configure(bg='#464646')
		root.title("SRHMD")
		Grid.columnconfigure(root, 0, weight=1)
		menubar = Menu(root)
		filemenu = Menu(menubar, tearoff=0)
		filemenu.add_command(label="Load", command=lambda: self.load_file())
		filemenu.add_command(label="Save", command=lambda: self.save_file())
		filemenu.add_command(label="Add Robot", command=lambda: self.add_robot())
		filemenu.add_command(label="Remove Robot", command=lambda: self.rmv_robot())
		menubar.add_cascade(label="File", menu=filemenu)
		filemenu.add_separator()
		root.config(menu=menubar)
		return root