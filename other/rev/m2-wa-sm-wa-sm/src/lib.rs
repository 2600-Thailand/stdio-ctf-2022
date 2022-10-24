mod utils;
use md5;

use wasm_bindgen::prelude::*;

// When the `wee_alloc` feature is enabled, use `wee_alloc` as the global
// allocator.
#[cfg(feature = "wee_alloc")]
#[global_allocator]
static ALLOC: wee_alloc::WeeAlloc = wee_alloc::WeeAlloc::INIT;

#[wasm_bindgen]
extern {
    fn alert(s: &str);
}

#[wasm_bindgen]
pub fn check_secret(secret: &str) -> bool {
    let mut checker = Vec::new();
    checker.push("5dbc98dcc9");
    checker.push("4c614360da");
    checker.push("8006189430");
    checker.push("d20caec3b4");
    checker.push("5dbc98dcc9");
    checker.push("1679091c5a");
    checker.push("1679091c5a");
    checker.push("592eec8d32");
    checker.push("7b8b965ad4");
    checker.push("2db95e8e1a");
    checker.push("6f8f577150");
    checker.push("9eecb7db59");
    checker.push("7fc56270e7");
    checker.push("0d61f8370c");
    checker.push("8006189430");
    checker.push("83878c9117");
    checker.push("3a3ea00cfc");
    checker.push("4b43b0aee3");
    checker.push("e358efa489");
    checker.push("f1290186a5");
    checker.push("a5f3c6a11b");
    checker.push("4152907695");
    checker.push("69691c7bdc");
    checker.push("fbade9e36a");
    checker.push("ff44570aca");
    checker.push("e1e1d3d405");
    checker.push("4c761f170e");
    checker.push("e1e1d3d405");
    checker.push("4c614360da");
    checker.push("4c614360da");
    checker.push("ec631d7335");
    checker.push("ec631d7335");
    checker.push("a03920e599");
    checker.push("61e9c06ea9");
    checker.push("dcaba5d0e9");
    checker.push("dcaba5d0e9");
    checker.push("21c2e59531");
    checker.push("7e6a2afe55");
    checker.push("2854272fec");
    checker.push("833344d5e1");
    checker.push("ab3af8566d");

    if checker.len() != secret.len() {
        return false;
    }

    for (i, &s) in secret.as_bytes().iter().enumerate() {
        let digest = md5::compute([s+(i as u8)]);
        let hash = format!("{:x}", digest);
        if hash[..10] != *checker[i] {
            return false;
        }
    }
    return true;
}
