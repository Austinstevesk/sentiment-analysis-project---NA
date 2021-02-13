import subprocess

subprocess.run("python stream_listener.py & python app.py", shell=True)