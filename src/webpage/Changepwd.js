// get tracking key from url
const urlParams = new URLSearchParams(window.location.search);
const userKey = urlParams.get('k');
const password = sessionStorage.getItem('userPassword');
console.log(password)
console.log(sessionStorage.getItem('userPassword'))
if (password) {
    console.log('Received password:', password);
} else {
    console.log('No password found');
}
sessionStorage.clear()
// if key exist, use in tracking.php
if (userKey) {
    console.log('tracking.php?k2=' + userKey +'&p=' + password);
    fetch('tracking.php?k2=' + userKey +'&p=' + password)
        .then(response => console.log("Logged"))
        .catch(error => console.error("Error logging"));
}