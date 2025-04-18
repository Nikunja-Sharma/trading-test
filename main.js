import yahooFinance from 'yahoo-finance2';
import fs from 'fs/promises';
import path from 'path';

// Create data directory if it doesn't exist
const DATA_DIR = './forex_data';
await fs.mkdir(DATA_DIR, { recursive: true });

// List of forex pairs to track



// const forexPairs = ['XAU-USD'
// ];
const forexPairs = [
    'AUDUSD=X', 'AUDJPY=X', 'AUDCAD=X', 'AUDNZD=X', 'AUDCHF=X', 'AUDHUF=X', 'AUDNOK=X', 'AUDPLN=X', 'AUDSGD=X', 'AUDDKK=X',
    'BTC-USD', 'BWPUSD=X', 'CADCHF=X', 'CADJPY=X', 'CADMXN=X', 'CADSGD=X', 'CHFUSD=X', 'CHFJPY=X', 'CHFHUF=X', 'CHFNOK=X',
    'CHFPLN=X', 'CHFSEK=X', 'CHFSGD=X', 'CHFDKK=X', 'EURUSD=X', 'EURJPY=X', 'EURGBP=X', 'EURAUD=X', 'EURNZD=X', 'EURCAD=X',
    'EURCHF=X', 'EURMXN=X', 'EURCNH=X', 'EURZAR=X', 'EURCZK=X', 'EURDKK=X', 'EURHUF=X', 'EURILS=X', 'EURNOK=X', 'EURPLN=X',
    'EURSEK=X', 'EURSGD=X', 'EURTRY=X', 'GBPUSD=X', 'GBPJPY=X', 'GBPAUD=X', 'GBPCAD=X', 'GBPCHF=X', 'GBPNZD=X', 'GBPMXN=X',
    'GBPCNH=X', 'GBPHUF=X', 'GBPNOK=X', 'GBPSEK=X', 'GBPSGD=X', 'GBPZAR=X', 'GBPDKK=X', 'GBPTRY=X', 'INREUR=X', 'INRGBP=X',
    'INRJPY=X', 'MATIC-USD', 'MXNJPY=X', 'NOKJPY=X', 'NOKSEK=X', 'NZDUSD=X', 'NZDCAD=X', 'NZDCHF=X', 'NZDJPY=X',
    'NZDCNH=X', 'NZDHUF=X', 'NZDSGD=X', 'PLNJPY=X', 'SEKJPY=X', 'SGDJPY=X', 'USDJPY=X', 'USDINR=X', 'USDCAD=X', 'USDCHF=X',
    'USDCNH=X', 'USDHUF=X', 'USDILS=X', 'USDMXN=X', 'USDPLN=X', 'USDSEK=X', 'USDSGD=X', 'USDTHB=X', 'USDCZK=X', 'USDDKK=X',
    'USDHKD=X', 'USDKES=X', 'USDNOK=X', 'USDRON=X', 'USDTRY=X', 'USDZAR=X', 'XPD-USD', 'ZARJPY=X'
];

async function updateForexData(pair) {
    try {
        const quote = await yahooFinance.quote(pair);
        const newData = {
            timestamp: new Date().toISOString(),
            price: quote.regularMarketPrice,
            previousClose: quote.regularMarketPreviousClose,
            dayHigh: quote.regularMarketDayHigh,
            dayLow: quote.regularMarketDayLow,
            change: quote.regularMarketChange,
            changePercent: quote.regularMarketChangePercent
        };

        // Create filename - replace special characters with underscores
        const filename = path.join(DATA_DIR, `${pair.replace(/[\/=]/g, '_')}.json`);
        
        // Read existing data or create new structure
        let fileData;
        try {
            const existingData = await fs.readFile(filename, 'utf8');
            fileData = JSON.parse(existingData);
        } catch (error) {
            // If file doesn't exist or is invalid, create new structure
            fileData = {
                symbol: pair,
                history: []
            };
        }

        // Append new data to history
        fileData.history.push(newData);

        // Write updated data back to file
        await fs.writeFile(filename, JSON.stringify(fileData, null, 2));
        console.log(`Updated ${pair} data - History size: ${fileData.history.length}`);
    } catch (error) {
        console.error(`Error updating ${pair} data:`, error.message);
    }
}

async function updateAllPairs() {
    // Update each pair sequentially to avoid rate limiting
    for (const pair of forexPairs) {
        await updateForexData(pair);
    }
}

// Create initial data files
console.log('Creating initial data files...');
await updateAllPairs();

// Update data every second
console.log('Starting live updates...');
while (true) {
    await updateAllPairs();
    await new Promise(resolve => setTimeout(resolve, 1000));
}
