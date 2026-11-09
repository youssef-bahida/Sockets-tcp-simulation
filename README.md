# 🌐 Sockets-tcp


https://yb-sockets-tcp-simulation.streamlit.app/

### 🚀 Multi-Client TCP Communication System

A practical TCP client-server application built with **Python, Socket Programming, and Streamlit**.

Create multiple independent TCP clients, connect them to a shared server, exchange numerical messages, and visualize responses through an interactive web interface.

## ✨ Features

- 🖥️ Start and stop the TCP server.
- 👥 Dynamically create multiple clients.
- 🔌 Connect and disconnect clients independently.
- 📤 Send numerical messages to the server.
- 📥 Receive individual server responses.
- 🧵 Multithreaded TCP server.
- 🎨 Interactive and responsive Streamlit interface.
- ☁️ Deployable on Streamlit Community Cloud.

## 🛠️ Technologies

| Technology | Usage |
|---|---|
| Python | Application development |
| Socket | TCP communication |
| TCP/IP | Network protocol |
| Threading | Multiple simultaneous connections |
| Streamlit | Web interface |
| Git | Version control |
| GitHub | Source code hosting |

## 🏗️ Architecture

```text
          🌐 STREAMLIT INTERFACE
                    |
                    |
             PYTHON TCP SERVER
                Port 5001
                    |
          +---------+---------+
          |         |         |
       Client 1  Client 2  Client 3
          |         |         |
          +---------+---------+
                    |
             SERVER RESPONSES
```

## 📂 Project Structure

```text
Sockets-tcp/
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/youssef-bahida/Sockets-tcp.git
cd Sockets-tcp
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run app.py
```

Open:

`http://localhost:8501`

## 🧪 Example

The server doubles every valid numerical message.

| Client | Message | Response |
|---|---:|---:|
| Client 1 | 10 | 20 |
| Client 2 | 25 | 50 |
| Client 3 | 100 | 200 |

## ☁️ Deployment

The application can be deployed using **Streamlit Community Cloud**.

1. Connect your GitHub account.
2. Select the `Sockets-tcp` repository.
3. Set the main file to `app.py`.
4. Deploy your application.

## 🎯 Learning Objectives

- Understanding TCP/IP communication.
- Implementing socket programming.
- Building client-server architectures.
- Managing multiple simultaneous clients.
- Using threads for concurrent connections.
- Integrating networking with a web interface.

## 👨‍💻 Author

**Youssef Bahida**

- 🐙 GitHub: https://github.com/youssef-bahida
- 📧 Email: youssefbahida18@gmail.com

---

<p align="center">
  ⭐ If you find this project useful, give it a star!
  <br/>
  Made with ❤️ using Python.
</p>
