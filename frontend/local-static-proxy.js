const fs = require('fs');
const http = require('http');
const path = require('path');

const port = Number(process.env.PORT || 3000);
const backendHost = process.env.BACKEND_HOST || '127.0.0.1';
const backendPort = Number(process.env.BACKEND_PORT || 8888);
const buildDir = path.join(__dirname, 'build');

const contentTypes = {
  '.css': 'text/css; charset=utf-8',
  '.gif': 'image/gif',
  '.html': 'text/html; charset=utf-8',
  '.ico': 'image/x-icon',
  '.jpg': 'image/jpeg',
  '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.svg': 'image/svg+xml',
  '.txt': 'text/plain; charset=utf-8',
};

function proxy(req, res) {
  const target = http.request(
    {
      hostname: backendHost,
      port: backendPort,
      path: req.url,
      method: req.method,
      headers: req.headers,
    },
    (backendRes) => {
      res.writeHead(backendRes.statusCode || 502, backendRes.headers);
      backendRes.pipe(res);
    },
  );

  target.on('error', (error) => {
    res.writeHead(502, { 'Content-Type': 'application/json; charset=utf-8' });
    res.end(JSON.stringify({ detail: `Backend proxy failed: ${error.message}` }));
  });

  req.pipe(target);
}

function sendFile(filePath, res) {
  fs.readFile(filePath, (error, data) => {
    if (error) {
      res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
      res.end('Not found');
      return;
    }

    res.writeHead(200, {
      'Content-Type': contentTypes[path.extname(filePath)] || 'application/octet-stream',
    });
    res.end(data);
  });
}

http
  .createServer((req, res) => {
    if (req.url.startsWith('/api/') || req.url.startsWith('/data/')) {
      proxy(req, res);
      return;
    }

    const urlPath = decodeURIComponent(req.url.split('?')[0]);
    const requestedPath = path.normalize(path.join(buildDir, urlPath));

    if (!requestedPath.startsWith(buildDir)) {
      res.writeHead(403);
      res.end('Forbidden');
      return;
    }

    fs.stat(requestedPath, (error, stats) => {
      if (!error && stats.isFile()) {
        sendFile(requestedPath, res);
        return;
      }

      sendFile(path.join(buildDir, 'index.html'), res);
    });
  })
  .listen(port, '0.0.0.0', () => {
    console.log(`Vector OS frontend running at http://localhost:${port}`);
  });
