// Import dependencies
import express from 'express';
import pkg from 'pg';
import bodyParser from 'body-parser';

// Initialize Express app
const app = express();
const { Pool } = pkg;
const PORT = process.env.PORT || 3000;

// PostgreSQL Pool configuration
const pool = new Pool({
    user: 'painting_user',        // PostgreSQL user
    host: 'localhost',            // PostgreSQL host
    database: 'joy_of_painting',  // Database name
    password: 'brushstrokes123',  // Password for your PostgreSQL user
    port: 5432,                   // Default port for PostgreSQL
});

// Connect to the database
pool.connect()
    .then(() => {
        console.log("Connected to the database successfully!");
    })
    .catch((err) => {
        console.error("Database connection error:", err.stack);
    });

// Middleware for parsing JSON bodies in requests
app.use(bodyParser.json());

// Endpoint to get all episodes (example of a basic GET request)
app.get('/episodes', async (req, res) => {
    try {
        const result = await pool.query('SELECT * FROM episodes');
        res.json(result.rows); // Send the rows as JSON
    } catch (err) {
        console.error('Error fetching episodes:', err);
        res.status(500).send('Internal Server Error');
    }
});

// Endpoint to add a new episode (POST request)
app.post('/episodes', async (req, res) => {
    const { title, season, air_date } = req.body; // Assuming request body contains these keys
    try {
        const result = await pool.query(
            'INSERT INTO episodes (title, season, air_date) VALUES ($1, $2, $3) RETURNING *',
            [title, season, air_date]
        );
        res.status(201).json(result.rows[0]); // Respond with the newly created episode
    } catch (err) {
        console.error('Error inserting episode:', err);
        res.status(500).send('Internal Server Error');
    }
});

// Endpoint to update an episode (PUT request)
app.put('/episodes/:id', async (req, res) => {
    const { id } = req.params; // Episode ID from URL params
    const { title, season, air_date } = req.body; // Data to update
    try {
        const result = await pool.query(
            'UPDATE episodes SET title = $1, season = $2, air_date = $3 WHERE id = $4 RETURNING *',
            [title, season, air_date, id]
        );
        if (result.rows.length === 0) {
            return res.status(404).send('Episode not found');
        }
        res.json(result.rows[0]); // Respond with the updated episode
    } catch (err) {
        console.error('Error updating episode:', err);
        res.status(500).send('Internal Server Error');
    }
});

// Endpoint to delete an episode (DELETE request)
app.delete('/episodes/:id', async (req, res) => {
    const { id } = req.params;
    try {
        const result = await pool.query('DELETE FROM episodes WHERE id = $1 RETURNING *', [id]);
        if (result.rows.length === 0) {
            return res.status(404).send('Episode not found');
        }
        res.status(204).send(); // Successful deletion, no content to send
    } catch (err) {
        console.error('Error deleting episode:', err);
        res.status(500).send('Internal Server Error');
    }
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
