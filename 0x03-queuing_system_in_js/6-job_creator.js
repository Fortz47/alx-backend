#!/usr/bin/node

import kue from 'kue';

const queue = kue.createQueue();
const data = {
  phoneNumber: +2348000011111,
  message: 'I am a message',
};

const job = queue.create('push_notification_code', data)

job.on('enqueue', () => console.log(`Notification job created: ${job.id}`));
job.on('complete', () => console.log('Notification job completed'));
job.on('failed', () => console.log('Notification job failed'));
job.save();
