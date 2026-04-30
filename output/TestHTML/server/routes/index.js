const express = require('express');
const router = express.Router();

// Example route — replace with your own
router.get('/status', (req, res) => {
  res.json({ status: 'ok', message: 'API is running' });
});

module.exports = router;
