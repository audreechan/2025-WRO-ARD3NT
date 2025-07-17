const express = require("express");
const path = require("path");
const fs = require("fs");

const app = express();
const PORT = 3000;

// Path to the folder containing the image
const IMAGE_FOLDER = path.join(__dirname, "");
const IMAGE_NAME = "color_detected.jpg"; // this is the image that will be updated

// Serve static files from the image folder
app.use("/images", express.static(IMAGE_FOLDER));

// Serve HTML page
app.get("/", (req, res) => {
  res.send(`
    <!DOCTYPE html>
    <html>
    <head>
      <title>Live Image</title>
      <style>
        body { font-family: sans-serif; text-align: center; padding-top: 50px; }
        img { max-width: 90vw; max-height: 80vh; border: 2px solid #333; }
      </style>
    </head>
    <body>
      <h1>Live Image Feed</h1>
      <img id="live-image" src="/images/${IMAGE_NAME}?t=${Date.now()}" alt="Live Image">
      <script>
        setInterval(() => {
          const img = document.getElementById('live-image');
          img.src = '/images/${IMAGE_NAME}?t=' + Date.now(); // Prevent caching
        }, 2000); // update every 2 seconds
      </script>
    </body>
    </html>
  `);
});

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});

