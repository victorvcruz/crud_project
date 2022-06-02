To run project you need Python, Pip, [Docker](https://docs.docker.com/engine/install/) and [Docker-compose](https://docs.docker.com/compose/install/),  installed in your pc

## How to run project

1. run `sudo docker-compose up -d` in root directory
2. run `pip install -r requirements.txt` in root directory
3. run main.py
4. in http://localhost:5000/accounts insert your request

To stop execution run `sudo docker-compose down`

### Application of the requisition

* CreateAccount

`POST in http://localhost:5000/accounts`

```
{
	"login": (your login),
	"password": (your password),
	"cpf": (your cpf),
	"email": (your email),
	"phone": (your phone),
	"cnpj": (your cnpj),
	"date": (your birth date)
} 
```
<br />

* CreateToken

`POST in http://localhost:5000/accounts/login?login=(your login)`

in the "password" header put your password
<br />
<br />
* GetAccount

`GET in http://localhost:5000/accounts`

in the "token" header put your token
<br />
<br />
* UpdateAccount

`PUT in http://localhost:5000/accounts`

in the "token" header put your token

```
{
	"login": (your login),
	"password": (your password),
	"cpf": (your cpf),
	"email": (your email),
	"phone": (your phone),
	"cnpj": (your cnpj),
	"date": (your birth date)
} 
```
<br />
* DeleteAccount

`DELETE in http://localhost:5000/accounts`

in the "token" header put your token

