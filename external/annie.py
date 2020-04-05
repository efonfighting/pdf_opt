import subprocess
p = subprocess.Popen(['annie_0.9.8.exe','asdfasd'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
retval = p.wait()
print(retval)