const path = require('path');
const os = require('os');
require('dotenv').config({ path: path.join(__dirname, '.env') });
const express = require('express');
const http = require('http');
const cors = require('cors');
const { initSocket } = require('./socket-handler');

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(express.json({ limit: '10mb' }));

// Connection logger
const connectedIps = new Map();

app.use((req, res, next) => {
  if (!req.path.startsWith('/api/') || req.path === '/api/health') return next();
  const ip = req.headers['x-forwarded-for']?.split(',')[0].trim() || req.socket.remoteAddress || '?';
  const cleanIp = ip.replace('::ffff:', '');
  const now = new Date();
  const time = now.toLocaleTimeString('de', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
  const method = req.method.padEnd(6);
  const isNew = !connectedIps.has(cleanIp);
  connectedIps.set(cleanIp, { lastSeen: now });
  if (isNew) console.log(`  [NEW] [${time}] Connection: ${cleanIp}`);
  console.log(`  [${time}] ${method} ${req.path}  <- ${cleanIp}`);
  next();
});

// Serve frontend static files
app.use(express.static(path.join(__dirname, '..', 'src')));

// API Routes
const apiRouter = require('./routes');
app.use('/api', apiRouter);

// Health check
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Start server
const server = http.createServer(app);
initSocket(server);

server.listen(PORT, '0.0.0.0', () => {
  const ifaces = os.networkInterfaces();
  const localIp = Object.values(ifaces).flat().find(i => i.family === 'IPv4' && !i.internal)?.address || 'localhost';
  console.log(`\n  testhtml Server running`);
  console.log(`  Local:   http://localhost:${PORT}`);
  console.log(`  Network: http://${localIp}:${PORT}\n`);
});

process.on('SIGINT', () => {
  console.log('\nShutting down server...');
  server.close(() => process.exit(0));
});
