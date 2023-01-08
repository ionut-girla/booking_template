#SOURCE D:/FACULTATE/AN 4/SEM 1/BD/Proiect/script12.sql
/*          Folositi pentru cale simbolul "/", NU "\"         */ 


/*#############################################################*/
/*        PARTEA 1 - STERGEREA SI RECREAREA BAZEI DE DATE      */

CREATE DATABASE bookingDB;
USE bookingDB;

/*#############################################################*/




/*#############################################################*/
/*                  PARTEA 2 - CREAREA TABELELOR              */

CREATE TABLE tblClienti(
    idClient SMALLINT(5) PRIMARY KEY AUTO_INCREMENT,
    nume VARCHAR(30) NOT NULL,
    prenume VARCHAR(30) NOT NULL,
    cnp CHAR(13) NOT NULL UNIQUE,
    nrTelefon VARCHAR(15) NOT NULL UNIQUE,
    judet VARCHAR(30) NOT NULL,
    localitate VARCHAR (30) NOT NULL
    );
    
CREATE TABLE tblRezervare(
    idRezervare SMALLINT(5) PRIMARY KEY AUTO_INCREMENT,
    codClient SMALLINT(5),
    dataCheckin DATE NOT NULL,
    dataCheckout DATE NOT NULL,
    nrZile SMALLINT(3) DEFAULT '1',
    CONSTRAINT fk_rezervare FOREIGN KEY (codClient)
    REFERENCES tblClienti(idClient) ON DELETE CASCADE ON UPDATE CASCADE
    );
       
CREATE TABLE tblCamera(
   idCamera SMALLINT(3) PRIMARY KEY AUTO_INCREMENT,
   tipCamera VARCHAR(10),
   descriere VARCHAR(100),
   pretCamera DECIMAL(5,2) NOT NULL
   );

CREATE TABLE tblRezervareCamera(
    idRezervareCamera SMALLINT(3) PRIMARY KEY AUTO_INCREMENT,
    codCamera SMALLINT(3),
    codRezervare SMALLINT(5),    
    nrAdulti TINYINT(2) NOT NULL,
    nrCopii TINYINT(1) DEFAULT '0',   
    CONSTRAINT fk_codCamera FOREIGN KEY (codCamera)
    REFERENCES tblCamera(idCamera) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_codRezervare FOREIGN KEY (codRezervare)
    REFERENCES tblRezervare(idRezervare) ON DELETE CASCADE ON UPDATE CASCADE
    );
	
CREATE TABLE tblFactura(
   idFactura SMALLINT (3) PRIMARY KEY AUTO_INCREMENT,
   codRezervare SMALLINT(5),
   seria VARCHAR(15) NOT NULL UNIQUE,
   dataEmitere DATE NOT NULL,
   tipPlata ENUM("card","cash","tichete"),
   CONSTRAINT fk_factura FOREIGN KEY (codRezervare)
   REFERENCES tblRezervare(idRezervare) ON DELETE CASCADE ON UPDATE CASCADE
   );
   


/*#############################################################*/

ALTER TABLE tblRezervare AUTO_INCREMENT = 100;
ALTER TABLE tblRezervareCamera AUTO_INCREMENT = 200;
ALTER TABLE tblFactura AUTO_INCREMENT = 650;

/*#############################################################*/
/*         PARTEA 3 - INSERAREA INREGISTRARILOR IN TABELE      */

INSERT INTO tblClienti (nume,prenume,cnp,nrTelefon,judet,localitate) VALUES
        
    ("Preda","Valeriu", "1881118250604", "0756268349", "Braila", "Braila"),
    ("Banica", "Camelia", "1931104362705", "0736268549", "Vrancea", "Adjud"),
    ("Popescu", "Ionel", "1990509127825", "0756168300", "Buzau", "Buzau"),
    ("Stanescu", "Alexandru", "5010311048932", "0756228349", "Brasov", "Poiana Brasov"),
    ("Voicu", "Andreea-Valeria", "1930702401785", "0796268341", "Galati", "Galati"),
    ("Munteanu", "Mirela", "1901224145117", "0726268449", "Bucuresti", "Sector 4"),
    ("Popa", "Petre-Gabriel", "1910319314041", "0746248349", "Maramures", "Baia Mare"),
    ("Ardeleanu", "Andrei", "1990828297071", "0755268349", "Bihor", "Beius"),
    ("Cimpeanu", "Mihai", "1890921094508", "0756333349", "Neamt", "Piatra Neamt"),
    ("Badea", "Nicoleta", "1980212256755", "0722268349", "Valcea", "Dragasani");
	
	
INSERT INTO tblRezervare (codClient,dataCheckin,dataCheckout,nrZile) VALUES

    (5,"2022-01-27","2022-01-30",3),
    (2,"2022-03-12","2022-03-19",7),
    (2,"2022-03-22","2022-03-26",4),
    (7,"2022-05-12","2022-05-17",5),
    (9,"2022-05-19","2022-05-25",6),
    (8,"2022-06-05","2022-06-09",4),
	(6,"2022-07-05","2022-07-09",4),
    (10,"2022-10-12","2022-10-22",10),
    (1,"2022-11-10","2022-11-20",10),
    (3,"2022-12-14","2022-12-28",14),
    (4,"2022-12-14","2022-12-28",14);
	
	
INSERT INTO tblCamera (tipCamera,descriere,pretCamera) VALUES

    ("dubla","Camera dubla standard cu un pat dublu",200),
    ("tripla","Camera tripla cu un pat dublu si un pat de persoana",300),
    ("suita","Suita Prestige cu un pat dublu extra-large si o canapea extensibila",449.99),
    ("apartament","Apartament cu doua dormitoare cu vedere la munte",550),
    ("dubla","Camera dubla deluxe cu un pat dublu mare",220),
    ("suita","Suita de lux cu pat matrimonial cu vedere la gradina",599.99),
    ("tripla","Camera tripla cu vedere la gradina",350),
    ("apartament","Apartament cu doua dormitoare cu vedere la gradina",500),
    ("tripla","Camera tripla cu o canapea extensibila cu vedere la munte",400),
    ("apartament","Apartament cu pat dublu si doua paturi de o persoana",450);
	
INSERT INTO tblRezervareCamera (codCamera,codRezervare,nrAdulti,nrCopii) VALUES

    (2,102,2,1), 
    (4,102,2,2),
    (3,103,4,DEFAULT), 
	(1,101,2,DEFAULT), 
    (1,104,2,DEFAULT),
	(8,100,3,1),		
	(6,107,3,1),		
    (8,105,3,1),		
    (5,106,2,DEFAULT),	
    (9,106,0,3),
    (7,106,2,1),
	(3,108,4,1),		
	(4,109,4,DEFAULT);	
	
INSERT INTO tblFactura (codRezervare,seria,dataEmitere,tipPlata) VALUES
    (100,"85324","2022-01-30","card"),
    (101,"85325","2022-03-19","cash"),
    (102,"85326","2022-03-26","card"),
    (103,"85327","2022-05-17","tichete"),
    (104,"85328","2022-05-25","cash"),
    (105,"85329","2022-06-09","cash"),
	(106,"853210","2022-10-22","card"),
	(107,"853211","2022-11-20","tichete"),
	(108,"853212","2022-12-28","card"),
	(109,"853213","2022-12-28","card");
	(110,"853214","2022-12-28","card");
/*#############################################################*/



/*#############################################################*/
/*  PARTEA 4 - VIZUALIZAREA STUCTURII BD SI A INREGISTRARILOR  */
SHOW TABLES;
DESCRIBE tblClienti;
DESCRIBE tblRezervare;
DESCRIBE tblCamera;
DESCRIBE tblRezervareCamera;
DESCRIBE tblFactura;


SELECT * FROM tblClienti;
SELECT * FROM tblRezervare;
SELECT * FROM tblRezervareCamera;
SELECT * FROM tblCamera;
SELECT * FROM tblFactura;
/*#############################################################*/




/* 
- REDENUMITI FISIERUL  scriptXX.sql astfel incat XX sa coincida cu numarul echipei de BD. Ex: script07.sql

- SCRIPTUL AR TREBUI SA POATA FI RULAT FARA NICI O EROARE!

- ATENTIE LA CHEILE STRAINE! Nu uitati sa modificati motorul de stocare pentru tabele, la InnoDB, pentru a functiona constrangerile de cheie straina (vezi laborator 1, pagina 16 - Observatie)

*/