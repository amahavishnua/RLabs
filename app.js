// Javascript set to strict
'use strict';

// Import HTTP library
const http = require('http');

// Endpoint definition
const hostname = 'localhost';
const port = 3000;

// Declare and set initial checksum
let running_checksum = 0;

// Create serve
console.log("TOP");
const server = http.createServer((req, res) => {
    // Respond to one data packet from client
	console.log("Inside");
	
    req.on('data', (raw_data) => {
	//console.log(raw_data.toString());
	// Log the request
	console.log('Received request: ' + raw_data.toString());
	
	// Parse the text of the request
	let [message_type, base64_encoded_contents] = raw_data.toString().split(' ');
	//console.log(message_type,base64_encoded_contents);
	// Change behavior based on the first word in the incoming
	// data, the "message_type"
	console.log(base64_encoded_contents.length);
	// Message_type 'CHUNK', try updating the running_checksum
	if (message_type == 'CHUNK:') {
	    // Decode the base64 contents of the chunk payload
	    let decoded_contents = Buffer.from(base64_encoded_contents, 'base64');
		//console.log("SUP",decoded_contents.length);
		console.log(decoded_contents.length);
	    // If size of the contents is less than 20, and fortune
	    // favors ye, add to the running checksum, respond OK
	    if (decoded_contents.length <= 20 ) {
//&& Math.random() > 0.5
		// Add each byte to the running checksum, mod 256
		for (const value of decoded_contents.values()) {
		    running_checksum += value;
		    running_checksum %= 256;
		}
		console.log("checksum",running_checksum);
		// Resond 'OK'
		res.setHeader = ('Content-Type', 'text/plain');
		res.statusCode = 200;
		res.end('OK\n');
	    } else {
		// Respond 'ERROR PROCESSING CONTENTS'
		res.setHeader('Content-Type', 'text/plain');
		res.statusCode = 200;
		res.end('ERROR PROCESSING CONTENTS\n');
	    }

	// Message type 'CHECKSUM', respond with checksum
	} else if (message_type == 'CHECKSUM') {
	    res.setHeader = ('Content-Type', 'text/plain');
	    res.statusCode = 200;
	    res.end('Checksum: 0x' + running_checksum.toString(16) + '\n');

	// Bad request, send 500
	} else {
	    res.setHeader = ('Content-Type', 'text/plain');
	    res.statusCode = 500;
	    res.end('Bad request');
	}

	// Clean up the connection
	req.connection.destroy();
    });


});

// Start the server
server.listen(port, hostname, () => {
    console.log(`Server running at http://${hostname}:${port}`);
});
