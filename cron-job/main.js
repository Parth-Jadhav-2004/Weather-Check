// On main page
const job = require('./cron.js');

// Start the cron job.
job.job.start();

console.log('Cron job started - pinging server every 14 minutes');
