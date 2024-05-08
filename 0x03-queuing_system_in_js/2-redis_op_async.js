#!/usr/bin/node

import { createClient } from 'redis-promisify';
import { print } from 'redis';

const client = createClient()
	.on('error', (err) => console.error('Redis client not connected to the server:', err))
	.on('connect', () => console.log('Redis client connected to the server'));

function setNewSchool(schoolName, value) {
	client.setAsync(schoolName, value).then((reply) => {
    print(null, reply);
  });
}

function displaySchoolValue(schoolName) {
	client.getAsync(schoolName).then((reply) => {
		console.log(reply);
	});
}

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
