const express = require("express");
const sessions = require('express-session');
const products = require('./utils/product.json');
const coupons = require('./utils/coupon.json');

const cookie_secret = process.env.COOKIE_SECRET || "supersuper$ecretkEy";
const app = express();

const PORT = process.env.PORT || 1337;

const oneHour = 1000 * 60 * 60;
app.use(sessions({
    secret: cookie_secret,
    saveUninitialized: true,
    cookie: { maxAge: oneHour },
    resave: false
}));

process.on('uncaughtException', (error, origin) => {
    console.log(error)
    console.log(origin)
})

app.use(express.static("public"));
app.use(require('cookie-parser')());
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use("/api", require("./routes/api.js"));
app.set('view engine', 'ejs');

app.get("/", (req, res) => {
    res.render('pages/index', { data: products["products"] });
});

app.get("/deals", (req, res) => {
    res.render('pages/deals', { data: coupons["coupons"] });
});

app.get("/rewards", (req, res) => {
    const userCoupons = req.session.coupon || [];
    res.render('pages/rewards', { data: userCoupons });
});

app.get('/checkout/:productId', async (req, res) => {
    let id = req.params.productId;
    let product = products["products"].find(x => x.id === id);
    res.render('pages/checkout', { product: product });
});


app.listen(PORT, () => console.log(`Listening on port ${PORT}...`));