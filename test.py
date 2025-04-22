import subprocess
import shlex

cmd = "pip install -r re.txt"
result = subprocess.run(shlex.split(cmd), capture_output=True, text=True, shell=True)
print(result.stdout)
