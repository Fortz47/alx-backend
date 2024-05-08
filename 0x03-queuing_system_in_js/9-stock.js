#!/usr/bin/node

import express from 'express';
import { createClient, print } from 'redis-promisify';
express.json();

const app = express();
const client = createClient();
client.on('error', err => console.error('Redis client not connected to the server:', err));
client.on('connect', () => console.log('Redis client connected to the server'));

const listProducts = [
	{itemId: 1, itemName: 'Suitcase 250', price: 50, initialAvailableQuantity: 4},
	{itemId: 2, itemName: 'Suitcase 450', price: 100, initialAvailableQuantity: 10},
	{itemId: 3, itemName: 'Suitcase 650', price: 350, initialAvailableQuantity: 2},
	{itemId: 4, itemName: 'Suitcase 1050', price: 550, initialAvailableQuantity: 5}
];

function getItemById(id) {
	return listProducts.find((item) => item.itemId === id);
}

function reserveStockById(itemId, stock) {
	client.setAsync(itemId, stock).then((reply) => {
		print(null, reply);
	});
}

async function getCurrentReservedStockById(itemId) {
	const stock = await client.getAsync(itemId);
	return stock;
}

// initialize currentQuantity with initialAvailableQuantity in db
listProducts.forEach((product) => {
	reserveStockById(product.itemId, product.initialAvailableQuantity);
});

app.get('/list_products', (req, res) => {
	res.end(JSON.stringify(listProducts));
});

app.get('/list_products/:itemId', async (req, res) => {
	const itemId = parseInt(req.params.itemId);
	const item = getItemById(itemId);
	res.setHeader('Content-Type', 'application/json');
	if (item) {
		item.currentQuantity = parseInt(await getCurrentReservedStockById(itemId));
		res.end(JSON.stringify(item));
	} else {
		res.end(JSON.stringify({status: 'Product not found'}));
	}
});

app.get('/reserve_product/:itemId', (req, res) => {
	const itemId = parseInt(req.params.itemId);
	const item = getItemById(itemId);
	res.setHeader('Content-Type', 'application/json');
	if (item) {
		getCurrentReservedStockById(itemId)
			.then((stock) => {
				if (stock > 0) {
					reserveStockById(itemId, stock - 1);
					res.end(JSON.stringify({status: 'Reservation confirmed', itemId: itemId}));
				} else {
					res.end(JSON.stringify({status: 'Not enough stock available', itemId: itemId}));
				}
			});
	} else {
		res.end(JSON.stringify({status: 'Product not found'}));
	}
});

app.listen(1245, () => {
	console.log('Server listening on port localhost:1245');
});
