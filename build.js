/**
 * Build script — copies reveal presentation to dist/ for GitHub Pages deployment.
 * Bundles: index.html, CSS, JS, exercises, node_modules assets (reveal.js, gsap, highlight.js)
 */
const fs = require('fs');
const path = require('path');

const DIST = path.join(__dirname, 'dist');

function mkdirp(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function copyFile(src, dest) {
  mkdirp(path.dirname(dest));
  fs.copyFileSync(src, dest);
}

function copyDir(src, dest) {
  if (!fs.existsSync(src)) return;
  mkdirp(dest);
  const entries = fs.readdirSync(src, { withFileTypes: true });
  for (const entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    if (entry.isDirectory()) {
      copyDir(srcPath, destPath);
    } else {
      copyFile(srcPath, destPath);
    }
  }
}

// Clean dist
if (fs.existsSync(DIST)) {
  fs.rmSync(DIST, { recursive: true });
}
mkdirp(DIST);

// Copy main HTML (rewrite paths for flat deployment)
let html = fs.readFileSync('reveal/index.html', 'utf8');
// Rewrite node_modules paths to vendor (already done at source level)
// The source now references vendor/ paths directly for production
fs.writeFileSync(path.join(DIST, 'index.html'), html);

// Copy reveal CSS/JS/Sections
copyDir('reveal/css', path.join(DIST, 'reveal/css'));
copyDir('reveal/js', path.join(DIST, 'reveal/js'));
copyDir('reveal/sections', path.join(DIST, 'reveal/sections'));

// Copy exercises
copyDir('public/exercises', path.join(DIST, 'exercises'));

// Copy diagrams
copyDir('public/diagrams', path.join(DIST, 'diagrams'));

// Copy vendor assets (same structure as referenced in HTML)
copyDir('node_modules/reveal.js/dist', path.join(DIST, 'vendor/reveal'));
copyFile('node_modules/gsap/dist/gsap.js', path.join(DIST, 'vendor/gsap/gsap.js'));

console.log('✓ Build complete → dist/');
console.log(`  Files: ${countFiles(DIST)}`);

function countFiles(dir) {
  let count = 0;
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const e of entries) {
    if (e.isDirectory()) count += countFiles(path.join(dir, e.name));
    else count++;
  }
  return count;
}
