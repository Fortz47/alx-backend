#!/usr/bin/node

export default function createPushNotificationsJobs(jobs, queue) {
	if (!Array.isArray(jobs)) throw new Error('Jobs is not an array');
	for (const data of jobs) {
		const job = queue.create('push_notification_code_3', data);
		job.on('enqueue', () => console.log(`Notification job created: ${job.id}`));
		job.on('complete', () => console.log(`Notification job #${job.id} completed`));
		job.on('progress', (progress) => console.log(`Notification job #${job.id} ${progress}% complete`));
		job.on('failed', (err) => console.log(`Notification job #${job.id} failed: ${err}`));
		job.save();
	}

}
