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
	"login": "thiago222",
	"password": "12345",
	"cpf": "17539433027",
	"email": "thiago245@gmail.com",
	"phone": "5562980078265",
	"cnpj": "07653804000139",
	"date": "1999-04-20"
} 
```
<br />

* CreateToken

`POST in http://localhost:5000/accounts/login?login=thiago222`

Headers: "password": "12345"

<br />

then will return:

```
{
	"token": "eyJ0eXAiOiJKV1QiLCJ_example"
}
```

<br />
<br />

* GetAccount

`GET in http://localhost:5000/accounts`

Headers: "token": "eyJ0eXAiOiJKV1QiLCJ_example"
<br />
<br />
* UpdateAccount

`PUT in http://localhost:5000/accounts`

Headers: "token": "eyJ0eXAiOiJKV1QiLCJ_example"

```
{
	"login": "thiago4444",
	"password": "12345",
	"cpf": "17539433027",
	"email": "thiago245@gmail.com",
	"phone": "5562980078265",
	"cnpj": "07653804000139",
	"date": "1999-04-20"
} 
```
<br />

* DeleteAccount

`DELETE in http://localhost:5000/accounts`

Headers: "token": "eyJ0eXAiOiJKV1QiLCJ_example"

