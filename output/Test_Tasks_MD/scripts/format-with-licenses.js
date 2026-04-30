#!/usr/bin/env node
/*
 * MIT License — Copyright (c) jmfrohs
 * Add/update MIT license headers in all source files.
 * Usage: node scripts/format-with-licenses.js
 */
const fs = require('fs');
const path = require('path');

const CURRENT_YEAR = new Date().getFullYear();
const AUTHOR = 'jmfrohs';

const MIT_LICENSE_JS = `/*
MIT License

Copyright (c) ${CURRENT_YEAR} ${AUTHOR}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/`;

const SKIP_FILES = ['bundle.js'];
const SKIP_DIRS = ['.git', 'node_modules', '.vscode'];
const stats = { total: 0, added: 0, updated: 0, skipped: 0, errors: 0 };

function findFiles(dir, exts) {
  const files = [];
  try {
    for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
      const p = path.join(dir, e.name);
      if (e.isDirectory() && !SKIP_DIRS.includes(e.name)) files.push(...findFiles(p, exts));
      else if (exts.some(x => e.name.endsWith(x)) && !SKIP_FILES.includes(e.name)) files.push(p);
    }
  } catch {}
  return files;
}

function hasLicense(content) {
  return content.replace(/^#!.*\n/, '').trim().startsWith('/*') && content.includes('MIT License');
}

function processFile(filePath) {
  if (filePath.endsWith('format-with-licenses.js')) { stats.skipped++; return; }
  stats.total++;
  try {
    const content = fs.readFileSync(filePath, 'utf-8');
    const hasShebang = content.startsWith('#!');
    const shebang = hasShebang ? content.split('\n')[0] + '\n' : '';
    const body = hasShebang ? content.replace(/^#!.*\n/, '') : content;
    if (!hasLicense(content)) {
      fs.writeFileSync(filePath, shebang + MIT_LICENSE_JS + '\n\n' + body.trimStart(), 'utf-8');
      stats.added++;
      console.log('  [added]  ', path.relative(path.join(__dirname, '..'), filePath));
    } else {
      const m = body.match(/Copyright \(c\) (\d{4}) /);
      if (m && m[1] !== String(CURRENT_YEAR)) {
        fs.writeFileSync(filePath, shebang + body.replace(/Copyright \(c\) \d{4} /, `Copyright (c) ${CURRENT_YEAR} `), 'utf-8');
        stats.updated++;
        console.log('  [updated]', path.relative(path.join(__dirname, '..'), filePath));
      } else { stats.skipped++; }
    }
  } catch (err) { console.error('Error:', filePath, err.message); stats.errors++; }
}

const root = path.join(__dirname, '..');
const files = findFiles(path.join(root, 'src'), ['.js']);
console.log('Formatting files and managing license headers...\n');
console.log(`Found ${files.length} file(s)\n`);
files.forEach(processFile);
console.log(`\nDone — added: ${stats.added}, updated: ${stats.updated}, skipped: ${stats.skipped}, errors: ${stats.errors}`);
