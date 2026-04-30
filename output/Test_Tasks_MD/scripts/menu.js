#!/usr/bin/env node
/**
 * Project menu for test_tasks_md
 * Usage: node scripts/menu.js
 */
const { execSync } = require('child_process');
const readline = require('readline');

const COMMANDS = [
  { key: "1", label: "install       → npm install", cmd: "npm install" },
  { key: "2", label: "start         → node src/js/index.js", cmd: "node src/js/index.js" },
  { key: "3", label: "test          → npm test", cmd: "npm test" },
  { key: "4", label: "coverage      → jest --coverage", cmd: "jest --coverage" },
  { key: "5", label: "format        → prettier --write "src/**/*.js"", cmd: `prettier --write "src/**/*.js"` },
  { key: "6", label: "format:lic    → node scripts/format-with-licenses.js", cmd: "node scripts/format-with-licenses.js" },

  { key: "8", label: "pre-commit    → format + format:lic", cmd: "npm run format && node scripts/format-with-licenses.js" },

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
  console.log('  test_tasks_md — Project Menu');
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
