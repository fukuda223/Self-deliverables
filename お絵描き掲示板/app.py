import os
import base64
from flask import Flask, render_template, request, jsonify # type: ignore
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
socketio = SocketIO(app)

UPLOAD_FOLDER = 'static/drawings'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 仮のデータベース（本番ではMongoDBやPostgreSQLなどを使用）
drawings = []
threads = []
thread_id_counter = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_thread', methods=['POST'])
def create_thread():
    global thread_id_counter
    title = request.json.get('title')
    new_thread = {
        'id': thread_id_counter,
        'title': title,
        'drawings': []
    }
    threads.append(new_thread)
    thread_id_counter += 1
    return jsonify({'success': True, 'thread': new_thread})

@app.route('/upload_drawing', methods=['POST'])
def upload_drawing():
    data = request.json.get('image_data')
    thread_id = request.json.get('thread_id')
    image_data = data.split(',')[1] # 'data:image/png;base64,' の部分を削除

    filename = f'drawing_{len(drawings)}.png'
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    try:
        with open(filepath, 'wb') as f:
            f.write(base64.b64decode(image_data))

        new_drawing = {
            'id': len(drawings),
            'image_url': f'/{UPLOAD_FOLDER}/{filename}',
            'likes': 0,
            'thread_id': thread_id
        }
        drawings.append(new_drawing)

        # 該当するスレッドに絵を追加
        for thread in threads:
            if thread['id'] == thread_id:
                thread['drawings'].append(new_drawing)
                break

        # 全クライアントに新しい絵を通知
        socketio.emit('new_drawing_posted', new_drawing)
        socketio.emit('update_ranking', get_ranking())

        return jsonify({'success': True, 'drawing': new_drawing})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/like_drawing', methods=['POST'])
def like_drawing():
    drawing_id = request.json.get('drawing_id')
    for drawing in drawings:
        if drawing['id'] == drawing_id:
            drawing['likes'] += 1
            # 全クライアントに更新されたいいね数を通知
            socketio.emit('update_like_count', {'id': drawing_id, 'likes': drawing['likes']})
            socketio.emit('update_ranking', get_ranking())
            return jsonify({'success': True, 'likes': drawing['likes']})
    return jsonify({'success': False, 'message': 'Drawing not found'})

def get_ranking():
    sorted_drawings = sorted(drawings, key=lambda x: x['likes'], reverse=True)
    return sorted_drawings[:5] # トップ5を返す

@socketio.on('connect')
def on_connect():
    print('Client connected')
    emit('initial_data', {'threads': threads, 'drawings': drawings, 'ranking': get_ranking()})

if __name__ == '__main__':
    socketio.run(app, debug=True)