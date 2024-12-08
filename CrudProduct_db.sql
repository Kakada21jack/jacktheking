CREATE DATABASE Crudproduct_db;
USE Crudproduct_db;  

CREATE TABLE Product (  
    Id INT AUTO_INCREMENT PRIMARY KEY,  
    Name VARCHAR(255) NOT NULL,  
    Cost DOUBLE(10,2) NOT NULL,  
    Price DOUBLE(10,2) NOT NULL  
);