### Note - 
1. Json schema validation used to validate the input json <a href="https://json-schema.org/understanding-json-schema/">reference</a>
2. Email account config is required to send email, gmail only, please turn on the less secure app <a href="https://accounts.google.com/signin/v2/identifier?service=accountsettings&passive=1209600&osid=1&continue=https%3A%2F%2Fmyaccount.google.com%2Flesssecureapps&followup=https%3A%2F%2Fmyaccount.google.com%2Flesssecureapps&emr=1&mrp=security&rart=ANgoxcfVG6bOANz8k6VQg5AEuKfs_1skL09Z0q6ZSugEonRMqIzRgGYNBz0QXAJn7mGji7hJ7JsrvwAwbasjt14Os9HqdNs-xA&flowName=GlifWebSignIn&flowEntry=ServiceLogin">click here</a> after login.


export EMAIL_HOST_USER="xxxx@gmail.com"  <br>
export EMAIL_HOST_PASSWORD="xxxxxxxx"


#### Add user -
URL - /api/user/
HTTP method POST 

```
{
	"email_id": "thisisprabin@gmail.com",
	"first_name": "Prabin",
	"last_name": "Pramanik"
}
```
<br>

#### List user -
URL - /api/user/
HTTP method GET
<br>


#### Deposit Amount -
URL - /api/deposit/
HTTP method POST

```
{
	"user_id": 1,
	"account_number": 1614842576,
	"amount": 12
}
```
<br>


#### Withdraw Amount -
URL - /api/withdraw/
HTTP method POST

```
{
	"user_id": 1,
	"account_number": 1614842576,
	"amount": 12
}
```
<br>

#### Enquiry Amount -
URL - /api/enquiry/
HTTP method POST

```
{
	"user_id": 1,
	"account_number": 1614842576
}
```
<br>

#### Download transaction record -
URL - /api/download-transaction-record/
HTTP method POST

```
{
	"account_number": 1614842576
}
```












