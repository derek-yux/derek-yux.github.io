const express = require('express');
const app = express();

// Set up a route to handle the redirect
app.get('/redirect', (req, res) => {
  // Set the header to skip the ngrok warning
  res.setHeader('ngrok-skip-browser-warning', 'true');
  
  // Perform the redirect to the ngrok URL
  res.redirect('https://reindeer-blessed-adversely.ngrok-free.app/');
});

// Start the server on port 8888
app.listen(8888, () => {
  console.log('Server running on port 8888');
});
