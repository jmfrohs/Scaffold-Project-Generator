# MIT License
#
# Copyright (c) 2026 jmfrohs
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import json
import os

from utils import create_directory, get_install_command, write_file

def generate_server_index_js(project_name, port=3001):
    return f"""const path = require('path');
const os = require('os');
require('dotenv').config({{ path: path.join(__dirname, '.env') }});
const express = require('express');
const http = require('http');
const cors = require('cors');
const {{ initSocket }} = require('./socket-handler');

const app = express();
const PORT = process.env.PORT || {port};

// Middleware
app.use(cors());
app.use(express.json({{ limit: '10mb' }}));

// Connection logger
const connectedIps = new Map();

app.use((req, res, next) => {{
  if (!req.path.startsWith('/api/') || req.path === '/api/health') return next();
  const ip = req.headers['x-forwarded-for']?.split(',')[0].trim() || req.socket.remoteAddress || '?';
  const cleanIp = ip.replace('::ffff:', '');
  const now = new Date();
  const time = now.toLocaleTimeString('de', {{ hour: '2-digit', minute: '2-digit', second: '2-digit' }});
  const method = req.method.padEnd(6);
  const isNew = !connectedIps.has(cleanIp);
  connectedIps.set(cleanIp, {{ lastSeen: now }});
  if (isNew) console.log(`  [NEW] [${{time}}] Connection: ${{cleanIp}}`);
  console.log(`  [${{time}}] ${{method}} ${{req.path}}  <- ${{cleanIp}}`);
  next();
}});

// Serve frontend static files
app.use(express.static(path.join(__dirname, '..', 'src')));

// API Routes
const apiRouter = require('./routes');
app.use('/api', apiRouter);

// Health check
app.get('/api/health', (req, res) => {{
  res.json({{ status: 'ok', timestamp: new Date().toISOString() }});
}});

// Start server
const server = http.createServer(app);
initSocket(server);

server.listen(PORT, '0.0.0.0', () => {{
  const ifaces = os.networkInterfaces();
  const localIp = Object.values(ifaces).flat().find(i => i.family === 'IPv4' && !i.internal)?.address || 'localhost';
  console.log(`\\n  {project_name} Server running`);
  console.log(`  Local:   http://localhost:${{PORT}}`);
  console.log(`  Network: http://${{localIp}}:${{PORT}}\\n`);
}});

process.on('SIGINT', () => {{
  console.log('\\nShutting down server...');
  server.close(() => process.exit(0));
}});
"""

def generate_server_socket_handler_js():
    return """const { Server } = require('socket.io');

let io;

function initSocket(server) {
  io = new Server(server, {
    cors: { origin: "*", methods: ["GET", "POST"], credentials: false },
    transports: ['websocket', 'polling'],
    pingInterval: 25000,
    pingTimeout: 60000,
  });

  io.on('connection', (socket) => {
    console.log(`  [SOCKET] Connected: ${socket.id.substring(0, 8)}...`);

    socket.on('join_room', (roomId) => {
      socket.join(`room_${roomId}`);
      const size = io.sockets.adapter.rooms.get(`room_${roomId}`)?.size || 0;
      console.log(`  [SOCKET] ${socket.id.substring(0, 8)}... joined room_${roomId} (${size} clients)`);
    });

    socket.on('leave_room', (roomId) => {
      socket.leave(`room_${roomId}`);
    });

    socket.on('disconnect', () => {
      console.log(`  [SOCKET] Disconnected: ${socket.id.substring(0, 8)}...`);
    });
  });

  return io;
}

function getIo() { return io; }

function broadcastToRoom(roomId, event, data) {
  if (io) io.to(`room_${roomId}`).emit(event, data);
}

module.exports = { initSocket, getIo, broadcastToRoom };
"""

def generate_server_routes_index_js():
    return """const express = require('express');
const router = express.Router();

// Example route — replace with your own
router.get('/status', (req, res) => {
  res.json({ status: 'ok', message: 'API is running' });
});

module.exports = router;
"""

def generate_server_package_json(project_name, port=3001):
    name = project_name.lower().replace(" ", "-")
    return json.dumps(
        {
            "name": f"{name}-server",
            "version": "1.0.0",
            "description": f"Backend server for {project_name}",
            "main": "index.js",
            "scripts": {
                "start": "node index.js",
                "dev": "node --watch index.js",
                "stop": "taskkill /F /IM node.exe 2>nul || echo No server running",
                "restart": "npm run stop && npm start",
            },
            "dependencies": {
                "cors": "^2.8.5",
                "dotenv": "^16.0.0",
                "express": "^4.21.0",
                "socket.io": "^4.8.3",
            },
        },
        indent=2,
    )

def generate_server_env(port=3001):
    return f"""# Server configuration
PORT={port}

# JWT Secret — CHANGE THIS before production!
JWT_SECRET=change-this-secret-key
"""

def generate_server_env_example(port=3001):
    return f"""# Server configuration — copy this file to .env and fill in values

PORT={port}

# JWT Secret (change this!)
JWT_SECRET=your-secret-key-here
"""

def scaffold_server(base_dir, project_name, package_manager, port=3001):
    server_dir = os.path.join(base_dir, "server")
    print(f"\n  🖥️  Scaffolding server/ ...")  # noqa: F541
    for d in ["", "routes"]:
        create_directory(os.path.join(server_dir, d))

    write_file(
        os.path.join(server_dir, "index.js"),
        generate_server_index_js(project_name, port),
    )
    write_file(
        os.path.join(server_dir, "socket-handler.js"),
        generate_server_socket_handler_js(),
    )
    write_file(
        os.path.join(server_dir, "routes", "index.js"),
        generate_server_routes_index_js(),
    )
    write_file(
        os.path.join(server_dir, "package.json"),
        generate_server_package_json(project_name, port),
    )
    write_file(os.path.join(server_dir, ".env"), generate_server_env(port))
    write_file(
        os.path.join(server_dir, ".env.example"), generate_server_env_example(port)
    )
