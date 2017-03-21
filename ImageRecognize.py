import subprocess

filename = "cd4c1a39ddb0f480d5695af769567ddf.png"

result = subprocess.check_output("java -jar ImageRecognize.jar " + filename, shell=True).splitlines()[0].decode()
print(result)
