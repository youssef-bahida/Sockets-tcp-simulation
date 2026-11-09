import socket
import socketserver
import threading
import streamlit as st


# ==========================================
# CONFIGURATION
# ==========================================

HOST = "127.0.0.1"
PORT = 5001


# ==========================================
# TCP SERVER MANAGER
# ==========================================

class TCPServerManager:

    def __init__(self):
        self.server = None
        self.thread = None
        self.lock = threading.Lock()
        self.active_sockets = set()

    @property
    def running(self):
        return self.thread is not None and self.thread.is_alive()

    def start(self):

        with self.lock:

            if self.running:
                return False

            manager = self

            class ClientHandler(socketserver.StreamRequestHandler):

                def handle(self):

                    manager.register(self.request)

                    try:
                        for line in self.rfile:

                            message = line.decode(
                                "utf-8", errors="replace"
                            ).strip()

                            if not message:
                                continue

                            try:
                                number = float(message)
                                result = number * 2

                                response = f"RESULT:{result:g}\n"

                            except ValueError:

                                response = (
                                    "ERROR:Please send a valid number.\n"
                                )

                            self.wfile.write(response.encode("utf-8"))
                            self.wfile.flush()

                    except (ConnectionError, OSError):
                        pass

                    finally:
                        manager.unregister(self.request)

            class TCPServer(socketserver.ThreadingTCPServer):
                allow_reuse_address = True
                daemon_threads = True

            try:

                self.server = TCPServer(
                    (HOST, PORT),
                    ClientHandler
                )

                self.thread = threading.Thread(
                    target=self.server.serve_forever,
                    daemon=True
                )

                self.thread.start()

                return True

            except OSError:
                self.server = None
                self.thread = None
                raise

    def register(self, client_socket):

        with self.lock:
            self.active_sockets.add(client_socket)

    def unregister(self, client_socket):

        with self.lock:
            self.active_sockets.discard(client_socket)

    def stop(self):

        with self.lock:

            if self.server is None:
                return

            server = self.server
            self.server = None

            sockets = list(self.active_sockets)
            self.active_sockets.clear()

            self.thread = None

        server.shutdown()
        server.server_close()

        for client_socket in sockets:
            try:
                client_socket.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass

            try:
                client_socket.close()
            except OSError:
                pass


# One shared server for the Streamlit process
@st.cache_resource
def get_server():

    return TCPServerManager()


server = get_server()


# ==========================================
# CLIENT FUNCTIONS
# ==========================================

def create_client():

    client_id = st.session_state.next_client_id

    st.session_state.clients[client_id] = {
        "socket": None,
        "connected": False,
        "last_sent": None,
        "response": "No response yet"
    }

    st.session_state.next_client_id += 1


def connect_client(client_id):

    client = st.session_state.clients[client_id]

    if not server.running:

        client["response"] = "Server is not running."
        return

    try:

        sock = socket.create_connection(
            (HOST, PORT),
            timeout=3
        )

        sock.settimeout(3)

        client["socket"] = sock
        client["connected"] = True
        client["response"] = "Connected successfully."

    except OSError as error:

        client["connected"] = False
        client["response"] = f"Connection failed: {error}"


def disconnect_client(client_id):

    client = st.session_state.clients[client_id]

    sock = client["socket"]

    if sock:

        try:
            sock.close()
        except OSError:
            pass

    client["socket"] = None
    client["connected"] = False
    client["response"] = "Disconnected."


def send_message(client_id, number):

    client = st.session_state.clients[client_id]

    sock = client["socket"]

    if not client["connected"] or sock is None:

        client["response"] = "Connect this client first."
        return

    try:

        sock.sendall(f"{number}\n".encode("utf-8"))

        response = sock.recv(1024).decode(
            "utf-8", errors="replace"
        ).strip()

        client["last_sent"] = number
        client["response"] = response

    except (OSError, TimeoutError) as error:

        disconnect_client(client_id)
        client["response"] = f"Communication error: {error}"


def remove_client(client_id):

    disconnect_client(client_id)

    del st.session_state.clients[client_id]


def stop_server():

    server.stop()

    # Disconnect clients belonging to this browser session
    for client_id in list(st.session_state.clients):

        disconnect_client(client_id)


# ==========================================
# SESSION INITIALIZATION
# ==========================================

if "clients" not in st.session_state:

    st.session_state.clients = {}

if "next_client_id" not in st.session_state:

    st.session_state.next_client_id = 1


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="TCP Communication",
    page_icon="🌐",
    layout="wide"
)


# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.main {
    background-color: #0b1120;
}

.block-container {
    padding-top: 2rem;
    max-width: 1400px;
}

h1, h2, h3 {
    color: #f1f5f9;
}

.client-card {
    background: #172033;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #29364d;
    margin-bottom: 10px;
}

.status-online {
    color: #22c55e;
    font-weight: bold;
}

.status-offline {
    color: #f87171;
    font-weight: bold;
}

div.stButton > button {
    border-radius: 9px;
    font-weight: 600;
    min-height: 40px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# HEADER
# ==========================================

st.title("🌐 TCP Communication System")

st.caption(
    "Java-style TCP client/server communication — "
    "implemented in Python."
)

st.divider()


# ==========================================
# SERVER CONTROL
# ==========================================

st.subheader("🖥️ TCP Server")

server_col1, server_col2, server_col3 = st.columns(
    [1, 1, 2]
)

with server_col1:

    if st.button(
        "▶ Start Server",
        use_container_width=True,
        type="primary",
        disabled=server.running
    ):

        try:

            server.start()
            st.success("TCP server started!")

        except OSError as error:

            st.error(f"Cannot start server: {error}")

with server_col2:

    if st.button(
        "■ Stop Server",
        use_container_width=True,
        disabled=not server.running
    ):

        stop_server()
        st.warning("TCP server stopped.")

with server_col3:

    if server.running:

        st.success(f"🟢 Server ONLINE — Port {PORT}")

    else:

        st.error("🔴 Server OFFLINE")


st.divider()


# ==========================================
# CLIENT MANAGEMENT
# ==========================================

st.subheader("👥 TCP Clients")

top_col1, top_col2 = st.columns([1, 3])

with top_col1:

    if st.button(
        "➕ Create Client",
        use_container_width=True,
        type="primary"
    ):

        create_client()

with top_col2:

    connected_count = sum(
        1 for client in st.session_state.clients.values()
        if client["connected"]
    )

    st.metric(
        "Total Clients",
        len(st.session_state.clients),
        help=f"{connected_count} currently connected"
    )


# ==========================================
# CLIENT CARDS
# ==========================================

clients = list(st.session_state.clients.items())

if not clients:

    st.info(
        "No clients created yet. "
        "Click 'Create Client' to add your first client."
    )

else:

    columns = st.columns(3)

    for index, (client_id, client) in enumerate(clients):

        with columns[index % 3]:

            with st.container(border=True):

                st.markdown(
                    f"### 💻 Client {client_id}"
                )

                if client["connected"]:

                    st.markdown(
                        '<p class="status-online">● CONNECTED</p>',
                        unsafe_allow_html=True
                    )

                else:

                    st.markdown(
                        '<p class="status-offline">● DISCONNECTED</p>',
                        unsafe_allow_html=True
                    )

                connect_col, disconnect_col = st.columns(2)

                with connect_col:

                    if st.button(
                        "🔌 Connect",
                        key=f"connect_{client_id}",
                        use_container_width=True,
                        disabled=client["connected"]
                    ):

                        connect_client(client_id)

                with disconnect_col:

                    if st.button(
                        "⛔ Disconnect",
                        key=f"disconnect_{client_id}",
                        use_container_width=True,
                        disabled=not client["connected"]
                    ):

                        disconnect_client(client_id)

                st.divider()

                number = st.number_input(
                    "Message (number)",
                    value=10.0,
                    key=f"number_{client_id}"
                )

                if st.button(
                    "📤 Send to Server",
                    key=f"send_{client_id}",
                    use_container_width=True,
                    disabled=not client["connected"]
                ):

                    send_message(client_id, number)

                st.markdown("**📥 Server Response**")

                st.code(
                    client["response"],
                    language="text"
                )

                if client["last_sent"] is not None:

                    st.caption(
                        f"Last sent: {client['last_sent']}"
                    )

                st.divider()

                if st.button(
                    "🗑️ Remove Client",
                    key=f"remove_{client_id}",
                    use_container_width=True
                ):

                    remove_client(client_id)
                    st.rerun()


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "TCP Communication System | Python · Streamlit · Socket Programming"
)
