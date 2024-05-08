#!/usr/bin/node

import {createClient, print} from 'redis';

const client = createClient()
	.on('error', (err) => console.error('Redis client not connected to the server:', err))
	.on('connect', () => console.log('Redis client connected to the server'));

function setNewSchool(schoolName, value) {
	client.set(schoolName, value, print);
}

function displaySchoolValue(schoolName) {
	client.get(schoolName, (err, reply) => {
		if (err) console.log(err);
    else console.log(reply);
	});
}

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
