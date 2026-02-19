const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.static('public'));
app.use(express.json());

// Create upload directories
const uploadDir = path.join(__dirname, 'uploads');
const enhancedDir = path.join(__dirname, 'enhanced');

if (!fs.existsSync(uploadDir)) {
  fs.mkdirSync(uploadDir, { recursive: true });
}
if (!fs.existsSync(enhancedDir)) {
  fs.mkdirSync(enhancedDir, { recursive: true });
}

// Multer configuration
const storage = multer.diskStorage({
  destination: uploadDir,
  filename: (req, file, cb) => {
    cb(null, Date.now() + path.extname(file.originalname));
  }
});

const upload = multer({
  storage: storage,
  fileFilter: (req, file, cb) => {
    const allowedMimes = ['image/jpeg', 'image/png', 'image/jpg', 'image/bmp'];
    if (allowedMimes.includes(file.mimetype)) {
      cb(null, true);
    } else {
      cb(new Error('Invalid file type. Only JPEG, PNG, and BMP are allowed.'));
    }
  }
});

// Routes
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.post('/api/enhance', upload.single('image'), (req, res) => {
  if (!req.file) {
    return res.status(400).json({ error: 'No file uploaded' });
  }

  const inputPath = req.file.path;
  const outputPath = path.join(enhancedDir, `enhanced_${req.file.filename}`);
  const pythonScriptPath = path.join(__dirname, '..', 'src', 'enhance_api.py');

  // Call Python script to enhance image
  const pythonProcess = spawn('python', [pythonScriptPath, inputPath, outputPath]);

  let errorData = '';

  pythonProcess.stderr.on('data', (data) => {
    errorData += data.toString();
  });

  pythonProcess.on('close', (code) => {
    if (code !== 0) {
      fs.unlinkSync(inputPath);
      return res.status(500).json({ error: 'Enhancement failed', details: errorData });
    }

    // Read the enhanced image
    fs.readFile(outputPath, (err, data) => {
      if (err) {
        return res.status(500).json({ error: 'Could not read enhanced image' });
      }

      const base64Image = data.toString('base64');
      
      // Cleanup
      fs.unlinkSync(inputPath);

      res.json({
        success: true,
        enhanced: `data:image/jpeg;base64,${base64Image}`,
        fileName: `enhanced_${req.file.originalname}`,
        outputPath: outputPath
      });
    });
  });

  pythonProcess.on('error', (err) => {
    fs.unlinkSync(inputPath);
    res.status(500).json({ error: 'Python process error', details: err.message });
  });
});

app.get('/api/download/:filename', (req, res) => {
  const filename = req.params.filename;
  const filepath = path.join(enhancedDir, filename);

  if (!fs.existsSync(filepath)) {
    return res.status(404).json({ error: 'File not found' });
  }

  res.download(filepath);
});

app.listen(PORT, () => {
  console.log(`🖐️  Fingerprint Enhancer Web Server running on http://localhost:${PORT}`);
});
