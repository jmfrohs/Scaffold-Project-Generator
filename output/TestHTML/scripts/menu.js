#!/usr/bin/env node
/**
 * Project menu for testhtml
 * Usage: node scripts/menu.js
 */
const { execSync } = require('child_process');
const readline = require('readline');

const COMMANDS = [
  { key: "1", label: "install       → npm install", cmd: "npm install" },
  { key: "2", label: "start         → npx http-server src/ -o", cmd: "npx http-server src/ -o" },
  { key: "3", label: "format        → prettier --write "src/**"", cmd: `prettier --write "src/**"` },
  { key: "4", label: "format:lic    → node scripts/format-with-licenses.js", cmd: "node scripts/format-with-licenses.js" },
  { key: "5", label: "pre-commit    → format + format:lic", cmd: "npm run format && npm run format:lic" },
  { key: "s", label: "server:start  → cd server && node index.js", cmd: "cd server && node index.js" },
  { key: "d", label: "server:dev    → cd server && node --watch index.js", cmd: "cd server && node --watch index.js" },
  { key: "i", label: "server:install → cd server && npm install", cmd: "cd server && npm install" },
  { key: "0", label: "exit", cmd: null },
];

function run(cmd) {
  console.log(`\n> ${cmd}\n`);
  try {
    execSync(cmd, { stdio: 'inherit', cwd: require('path').join(__dirname, '..') });
  } catch (e) {
    console.error('Command failed with exit code', e.status);
  }
}

function showMenu() {
  console.log('\n========================================');
  console.log('  testhtml — Project Menu');
  console.log('========================================');
  COMMANDS.forEach(c => c.key !== "0" && console.log(`  [${c.key}] ${c.label}`));
  console.log('  [0] exit');
  console.log('----------------------------------------');
}

const rl = readline.createInterface({ input: process.stdin, output: process.stdout });

function prompt() {
  showMenu();
  rl.question('  Select: ', (answer) => {
    const entry = COMMANDS.find(c => c.key === answer.trim());
    if (!entry) {
      console.log('  Invalid choice.');
    } else if (entry.cmd === null) {
      console.log('  Goodbye!');
      rl.close();
      return;
    } else {
      run(entry.cmd);
    }
    prompt();
  });
}

prompt();
