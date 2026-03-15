import socket
import threading
import json

HOST = '0.0.0.0'
PORT = 5555

game_state = {
    "player1": {"x": 100, "y": 100, "action": None},
    "player2": {"x": 200, "y": 100, "action": None},
    "puzzle_state": {}
}

clients = []
lock = threading.Lock()

def handle_client(conn, addr, player_id):
    print(f"Joueur {player_id} connecté depuis {addr}")
    while True:
        try:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break
            input_data = json.loads(data)
            with lock:
                game_state[f"player{player_id}"].update(input_data)
            state_json = json.dumps(game_state) + "\n"
            with lock:
                for client in clients:
                    try:
                        client.send(state_json.encode('utf-8'))
                    except:
                        pass
        except Exception as e:
            print(f"Erreur joueur {player_id}: {e}")
            break
    conn.close()
    with lock:
        if conn in clients:
            clients.remove(conn)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(2)
    print(f"Serveur démarré sur le port {PORT}...")
    player_id = 1
    while True:          # ← change "while len(clients) < 2" par "while True"
        conn, addr = server.accept()
        with lock:
            clients.append(conn)
        t = threading.Thread(target=handle_client, args=(conn, addr, player_id))
        t.daemon = True
        t.start()
        player_id += 1


if __name__ == "__main__":
    start_server()
