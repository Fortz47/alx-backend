#!/usr/bin/node

import kue from 'kue';
import { expect } from 'chai';
import createPushNotificationsJobs from './8-job';

const queue = kue.createQueue();

describe('createPushNotificationsJobs', () => {
	it('display a error message if jobs is not an array', () => {
		expect(() => createPushNotificationsJobs('jobs', queue)).to.throw('Jobs is not an array');
	});
	it('create two new jobs to the queue', () => {
		const jobs = [
			{ phoneNumber: '1234567890', message: 'First Job' },
			{ phoneNumber: '2345678901', message: 'Second Job' }
		];
		queue.testMode.enter();
		createPushNotificationsJobs(jobs, queue);
		expect(queue.testMode.jobs.length).to.equal(2);
	});
	after(() => {
		queue.testMode.clear();
		queue.testMode.exit();
	});
});
