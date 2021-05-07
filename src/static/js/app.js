function GenerateReceipt(){

    receipt_data = {
        "retailer": "H&M Hennes & Mauritz Pte Ltd",
        "address" : "JEM, Jurong Gateway Road #01-01 Singapore 608549",
        "gst_reg_no" : "M93217469R",
        "cashier_id" : 2729,
        "transaction_id" : 767664,
        "timestamp" : "05/02/2016 13:38:00",
        "products": [
            {
                "name": "Soap", 
                "qty": 2, 
                "price": 6.25, 
                "total": 12.50
            },
            {
                "name": "Cookies", 
                "qty": 1, 
                "price": 5.40, 
                "total": 5.40
            }
        ],
        "subtotal": 17.90,
        "gst": 1.25,
        "total": 19.15,
        "payment_method": "cash",
        "received": 20,
        "change": 0.85,
        "refund_policy": "Exchange and refund within 30 days with original receipt and price tag."
    }

    axios.post('/api', receipt_data)
        .then((response)=>{
            var file = new Blob([response.data], { type: 'application/pdf' });
            var fileURL = URL.createObjectURL(file);
            window.open(fileURL, '_blank'); // Does not work on Safari
        },
        (error) => { 
            console.log(error) 
    });
    
}