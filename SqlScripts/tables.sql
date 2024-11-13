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
