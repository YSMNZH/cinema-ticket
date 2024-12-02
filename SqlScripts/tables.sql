-- Roles Table
CREATE TABLE Roles (
    RoleID INT PRIMARY KEY,
    RoleName VARCHAR(15) NOT NULL,
    Description TEXT
);

-- Permissions Table
CREATE TABLE Permissions (
    PermissionID INT PRIMARY KEY,
    Action VARCHAR(50) NOT NULL
);

-- RolePermissions Table
CREATE TABLE RolePermissions (
    RoleID INT,
    PermissionID INT,
    PRIMARY KEY (RoleID, PermissionID),
    FOREIGN KEY (RoleID) REFERENCES Roles(RoleID),
    FOREIGN KEY (PermissionID) REFERENCES Permissions(PermissionID)
);

-- Users Table
CREATE TABLE Users (
    UserID INT PRIMARY KEY,
    RoleID INT,
    Name VARCHAR(20) NOT NULL,
    FamilyName VARCHAR(20) NOT NULL,
    BirthDate DATE NOT NULL,
    PhoneNumber VARCHAR(15) NOT NULL UNIQUE,
    Email VARCHAR(255) NOT NULL UNIQUE,
    Password TEXT NOT NULL,
    FOREIGN KEY (RoleID) REFERENCES Roles(RoleID)
);

-- Provinces Table
CREATE TABLE Provinces (
    ProvinceID INT PRIMARY KEY,
    ProvinceName VARCHAR(50) NOT NULL
);

-- Cities Table
CREATE TABLE Cities (
    CityID INT PRIMARY KEY,
    CityName VARCHAR(50) NOT NULL,
    ProvinceID INT,
    FOREIGN KEY (ProvinceID) REFERENCES Provinces(ProvinceID)
);

-- Cinemas Table
CREATE TABLE Cinemas (
    CinemaID INT PRIMARY KEY,
    CinemaName VARCHAR(100) NOT NULL,
    CityID INT,
    ProvinceID INT,
    Address TEXT,
    FOREIGN KEY (CityID) REFERENCES Cities(CityID),
    FOREIGN KEY (ProvinceID) REFERENCES Provinces(ProvinceID)
);

-- Movies Table
CREATE TABLE Movies (
    MovieID INT PRIMARY KEY,
    Title VARCHAR(255) NOT NULL,
    Genre VARCHAR(50) NOT NULL,
    DurationMinutes INT NOT NULL,
    ReleaseDate DATE NOT NULL,
    Rating DECIMAL(2,1)
);

-- Screenings Table (linked to Cinemas)
CREATE TABLE Screenings (
    ScreeningID INT PRIMARY KEY,
    AuditoriumID INT UNIQUE,
    MovieID INT,
    CinemaID INT,
    StartTime DATETIME NOT NULL,
    EndTime DATETIME NOT NULL,
    Capacity INT NOT NULL,
    FOREIGN KEY (MovieID) REFERENCES Movies(MovieID),
    FOREIGN KEY (CinemaID) REFERENCES Cinemas(CinemaID)
);

-- Seats Table
CREATE TABLE Seats (
    SeatID INT PRIMARY KEY,
    AuditoriumID INT,
    FOREIGN KEY (AuditoriumID) REFERENCES Screenings(AuditoriumID)
);

-- Tickets Table
CREATE TABLE Tickets (
    TicketID INT PRIMARY KEY,
    UserID INT,
    SeatID INT,
    Price DECIMAL(10,2) NOT NULL,
    PurchaseDateTime DATETIME NOT NULL,
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (SeatID) REFERENCES Seats(SeatID)
);

-- Reviews Table
CREATE TABLE Reviews (
    ReviewID INT PRIMARY KEY,
    UserID INT,
    MovieID INT,
    Rating DECIMAL(2,1),
    ReviewText TEXT,
    ReviewDate DATETIME,
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (MovieID) REFERENCES Movies(MovieID)
);
CREATE TABLE State (
  StateID SERIAL PRIMARY KEY,
  SName VARCHAR(255) NOT NULL
);

CREATE TABLE City (
  CityID SERIAL PRIMARY KEY,
  CName VARCHAR(255) NOT NULL,
  StateID INT NOT NULL,
  FOREIGN KEY(StateID) REFERENCES State(StateID)
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Administrator (
  AdminID SERIAL PRIMARY KEY,
  FirstName VARCHAR(255) NOT NULL,
  LastName VARCHAR(255) NOT NULL,
  Email VARCHAR(255) UNIQUE,
  Phone VARCHAR(11) UNIQUE,
  CHECK (Email IS NOT NULL OR Phone IS NOT NULL)
);

CREATE TABLE Publisher (
  PubID SERIAL PRIMARY KEY,
  IsActive BOOLEAN DEFAULT TRUE NOT NULL,
  RegDate TIMESTAMP NOT NULL
);

CREATE TABLE NormalUser (
  PubID INT,
  FirstName VARCHAR(255) NOT NULL,
  LastName VARCHAR(255) NOT NULL,
  Email VARCHAR(255) UNIQUE,
  Phone VARCHAR(11) UNIQUE,
  CityID INT NOT NULL,
  CHECK (Email IS NOT NULL OR Phone IS NOT NULL),
  FOREIGN KEY(CityID) REFERENCES City(CityID),
  PRIMARY KEY(PubID),
  FOREIGN KEY(PubID) REFERENCES Publisher(PubID)
    ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE BusinessCategory (
  CatID SERIAL PRIMARY KEY,
  CatName VARCHAR(255) NOT NULL
);

CREATE TABLE Business (
  PubID INT,
  UserID INT,
  BName VARCHAR(255) NOT NULL,
  CatID INT,
  RegistrationNum BIGINT NOT NULL,
  CityID INT NOT NULL,
  FOREIGN KEY(CityID) REFERENCES City(CityID),
  PRIMARY KEY(PubID),
  FOREIGN KEY(PubID) REFERENCES Publisher(PubID)
    ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY(CatID) REFERENCES BusinessCategory(CatID)
);


CREATE TABLE AdCategory (
  CatID SERIAL PRIMARY KEY,
  CatName VARCHAR(255) NOT NULL
);

CREATE TABLE Advertisement (
  AdvertisementID INT,
  PubID INT NOT NULL,
  Title VARCHAR(255) NOT NULL,
  Price INT,
  CreationDate TIMESTAMP NOT NULL,
  CityID INT NOT NULL,
  UpdateDate TIMESTAMP,
  AdDesc VARCHAR(511),
  CatID INT NOT NULL DEFAULT 0,
  PRIMARY KEY(AdvertisementID),
  FOREIGN KEY(PubID) REFERENCES Publisher(PubID)
    ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY(CityID) REFERENCES City(CityID),
  FOREIGN KEY(CatID) REFERENCES AdCategory(CatID)
);


CREATE TABLE StatusState (
  AdStateID SERIAL PRIMARY KEY,
  AdStateName VARCHAR(255) NOT NULL
);

CREATE TABLE AdStatus (
  AdvertisementID INT,
  AdStateID INT NOT NULL DEFAULT 0,
  AdminComment VARCHAR(255),
  UpdatedAt TIMESTAMP,
  PRIMARY KEY(AdvertisementID),
  FOREIGN KEY(AdvertisementID) REFERENCES Advertisement(AdvertisementID)
    ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY(AdStateID) REFERENCES StatusState(AdStateID)
);


CREATE TABLE ReportCategory (
  CatID SERIAL PRIMARY KEY,
  CatName VARCHAR(255) NOT NULL
);

CREATE TABLE Report (
  AdvertisementID INT,
  ReportID INT,
  UserID INT NOT NULL,
  CatID INT,
  RDesc VARCHAR(511),
  PRIMARY KEY(AdvertisementID, ReportID),
  FOREIGN KEY(AdvertisementID) REFERENCES Advertisement(AdvertisementID)
    ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY(UserID) REFERENCES NormalUser(PubID)
    ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY(CatID) REFERENCES ReportCategory(CatID)
);

CREATE TABLE HomeAppliance (
  AdvertisementID INT,
  Brand VARCHAR(255),
  Material VARCHAR(255),
  PRIMARY KEY(AdvertisementID),
  FOREIGN KEY(AdvertisementID) REFERENCES Advertisement(AdvertisementID)
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Vehicle (
  AdvertisementID INT,
  Brand VARCHAR(255),
  ProductionYear INT,
  PRIMARY KEY(AdvertisementID),
  FOREIGN KEY(AdvertisementID) REFERENCES Advertisement(AdvertisementID)
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE RealEstate (
  AdvertisementID INT,
  Area INT,
  ConstructionDate DATE,
  PRIMARY KEY(AdvertisementID),
  FOREIGN KEY(AdvertisementID) REFERENCES Advertisement(AdvertisementID)
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE DigitalProduct (
  AdvertisementID INT,
  Brand VARCHAR(255),
  Model VARCHAR(255),
  PRIMARY KEY(AdvertisementID),
  FOREIGN KEY(AdvertisementID) REFERENCES Advertisement(AdvertisementID)
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Other (
  AdvertisementID INT,
  PRIMARY KEY(AdvertisementID),
  FOREIGN KEY(AdvertisementID) REFERENCES Advertisement(AdvertisementID)
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Visit (
  UserID INT,
  AdvertisementID INT,
  PRIMARY KEY(UserID, AdvertisementID),
  FOREIGN KEY(UserID) REFERENCES NormalUser(PubID),
  FOREIGN KEY(AdvertisementID) REFERENCES Advertisement(AdvertisementID)
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Modified (
  AdminID INT,
  AdvertisementID INT,
  ModDate TIMESTAMP,
  ToStateID INT, 
  PRIMARY KEY(AdminID, AdvertisementID, ModDate),
  FOREIGN KEY(AdminID) REFERENCES Administrator(AdminID),
  FOREIGN KEY(AdvertisementID) REFERENCES Advertisement(AdvertisementID)
    ON DELETE CASCADE ON UPDATE CASCADE
);


INSERT INTO AdCategory(CatID, CatName) VALUES (0, 'Other');
INSERT INTO AdCategory(CatID, CatName) VALUES (1, 'HomeAppliance');
INSERT INTO AdCategory(CatID, CatName) VALUES (2, 'Vehicle');
INSERT INTO AdCategory(CatID, CatName) VALUES (3, 'RealState');
INSERT INTO AdCategory(CatID, CatName) VALUES (4, 'DigitalProduct');

INSERT INTO StatusState(AdStateID, AdStateName) VALUES (0, 'PENDING');
INSERT INTO StatusState(AdStateID, AdStateName) VALUES (1, 'ACCEPTED');
INSERT INTO StatusState(AdStateID, AdStateName) VALUES (2, 'REJECTED');

INSERT INTO ReportCategory(CatID, CatName) VALUES (0, 'Offensive');
INSERT INTO ReportCategory(CatID, CatName) VALUES (1, 'Violence');
INSERT INTO ReportCategory(CatID, CatName) VALUES (2, 'Not Accurate');
INSERT INTO ReportCategory(CatID, CatName) VALUES (3, 'Bad Word');
INSERT INTO ReportCategory(CatID, CatName) VALUES (4, 'Not Good');

INSERT INTO BusinessCategory(CatID, CatName) VALUES (0, 'Electronics');
INSERT INTO BusinessCategory(CatID, CatName) VALUES (1, 'Jewelry');
INSERT INTO BusinessCategory(CatID, CatName) VALUES (2, 'Toys');
INSERT INTO BusinessCategory(CatID, CatName) VALUES (3, 'Music');
INSERT INTO BusinessCategory(CatID, CatName) VALUES (4, 'Tools');
INSERT INTO BusinessCategory(CatID, CatName) VALUES (5, 'Clothing');
INSERT INTO BusinessCategory(CatID, CatName) VALUES (6, 'Sports');
