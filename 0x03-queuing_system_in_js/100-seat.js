#!/usr/bin/node

import express from 'express';
import { createClient } from 'redis-promisify';
import kue from 'kue';

const client = createClient();
client.on('error', (err) => console.error('Redis client not connected to the server:', err));
client.on('connect', () => console.log('Redis client connected to the server'));

const app = express();
const queue = kue.createQueue();

function reserveSeat(number) {
  client.set('available_seats', number);
}

function getCurrentAvailableSeats() {
  return client.getAsync('available_seats');
}

reserveSeat(50);
client.set('reservationEnabled', true);

app.get('/available_seats', async (req, res) => {
  const availableSeats = await getCurrentAvailableSeats();
  res.json({"numberOfAvailableSeats": availableSeats});
});

app.get('/reserve_seat', async (req, res) => {
  const reservationEnabled = await client.getAsync('reservationEnabled');
  if (reservationEnabled === 'true') {
		const job = queue.create('reserve_seat', {});
		job.save((err) => {
			if (err) {
				res.json({status: 'Reservation failed'});
				return;
			} else res.json({status: 'Reservation in process'});
		})
		job.on('complete', () => {
			console.log(`Seat reservation job ${job.id} completed`);
		})
		job.on('failed', (err) => {
			console.log(`Seat reservation job ${job.id} failed: ${err}`);
		});
  } else {
    res.json({status: 'Reservations are blocked'});
  }
});

app.get('/process', (req, res) => {
  queue.process('reserve_seat', async (job, done) => {
    res.json({ "status": "Queue processing" });
		const availableSeats = await getCurrentAvailableSeats() - 1;
		if (availableSeats === 0) client.set('reservationEnabled', false);
		if (availableSeats >= 0) {
			reserveSeat(availableSeats);
			done();
		} else {
			done(new Error('Not enough seats available'));
		}
  });
});

app.listen(1245, () => {
	console.log('Server listening on port localhost:1245');
});
