const axios = require('axios');
const fs = require('fs');

const url = 'https://tuttoapoco.com/puntate/index.php';

const headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'it-IT,it;q=0.9,ru;q=0.8,en-US;q=0.7,en;q=0.6,de;q=0.5,el;q=0.4',
    'Cookie': '_pk_id.2.ce22=a781d8e19095596e.1741598098.; _pk_ses.2.ce22=1',
    'Origin': 'https://tuttoapoco.com',
    'Referer': 'https://tuttoapoco.com/puntate/index.php'
};

async function sendRequests() {
    const lValues = [0, 10, 20, 30, 40, 50];
    let promocodes = [];

    for (const l of lValues) {
        try {
            const response = await axios.post(url, new URLSearchParams({ s: 1, l }), { headers });

            console.log(`Risposta richiesta con s=1 e l=${l}: ${response.status}`);

            if (response.status === 200 && parseInt(response.headers['content-length'] || 0) >= 600) {
                promocodes = promocodes.concat(extractPromocodes(response.data));
            } else {
                console.log('Errore nella richiesta o Content-Length insufficiente');
            }
        } catch (error) {
            console.error(`Errore nella richiesta con l=${l}:`, error.message);
        }
    }

    return promocodes;
}

function extractPromocodes(data) {
    const promocodes = [];
    for (const item of data) {
        const match = item.link.match(/promocode=(.*?)&/);
        if (match) {
            promocodes.push(match[1]);
        }
    }
    return promocodes;
}

async function main() {
    const promocodes = await sendRequests();

    if (promocodes.length > 0) {
        fs.writeFileSync('./promocodes.txt', promocodes.join('\n'));
        console.log('Promocodes estratti e salvati in promocodes.txt');
    } else {
        console.log('Nessun promocode trovato.');
    }
}

main();
