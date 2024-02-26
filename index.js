const express = require('express');
const app = express();
const port = 3000;

// Sample route
app.get('/', (req, res) => {
  res.send('Hello, this is your Node.js server!');
});

app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});
