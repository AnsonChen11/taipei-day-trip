![image](https://user-images.githubusercontent.com/110713031/224562536-ee13d036-b8c4-47fa-996e-3644ced418e8.png)

# Taipei-Day-Trip
Taipei-Day-Trip is a travel e-commerce website that allows users to browse or search for and order their preferred Taipei day trip itinerary.

- Website URL: <a>http://18.180.127.17:3000/</a>

- Test account: 123@gmail.com

- Test password: 123123

- Test Credit Card Infomation: 
  - Credit Card number（卡片號碼）: 4242 4242 4242 4242
  - Credit Card Expiration Dates （過期時間）: 02/42
  - Credit Card CCV Code （驗證密碼）: 424

# Demo

# Table of Contents
- [Main Features](#main-features)
- [Backend Technique](#backend-technique)
  - [Key Points](#key-points)
  - [Environment / Web Framework](#environment--web-framework)
  - [AWS Cloud Service](#aws-cloud-service)
  - [Database](#database)
  - [Networking](#networking)
  - [Third Party Library](#third-party-library)
  - [Version Control](#version-control)
- [System Architecture](#system-architecture)
- [Database Schema](#database-schema)
- [Frontend Technique](#frontend-technique)
- [API Doc](#api-doc)
- [Contact](#contact)

## Main Features

- Membership System 
  - Registration and login fields use regular expression validation to ensure data format correctness.
  - Member verification uses JSON Web Tokens.
  - View order history.
- Attraction
  - Use keywords to find related attractions.
  - Implement infinite scroll to load more attractions.
  - Implement carousel effect for attraction images.
- Order and payment
  - Shopping cart system for adding, removing, and managing items.
  - Integrate third-party payment service [TapPaySDK](https://www.tappaysdk.com/en).

## Backend Technique

#### Key Points
- JWT authentication
- Third-party Payment Service
- MVC Pattern

#### Environment / Web Framework
- Python / Flask

#### AWS Cloud Service
- EC2
- S3
- CloudFront

#### Database
- MySQL

#### Networking
- HTTP

#### Third Party Library
- bcrypt

#### Version Control
- Git/GitHub


## System Architecture
![TaipeiDayTrip Architecture](https://user-images.githubusercontent.com/110713031/224564857-6ccd72ad-7bb3-4751-81df-364373908ea7.jpeg)




## Database Schema
![Taipei Schema](https://user-images.githubusercontent.com/110713031/224561943-872c65b6-21e1-4cf7-b425-fadf9ad30d49.png)


## Frontend Technique

- HTML
- JavaScript
- CSS
- RWD
- AJAX

## API Doc

- [Link](https://app.swaggerhub.com/apis-docs/AnsonChen11/team-talk/1.0.0#/)

## Figma Doc

- [Link](https://www.figma.com/file/MZkYBH31H5gyLoZoZq116j)
## Contact

- Developer: Hungwei, Chen (Anson Chen)

- Email: ab67325@gmail.com

- LinkedIn: [AnsonChen](https://www.linkedin.com/in/anson-chen-b773b316b/)
