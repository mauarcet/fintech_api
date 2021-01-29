## Fintech API

This API provides a service that allows the registration of users' transactions to have an overview of their economic behavior.
It's constructed under the Django Rest Framework.

### Installation

This project comes with a Docker recipe. `docker-compose` and `Docker` are required for the installation.

Clone the project

```
git clone https://github.com/mauarcet/fintech_api.git
cd fintech_api
```

From the command line run:

```
docker-compose up
```

### Tests

In order to run the test suite kill the server with: `Ctrl+c`
From the command line:

```
docker-compose run --service-ports web python fintech_api/manage.py test users_transactions
```

### Usage

The following is a description of the objects used in the API and the endpoints available.

**User**
The `User` object allows you to register the users you want to register transactions and overview their economic behavior.

| Parameter                 | Description       |
| ------------------------- | ----------------- |
| name: string (required)   | Name of the user  |
| age: integer (required)   | Age of the user   |
| email: string (required)  | Email of the user |

Endpoints
`POST /users/:id`
`GET /users/:id`
`PUT /users/:id`
`DELETE /users/:id`
`GET /users/`

Example

```
curl --location --request POST 'http://127.0.0.1:8000/users/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "Dan Cooper",
    "age": 32,
    "email": "d_b_cooper@gmail.com"
}'
```

**Transaction**
Represents the money movement realized by the user.
Bulk transaction creation is featured.
| Parameter | Description |
|-----------|-------------|
| reference: string (required) | Unique reference to identify the transaction.|
| account: string (required) | Name of the account this transaction was made from.|
| date: date (required) | Date when the transaction was made. Format: "YYYY-MM-DD"|
| amount: integer (required) | Amount of the transaction, positive numbers when receiving money and negative when spending money.|
| type: string (required) | Inflow when it's a positive amount of money and outflow when is negative.|
| category: string (required) | Category where the transaction falls|
| user_id: integer (required) | Unique identifier of the user that made the transaction|

Endpoints
`POST /transactions/`
`GET /transactions/:id`
`PUT /transactions/:id`
`DELETE /transactions/:id`
`GET /transactions/`

Example

```
curl --location --request POST 'http://127.0.0.1:8000/transactions/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "reference": "0140900",
    "account": "BBVA",
    "date": "2021-01-27",
    "amount": "-150.72",
    "type": "outflow",
    "category": "transfer",
    "user_id": 3
}'
```

**User Transaction**
The following endpoint is useful for data insights on the user.
They provide summaries for inflow and outflow transactions as well as category type transactions.
All the query params are optional, when no parameter is sent the endpoint will return the transactions made by the specified user.
Types of user transactions summary:
Category. It shows a summary of the transactions ordered by category.

```
{"inflow": {"salary": "2500.72", "savings": "150.72"}, "outflow": {"groceries": "-51.13", "rent": "-560.00", "transfer": "-150.72"}}
```

Account. It shows a summary of the transactions by account.

```
[
 {"account": "C00099", "balance": "1738.87", "total_inflow": "2500.72", "total_outflow": "-761.85"},
 {"account": "S00012", "balance": "150.72", "total_inflow": "150.72", "total_outflow": "0.00"},
]
```

Endpoint
`GET users/:id/transactions`

Query params
| Parameter | Description |
|-----------|-------------|
| start_date | Retrieve all transactions after this date |
| end_date | Retrieve all transactions before this date |
| type | Defines the type of user transaction summary to make: category or account|

Account query example

```
curl --location --request GET 'http://127.0.0.1:8000/users/3/transactions?start_date=2021-01-26&end_date=2021-01-28&type=account' \
--data-raw ''
```

Category query example

```
curl --location --request GET 'http://127.0.0.1:8000/users/3/transactions?start_date=2021-01-26&end_date=2021-01-28&type=category' \
--data-raw ''
```

---

**Technical Debt**
Due to time constraints some technical debt is left in this application:

- Different env handling is not available.

- Current configuration is not suited for production.

- Security is not fully assured.

- More detailed error responses are required

- The Date format on the requirements is not optimal, I would prefered to use a timestamp instead. As this product is intended for other developers, unix timestamp is a better fit for the communication between systems.

- Reference shouldn't be provided by the user. The requirements specified that the reference was provided by the user, but this could be saved as another variable and use a UUID as the primary key for the object.

- Create validations for query params.

- Refactor Views to use decorator `@api_view`. I used a shortcut for the views on main models.

- Tests only cover main models. A more complete test suite is required.
