# flask server to print hello world using templates

import generate_keys
from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, rooms
from flask_session import Session
import rsa

app = Flask(__name__)

Session(app)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app, cors_allowed_origins="*")

keys = {
}

# static files
app.static_folder = 'static'
app.template_folder = 'templates'

def encrypt_content(file_data, public_key_hex):
    hex_bytes = bytes.fromhex(public_key_hex)
    public_key_byte = hex_bytes.decode('utf-8')
    public_key = rsa.PublicKey.load_pkcs1(public_key_byte)
    file_data = file_data.encode('utf-8')
    encrypted_data = rsa.encrypt(file_data, public_key)
    return encrypted_data.hex()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('new_key_req')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    name = json['name']
    type = json['type']
    new_keys = generate_keys.generate_key()
    keys[request.sid] = {}
    keys[request.sid]['name'] = name
    keys[request.sid]['type'] = type
    keys[request.sid]['public_key'] = new_keys[1]
    join_room(type)
    print(name)
    socketio.emit('new_key_res', {
                  "private_key": new_keys[0], "public_key": new_keys[1], "sid": request.sid}, room=request.sid)
    socketio.emit('new_user_keys', keys)


@socketio.on('software_update')
def handle_software_update(json, methods=['GET', 'POST']):
    for i in json["sid"]:
        encrypt_soft = encrypt_content(json["software"],keys[i]['public_key'])
        socketio.emit('software_update', {"encrypt_soft":encrypt_soft,"tester": keys[request.sid]['name'],"signature":json['signature'],"testersid":request.sid}, to=i)

@socketio.on("connect")
def handle_connect():
    socketio.emit('new_user_keys', keys)


@socketio.on("disconnect")
def handle_disconnect():
    if (request.sid in keys):
        del keys[request.sid]
    socketio.emit('new_user_keys', keys)


@app.route("/disconnect/<sid>")
def handle_disconnect(sid):
    del keys[sid]
    socketio.emit('new_user_keys', keys)
    return "ok"


# run the app
if __name__ == '__main__':
    app.run()
