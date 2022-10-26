const express = require("express");
const coupons = require('../utils/coupon.json');
const products = require('../utils/product.json');


const router = express.Router();

let tmp = {};
router.use((req, res, next) => {
    res.setHeader("Cache-Control", "no-store, no-cache");
    tmp[req.sessionID] = tmp[req.sessionID] || [];
    next();
});



router.post('/coupon/claim/', async (req, res) => {
    let code = req.body.promocode;
    let session = req.session;
    const valid = await isValid(code);
    if (!valid) return res.json({ success: false, message: "Fully claimed or invalid." });
    const claimed = await isClaimed(code, session);
    if (claimed) return res.json({ success: false, message: "You already claim this coupon" });
    await addCouponAmount(code, 1, session, req.sessionID);
    
    await updateCouponStatus(code, true, session);
    return res.json({ success: true, message: "Successfully Claimed." });

});

router.post('/coupon/apply/', async (req, res) => {
    let appliedCoupon = req.body.coupons;
    let userCoupons = req.session.coupon || [];
    let session = req.session;
    const valid = await isValid(appliedCoupon);
    if (!valid) return res.json({ success: false, message: "Invalid Coupon." });
    const claimed = await isClaimed(appliedCoupon, session);
    if (!claimed) return res.json({ success: false, message: "Please claim coupon before use." });

    let data = userCoupons.find(coupon => coupon.code === appliedCoupon);
    if (!data) return res.json({success: false, message: "Invalid."});

    return res.json({success: true, coupon: data});
});

router.delete('/removeAllCoupon', async (req, res) => {
    req.session.coupon = [];
    tmp[req.sessionID] = [];
    // req.session.destroy();
    // res.clearCookie("connect.sid");
    return res.json({success: true});
});

router.delete('/coupon/:code', async (req, res) => {
    let code = req.params.code;
    tmp[req.sessionID] = [];
    req.session.coupon = req.session.coupon.filter(obj => obj.code !== code);
    return res.json({data: req.session.coupon});
});

router.post('/checkout/:id', async (req, res) => {
    let promocodes = req.body.coupons || [];
    let session = req.session.coupon || [];
    const promocode_count = {};

    promocodes.forEach(e => {
        promocode_count[e] = (promocode_count[e] || 0) + 1;
    });
    let checkIsEnoughCoupon = session.length && session.every((coupon) => {
        return coupon.amount >= promocode_count[coupon.code]
    })
    if (!checkIsEnoughCoupon) return res.json({success: false, message: "Something went wrong!"});
    
    let discount = promocodes.map(code => {
        return coupons["coupons"].find(x => x.code === code)?.value
    }).reduce((a, b) => a + b, 0);


    let productId = req.params.id;
    let productDetails = products["products"].find(x => x.id === productId);
    if (discount >= productDetails.price) {
        let msg = process.env.FLAG || "FLAG is here.";
        return res.json({success: true, product: productDetails, flag: msg});
    }
    return res.json({success: false, message: "Insufficient Balance."});
});

async function isValid(code) {
    let coupon = coupons["coupons"].find(x => x.code === code);
    if (!coupon) return false;
    return coupon.status;
}

async function isClaimed(code, session) {
    let userCoupons = session.coupon || [];
    let data = userCoupons.find(coupon => coupon.code === code);
    if (data) return true;
    return false;
}

async function addCouponAmount(code, addAmount, session, id) {
    //await Delay(); // For test purpose.
    const coupon = coupons["coupons"].find(x => x.code === code);
    const index = tmp[id].findIndex(e => e.code === code) > -1;
    
    if (!index) {
        tmp[id].push({ ...coupon, amount: addAmount });
        session.coupon = tmp[id]; 
        return;
    }
    session.coupon = tmp[id].map(x => (x.code === code ? { ...x, amount: (x.amount >=0 ? x.amount += addAmount : 1) } : x));
    return;
}

async function updateCouponStatus(code, status, session) {
    let userCoupons = session.coupon || [];
    let coupon = userCoupons.find(x => x.code === code);
    if (!coupon) return false;
    newCoupon = [{...coupon, claimed: status}]
    session.coupon = userCoupons.map(obj => newCoupon.find(o => o.code === obj.code) || obj);
    return true;
}


module.exports = router;