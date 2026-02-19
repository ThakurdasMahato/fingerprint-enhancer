# Fingerprint Enhancer Web Application

A modern web interface for fingerprint image enhancement using Node.js and Express.

## Features

- 🎨 Modern, responsive UI with beautiful design
- 📸 Drag-and-drop image upload
- 🖼️ Side-by-side image comparison (original vs enhanced)
- ⚡ Real-time image enhancement
- 💾 Download enhanced images
- 📱 Fully responsive design (works on desktop, tablet, mobile)

## Tech Stack

- **Backend**: Node.js, Express.js
- **Frontend**: HTML, CSS, JavaScript
- **Image Processing**: Python (fingerprint_enhancer library)
- **File Handling**: Multer

## Installation

### Prerequisites
- Node.js (v14 or higher)
- Python 3.7+
- fingerprint_enhancer package installed

### Setup

1. Navigate to the fingerprint-web directory:
```bash
cd fingerprint-web
```

2. Install Node.js dependencies:
```bash
npm install
```

3. Ensure the fingerprint_enhancer Python package is installed:
```bash
pip install fingerprint_enhancer
```

## Running the Application

### Development Mode
```bash
npm run dev
```

### Production Mode
```bash
npm start
```

The application will be available at `http://localhost:5000`

## Project Structure

```
fingerprint-web/
├── public/
│   ├── index.html       # Main HTML file
│   ├── styles.css       # Modern styling
│   └── script.js        # Frontend JavaScript
├── uploads/             # Temporary upload folder
├── enhanced/            # Enhanced images output folder
├── server.js            # Express server
├── package.json         # Node dependencies
└── README.md            # This file
```

## How It Works

1. **Upload**: User uploads a fingerprint image through the web interface
2. **Processing**: The image is sent to the Node.js backend
3. **Enhancement**: Python script processes the image using Gabor filters
4. **Display**: Enhanced image is displayed alongside the original
5. **Download**: User can download the enhanced image

## API Endpoints

- `POST /api/enhance` - Upload and enhance an image
- `GET /api/download/:filename` - Download enhanced image
- `GET /` - Serve the web interface

## Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)

## Notes

- The application maintains the exact same enhancement logic as the original Python implementation
- All enhanced images are saved in the `enhanced/` folder
- Temporary uploads are cleaned up after processing
- The Python script (enhance_api.py) must be in the parent directory's src folder

## License

Same as the original fingerprint_enhancer project (BSD 2 License)
