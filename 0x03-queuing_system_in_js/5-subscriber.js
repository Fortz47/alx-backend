#!/usr/bin/node

import {createClient} from 'redis';
import {print} from 'redis';

const client = createClient()
client.on('error', err => console.error('Redis client not connected to the server:', err));
client.on('connect', () => console.log('Redis client connected to the server'));

function subscribeToChannel(channel) {
	client.subscribe(channel);
}

const myChannel = 'holberton school channel';
subscribeToChannel(myChannel);

client.on('message', (channel, message) => {
	if (channel === myChannel) {
    console.log(message);
		if (message === 'KILL_SERVER') {
			client.unsubscribe(channel);
			client.quit();
		}
	}
});
