const { Server } = require('socket.io');

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
