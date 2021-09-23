import psutil
import platform


#print information about operating system
uname = platform.uname()
print("os info:")
print("os name: " + uname.system)
print("os release: " + uname.release)
print("os version: " + uname.version)
print("processor name: " + uname.processor)

#get cpu information
print("cpu info:")
print("physical cores: " + str(psutil.cpu_count(logical=False)))
print("logical cores: " + str(psutil.cpu_count(logical=True)))
#get core speed
cpufreq = psutil.cpu_freq()
print("max frequency: " + str(cpufreq.max))
print("min frequency: " + str(cpufreq.min))
print("current frequency: " + str(cpufreq.current))

#cpu usage
print("cpu usage per core:")
for count, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
	print("Core " + str(count) + ": " + str(percentage))
print("Total cpu usage: " + str(psutil.cpu_percent()))

#memory usage
svmem = psutil.virtual_memory()
print("memory info:")
print("Total: " + str(svmem.total/8) + " bytes")
print("Aviable: " + str(svmem.available/8) + "bytes")
print("Used: " + str(svmem.used/8) + "bytes")
print("Percentage: " + str(svmem.percent) + "%")

