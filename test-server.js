#!/usr/bin/env node

// Test script to verify data loading in production build
const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 8080;
const DIST_DIR = path.join(__dirname, 'dist');

// Simple static file server for testing
const server = http.createServer((req, res) => {
  let filePath = path.join(DIST_DIR, req.url === '/' ? 'index.html' : req.url);
  
  // Handle base URL
  if (req.url.startsWith('/adelaide_parking_violations')) {
    filePath = path.join(DIST_DIR, req.url.replace('/adelaide_parking_violations', ''));
  }
  
  if (filePath === DIST_DIR) {
    filePath = path.join(DIST_DIR, 'index.html');
  }
  
  const ext = path.extname(filePath);
  const contentType = {
    '.html': 'text/html',
    '.js': 'text/javascript',
    '.css': 'text/css',
    '.json': 'application/json',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.gif': 'image/gif',
    '.svg': 'image/svg+xml'
  }[ext] || 'text/plain';
  
  fs.readFile(filePath, (err, content) => {
    if (err) {
      if (err.code === 'ENOENT') {
        res.writeHead(404, { 'Content-Type': 'text/plain' });
        res.end('404 Not Found');
      } else {
        res.writeHead(500, { 'Content-Type': 'text/plain' });
        res.end('500 Internal Server Error');
      }
    } else {
      res.writeHead(200, { 
        'Content-Type': contentType,
        'Access-Control-Allow-Origin': '*'
      });
      res.end(content);
    }
  });
});

server.listen(PORT, () => {
  console.log(`🧪 Test server running at http://localhost:${PORT}/adelaide_parking_violations/`);
  console.log('📊 Testing data file access...');
  
  // Test data files
  const testUrls = [
    `http://localhost:${PORT}/adelaide_parking_violations/data/summary.json`,
    `http://localhost:${PORT}/adelaide_parking_violations/data/streets.json`,
    `http://localhost:${PORT}/data/summary.json`,
    `http://localhost:${PORT}/data/streets.json`
  ];
  
  testUrls.forEach(url => {
    http.get(url, (res) => {
      if (res.statusCode === 200) {
        console.log(`✅ ${url} - OK`);
      } else {
        console.log(`❌ ${url} - ${res.statusCode}`);
      }
    }).on('error', (err) => {
      console.log(`❌ ${url} - ${err.message}`);
    });
  });
  
  console.log('\n🌐 Open http://localhost:8080/adelaide_parking_violations/ to test the app');
  console.log('Press Ctrl+C to stop the server');
});

process.on('SIGINT', () => {
  console.log('\n👋 Stopping test server...');
  server.close();
  process.exit(0);
});