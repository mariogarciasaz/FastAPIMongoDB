# FastAPI  - MongoDB


#### This API is a personal project

------------

**ATTENTION: TO RUN THIS API, YOU MUST HAVE A MONGODB DATABASE AND CONFIGURE DB.PY FILE WITH YOUR DATA CONNECTION**

------------



This API was made with FastAPI framework and MongoDB. It has 3 branches: Users, Clients and Products.

To use this API you need to be registered and logged in.

**User Branch**: This branch contains all users that can interact with the API(in this case a user is like an employee).
A user has the following keys:


- ***ID***:  auto-generated alphanumeric value.
- ***Username***: String value.
- ***Name***: String value.
- ***Email***: String value.
- ***Disabled***: Boolean value (If a user has the key value as "true", this user can't interact with the API).
- ***Password***: Encrypted string value.
- ***Role***: String value. There are 3 different roles: *"Admin"*, *"Read"* and *"Write"*:
	- ***Admin Role***: This role is used to manage all API branches(Create, modify and delete).
	- ***Read Role***: This role is used to get data from the Client and Product Branches.
	- ***Write Role***: This role is used to create, modify and delete records in the Client and Product Branches

**Client Branch**: This branch contains all clients.

A client has the following keys:


- ***ID***:  auto-generated alphanumeric value.
- ***Name***: String value.
- ***Lastname***: String value.
- ***Address***: String value.
- ***Phone***: String value.
- ***Email***: String value.

**Product branch**: This branch contains all products.

A product has the following keys:

- ***ID***:  auto-generated alphanumeric value.
- ***Name***: String value.
- ***Category***: String value.
- ***Price***: Float value.
- ***Stock***: Integer value.


The authentication method was developed with **JWT**(JSON Web Token). If you don't have a token, you will not be able to login on API.
To get a token, you must request one through the form with your username and password.


You will receive an HTTP Response with a token to interact with the API.

The duration of the token is 10 minutes, and after you must request a new token by following the last step.

 You can review the API methods in  /docs URL(Ex: http://localhost/docs)
