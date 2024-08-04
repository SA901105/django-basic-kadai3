/*
    Send a request to the view, create a session in Stripe on the Django side, 
    and query Stripe based on that session.
*/

// Get Stripe publishable key
fetch("/subscription/config/")
    // Get result object 
    .then((result) => { return result.json(); })
    // Get data object 
    .then((data) => {
        // Initialize Stripe.js
        const stripe = Stripe(data.publicKey);

        // Event handler
        let submitBtn = document.querySelector("#checkout");
        if (submitBtn !== null) {
            // When submitBtn was clicked
            submitBtn.addEventListener("click", () => {
                // Get Checkout Session ID
                fetch("/subscription/create-checkout-session/")
                    // Get result object 
                    .then((result) => { return result.json(); })
                    // Get data object 
                    .then((data) => {
                        console.log(data);
                        // Redirect to Stripe Checkout
                        return stripe.redirectToCheckout({ sessionId: data.sessionId })
                    })
                    .then((res) => {
                        console.log(res);
                    })
                    .catch(error => {
                        const message = 'StripeXXXXX'; // エラーメッセージ内容
                        document.getElementById('stripe-error').innerHTML = message;
                        console.error(message, error);
                    });
            });
        }
    })
    // Error handling
    .catch(error => {
        const message = 'StripeXXXXX'; // エラーメッセージ内容
        document.getElementById('stripe-error').innerHTML = message;
        console.error(message, error);
    });
