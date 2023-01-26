import os
from flask import Flask, render_template
app = Flask(__name__)

#Persistent storage use
# Get the path of the PV from an environment variable
# set DATA_PATH env var as path to which pvc is mounted
data_path = os.environ.get('DATA_PATH', '/app/appdata')

# Use the data_path to read and write data
with open(f'{data_path}/mydata.txt', 'w') as f:
    f.write('Hello, World!')

with open(f'{data_path}/mydata.txt', 'r') as f:
    print(f.read())


@app.route("/")
def hello():
    return render_template('index.html', message="Superman")

if __name__ == "__main__":
    app.run(port=8000)

