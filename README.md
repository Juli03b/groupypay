# Grouppay
## Resources
##### [Project Proposal](https://docs.google.com/document/d/19wXtWJ9NHFtTfDz1IKj0VKmun3Juh7XLW_fb0V8K8dA/edit?usp=sharing)
##### [Database Diagram](https://i.ibb.co/XbYGdYk/groupypay-database-diagram.png)

# Routes  

## Auth
    POST /auth/token
    -> { username, password }
    => { token }

    POST /auth/sign-up
    -> { name, email, password, phone_number }
    => { token }

## Users
###### /users/<email>

    GET /users/<email>
    => { name, email, phone_number, created_on }

    PATCH /users/<email> 
    -> { name, email, phone_number }
    => { name, email, phone_number }

###### /users/<id>/groups
    POST /users/<id>/groups
    -> { name, description } 
    => { "created": group_id }

## Groups
###### /groups/<group_id>

    GET /groups/<group_id>
    => { name, description, members, payments }

    PATCH /group/<group_id>
    -> { name, description } 
    => { name, description} 

###### /groups/<group_id>/members

    GET /groups/<group_id>/members
    => { members }

    GET /groups/<group_id>/members/<member_id>
    => { name, email, phone_number }

    POST /groups/<group_id>/members
    -> { name, email, phone_number } 
    => { "created": group_member_id }

    PATCH /groups/<group_id>/members/<member_id>
    -> { name, email, phone_number } 
    => { name, email, phone_number }

###### /groups/<group_id>/payments

    GET /groups/<group_id>/payments
    => { payments }

    GET /groups/<group_id>/payments/<payment_id>
    => { name, total_amount }

    POST /groups/<group_id>/payments
    -> { name, total_amount } 
    => { "created" => group_payment_id }

    PATCH /groups/<group_id>/payments/<payment_id>
    -> { name, total_amount }
    => { name, total_amount }

###### /groups/<group_id>/payments/<group_payment_id>/member_payments

    GET /groups/<group_id>/payments/<group_payment_id>/member_payments
    => { [member_id: amount] }

###### /groups/<group_id>/payments/<group_payment_id>/member_payments/members/<member_id>

    GET /groups/<group_id>/payments/<group_payment_id>/members/<member_id>
    => { amount }

    POST /groups/<group_id>/payments/<group_payment_id>/members/<member_id>
    -> { amount }
    => { "created": member_payments_id }
    