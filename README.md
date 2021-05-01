# The E-Receipt Project 
The idea behind the E-Receipt project is to use tech to come up with various paperless solutions to display receipts for both cash and cashless payment on a point of sales system or self-service kiosk.

### API
```
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{
    "retailer": "H&M Hennes & Mauritz Pte Ltd"
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
    "paymentMethod": "cash",
    "received": 20,
    "change": 0.85,
    "refund_policy": "Exchange and refund within 30 days with original receipt and price tag."
} ' \
  http://domainnametobeconfirmed/api
```