import subprocess

def install(name):
    subprocess.call(['pip', 'install', name])
	
f = open("requirements.txt", "r")

for i in f:
    print(i)
    install(i)