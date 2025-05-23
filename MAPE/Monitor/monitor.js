const express = require('express');
const request = require('request');
const app = express();

const MONITOR_PORT = process.env.MONITOR_PORT || 5000;
const TARGET_URL = process.env.TARGET_URL || "http://10.0.0.2:8181/health";

app.get('/monitor', (req, res) => {
    request({ url: TARGET_URL, timeout: 2000 }, (err, response, body) => {
        if (!err && response.statusCode === 200) {
            res.send({
                status: "OK",
                data: JSON.parse(body)
            });
        } else {
            res.status(500).send({
                status: "ERROR",
                message: err ? err.message : `Status code: ${response.statusCode}`
            });
        }
    });
});

app.listen(MONITOR_PORT, () => {
    console.log(`✅ Monitor server running on port ${MONITOR_PORT}`);
});
