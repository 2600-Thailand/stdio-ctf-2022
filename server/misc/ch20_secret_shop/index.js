const express = require('express');
const session = require('express-session');
const fs = require('fs');

const app = express();

const items = require('./secret_shop.json');

const item = {
    name: 'Some Item',
    display_name: 'Display Name',
    price: 0.5,
    description: 'This is an item',
    quantity: 1
};

items['aghanim_scepter'] = {
    name: 'aghanim_scepter',
    display_name: "Aghanim\'s Scepter",
    price: 0,
    description: 'Congrat! Summoned flag: ' + fs.readFileSync('flag.txt', 'utf8').trim(),
    quantity: 1
};
app.use(express.static('public')); 
app.use('/images', express.static('images'));

app.use(express.json({ extended: true }));

app.set('view engine', 'ejs');

app.use(session({
    secret: require('crypto').randomBytes(64).toString('hex'),
    resave: false,
    saveUninitialized: true,
}));

app.use((req, res, next) => {
    if (req.session.gold !== undefined)
        return next();

    req.session.gold = 1000;

    if (req.ip == '127.0.0.1') {
        req.session.admin = true;
    }

    next();
});

app.get('/', (req, res) => {
    res.render('index', { items, gold: req.session.gold });
});

app.post('/api/v1/sell', (req, res) => {
    for (const [key, value] of Object.entries(req.body)) {
        if (key === 'aganim_scepter' && !req.session.admin) {
            continue;
        }

        if (!items[key]) {
            items[key] = JSON.parse(JSON.stringify(item));
        }

        for (const [k, v] of Object.entries(value)) {
            if (k === 'quantity') {
                items[key][k] += v;
            } else {
                items[key][k] = v;
            }
        }
    }

    res.send('Sell successful');
});

app.post('/api/v1/buy', (req, res) => {
    const { item, quantity } = req.body;
    if (typeof item === 'undefined' || typeof quantity !== 'number' || quantity <= 0 || !items[item]) {
        return res.status(400).send('Invalid request');
    }

    if (items[item].name == 'aghanim_scepter') {
        if (items["ogre_axe"].quantity == 0 && items["blade_of_alacrity"].quantity == 0 && items["staff_of_wizardry"].quantity == 0 && items["point_booster"].quantity == 0){
            //
        } else {
            return res.status(400).send("You need to have Ogre Axe, Blade of Alacrity, Staff of Wizardry, and Point Booster to build the Aghanim's Scepter");
        }
    }

    if (items[item].quantity >= quantity) {
        if (req.session.gold >= items[item].price * quantity) {
            items[item].quantity -= quantity;
            req.session.gold -= items[item].price * quantity;
            res.json(items[item]);
        } else {
            res.status(402).send('Not enough gold');
        }
    } else {
        res.status(451).send('Not enough item');
    }
});

app.post('/api/v1/whosyordaddy', (req, res) => {
    if (req.session.admin) {
        req.session.gold += req.body.gold;
        res.send('Gold added');
    } else {
        res.status(403).send('Not admin');
    }
});

app.listen(3000, () => {
    console.log('Listening on port 3000');
});
