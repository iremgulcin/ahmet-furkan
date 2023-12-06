-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Anamakine: 127.0.0.1
-- Üretim Zamanı: 06 Ara 2023, 21:59:03
-- Sunucu sürümü: 10.4.28-MariaDB
-- PHP Sürümü: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Veritabanı: `yz_nabiz`
--

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `appointments`
--

CREATE TABLE `appointments` (
  `ID` int(11) NOT NULL,
  `PatientTC` varchar(11) DEFAULT NULL,
  `DoctorTC` varchar(11) DEFAULT NULL,
  `AppointmentDate` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Tablo döküm verisi `appointments`
--

INSERT INTO `appointments` (`ID`, `PatientTC`, `DoctorTC`, `AppointmentDate`) VALUES
(1, '11111111111', '22222222221', '2023-07-01 10:00:00'),
(2, '11111111112', '22222222221', '2023-07-02 14:00:00'),
(3, '11111111113', '22222222223', '2023-07-03 09:00:00');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `doctors`
--

CREATE TABLE `doctors` (
  `ID` int(11) NOT NULL,
  `TCNumber` varchar(11) DEFAULT NULL,
  `FirstName` varchar(100) DEFAULT NULL,
  `LastName` varchar(100) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `Password` varchar(100) DEFAULT NULL,
  `Specialty` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Tablo döküm verisi `doctors`
--

INSERT INTO `doctors` (`ID`, `TCNumber`, `FirstName`, `LastName`, `Email`, `Password`, `Specialty`) VALUES
(1, '22222222221', 'Hasan', 'Duran', 'hasan@mail.com', '$5$rounds=535000$0fXZxckgqyGvB.gp$YDtNq32Kjhj6BqxL1.zvLyGuJ44WflpBkw2008AA20D', 'Cardiology'),
(2, '22222222222', 'Elif', 'Öztürk', 'elif@mail.com', '$5$rounds=535000$0fXZxckgqyGvB.gp$YDtNq32Kjhj6BqxL1.zvLyGuJ44WflpBkw2008AA20D', 'Dermatology'),
(3, '22222222223', 'Fatma', 'Demir', 'fatma@mail.com', '$5$rounds=535000$0fXZxckgqyGvB.gp$YDtNq32Kjhj6BqxL1.zvLyGuJ44WflpBkw2008AA20D', 'Neurology');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `hospitalvisits`
--

CREATE TABLE `hospitalvisits` (
  `ID` int(11) NOT NULL,
  `PatientTC` varchar(11) DEFAULT NULL,
  `VisitDateTime` datetime DEFAULT NULL,
  `Reason` varchar(500) DEFAULT NULL,
  `DoctorTC` varchar(11) DEFAULT NULL,
  `Notes` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Tablo döküm verisi `hospitalvisits`
--

INSERT INTO `hospitalvisits` (`ID`, `PatientTC`, `VisitDateTime`, `Reason`, `DoctorTC`, `Notes`) VALUES
(1, '11111111111', '2023-06-20 10:00:00', 'Rutin Kontrol', '22222222221', NULL),
(2, '11111111111', '2023-06-15 14:00:00', 'Deri Alerjisi', '22222222222', NULL),
(3, '11111111111', '2023-05-05 09:00:00', 'Migren Kontrolü', '22222222223', NULL),
(4, '11111111112', '2023-12-05 19:10:19', 'Göğüs Taraması (Kontrol)', '22222222221', NULL);

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `laboratoryresults`
--

CREATE TABLE `laboratoryresults` (
  `ID` int(11) NOT NULL,
  `PatientTC` varchar(11) DEFAULT NULL,
  `HospitalName` varchar(200) NOT NULL,
  `TestName` varchar(100) DEFAULT NULL,
  `Result` varchar(100) DEFAULT NULL,
  `ResultUnit` varchar(100) NOT NULL,
  `ReferenceValue` varchar(100) NOT NULL,
  `TestDate` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Tablo döküm verisi `laboratoryresults`
--

INSERT INTO `laboratoryresults` (`ID`, `PatientTC`, `HospitalName`, `TestName`, `Result`, `ResultUnit`, `ReferenceValue`, `TestDate`) VALUES
(4, '11111111111', 'BAŞAKŞEHİR ÇAM VE SAKURA ŞEHİR HASTANESİ', 'Troponin T', '4.77', 'pg/mL', '0 - 19.8', '2023-07-02'),
(5, '11111111111', 'BAŞAKŞEHİR ÇAM VE SAKURA ŞEHİR HASTANESİ', 'Alanin aminotransferaz (ALT)', '10', 'U/L', '1 - 50.00', '2023-07-02'),
(6, '11111111111', 'BAŞAKŞEHİR ÇAM VE SAKURA ŞEHİR HASTANESİ', 'Albümin', '4.67', 'g/dL', '3.5 - 5.2', '2023-07-02'),
(7, '11111111111', 'BAŞAKŞEHİR ÇAM VE SAKURA ŞEHİR HASTANESİ', 'Alkalen fosfataz', '94', 'U/L', '30 - 120', '2023-07-02'),
(8, '11111111111', 'BAŞAKŞEHİR ÇAM VE SAKURA ŞEHİR HASTANESİ', 'Amilaz', '89', 'U/L', '28 - 100', '2023-07-02'),
(9, '11111111111', 'BAŞAKŞEHİR ÇAM VE SAKURA ŞEHİR HASTANESİ', 'Aspartat transaminaz (AST)', '13', 'U/L', '1 - 50', '2023-07-02'),
(10, '11111111111', 'BAŞAKŞEHİR ÇAM VE SAKURA ŞEHİR HASTANESİ', 'Bilirubin (Total,direkt), her biri', '0.57', 'mg/dL', '0.3 - 1.2', '2023-07-02'),
(11, '11111111111', 'BAŞAKŞEHİR ÇAM VE SAKURA ŞEHİR HASTANESİ', 'Bilirubin (direk)', '0.22', 'mg/dL', '0.01 - 0.2', '2023-07-02'),
(12, '11111111111', 'BAŞAKŞEHİR ÇAM VE SAKURA ŞEHİR HASTANESİ', 'CRP,türbidimetrik', '2.5', 'mg/L', '0 - 5', '2023-07-02'),
(13, '11111111111', 'BAŞAKŞEHİR ÇAM VE SAKURA ŞEHİR HASTANESİ', 'Gamma glutamil transferaz (GGT)', '10', 'U/L', '1 - 55', '2023-07-02'),
(14, '11111111111', 'BAŞAKŞEHİR ÇAM VE SAKURA ŞEHİR HASTANESİ', 'Glukoz', '236', 'mg/dL', '74 - 106', '2023-07-02'),
(15, '11111111111', 'BAŞAKŞEHİR ÇAM VE SAKURA ŞEHİR HASTANESİ', 'Kalsiyum (Ca)', '10.4', 'mg/dL', '8.8 - 10.6', '2023-07-02'),
(16, '11111111111', 'BAŞAKŞEHİR ÇAM VE SAKURA ŞEHİR HASTANESİ', 'Üre', '19.7', 'mg/dL', '17 - 43', '2023-07-02'),
(17, '11111111111', 'BAŞAKŞEHİR ÇAM VE SAKURA ŞEHİR HASTANESİ', 'Klor (Cl)', '100', 'mmol/L', '98 - 107', '2023-07-02'),
(18, '11111111111', 'BAŞAKŞEHİR ÇAM VE SAKURA ŞEHİR HASTANESİ', 'Kreatin kinaz (CK)', '61', 'U/L', '1 - 145', '2023-07-02'),
(19, '11111111111', 'BAŞAKŞEHİR ÇAM VE SAKURA ŞEHİR HASTANESİ', 'Kreatinin', '0.76', 'mg/dL', '0.67 - 1.17', '2023-07-02'),
(20, '11111111111', 'BAŞAKŞEHİR ÇAM VE SAKURA ŞEHİR HASTANESİ', 'Laktik Dehidrogenaz (LDH)', '163', 'U/L', '1 - 248', '2023-07-02'),
(21, '11111111111', 'BAŞAKŞEHİR ÇAM VE SAKURA ŞEHİR HASTANESİ', 'Lipaz', '43.4', 'U/L', '1 - 67', '2023-07-02'),
(22, '11111111111', 'BAŞAKŞEHİR ÇAM VE SAKURA ŞEHİR HASTANESİ', 'Magnezyum', '2.3', 'mg/dL', '1.8 - 2.6', '2023-07-02'),
(23, '11111111111', 'BAŞAKŞEHİR ÇAM VE SAKURA ŞEHİR HASTANESİ', 'Potasyum', '4.94', 'mmol/L', '3.50 - 5.10', '2023-07-02'),
(24, '11111111111', 'BAŞAKŞEHİR ÇAM VE SAKURA ŞEHİR HASTANESİ', 'Total Protein', '6.91', 'g/dL', '6.6 - 8.3', '2023-07-02'),
(25, '11111111111', 'BAŞAKŞEHİR ÇAM VE SAKURA ŞEHİR HASTANESİ', 'Sodyum (Na) (Serum ve vücut sıvılarında, herbiri)', '135', 'mmol/L', '136 - 146', '2023-07-02'),
(26, '11111111111', 'BAŞAKŞEHİR ÇAM VE SAKURA ŞEHİR HASTANESİ', 'Ürik asit', '6', 'mg/dL', '3.5 - 7.2', '2023-07-02'),
(27, '11111111111', 'BAŞAKŞEHİR ÇAM VE SAKURA ŞEHİR HASTANESİ', 'WBC', '10.03', '10 3/uL', '4.00 - 10.00', '2023-07-02'),
(28, '11111111111', 'BAŞAKŞEHİR ÇAM VE SAKURA ŞEHİR HASTANESİ', 'NEU%', '73.4', '%', '50.00 - 70.00', '2023-07-02'),
(29, '11111111111', 'BAŞAKŞEHİR ÇAM VE SAKURA ŞEHİR HASTANESİ', 'MO#', '0.61', '10 3/uL', '0.12 - 1.20', '2023-07-02'),
(30, '11111111111', 'BAŞAKŞEHİR ÇAM VE SAKURA ŞEHİR HASTANESİ', 'LY%', '19.2', '%', '20.00 - 40.00', '2023-07-02'),
(31, '11111111111', 'BAŞAKŞEHİR ÇAM VE SAKURA ŞEHİR HASTANESİ', 'EOS%', '1', '%', '0.50 - 5.00', '2023-07-02'),
(32, '11111111111', 'BAŞAKŞEHİR ÇAM VE SAKURA ŞEHİR HASTANESİ', 'BASO#', '0.3', '10 3/uL', '0.00 - 0.10', '2023-07-02'),
(33, '11111111111', 'BAŞAKŞEHİR ÇAM VE SAKURA ŞEHİR HASTANESİ', 'NEU#', '7.36', '10 3/uL', '2.00 - 7.00', '2023-07-02'),
(34, '11111111111', 'BAŞAKŞEHİR ÇAM VE SAKURA ŞEHİR HASTANESİ', 'MO%', '6.1', '%', '3.00 - 12.00', '2023-07-02'),
(35, '11111111111', 'BAŞAKŞEHİR ÇAM VE SAKURA ŞEHİR HASTANESİ', 'LY#', '1.93', '10 3/uL', '0.80 - 4.00', '2023-07-02'),
(36, '11111111111', 'BAŞAKŞEHİR ÇAM VE SAKURA ŞEHİR HASTANESİ', 'EOS#', '0.1', '10 3/uL', '0.02 - 0.50', '2023-07-02'),
(37, '11111111111', 'BAŞAKŞEHİR ÇAM VE SAKURA ŞEHİR HASTANESİ', 'BASO%', '0.03', '%', '0.00 - 1.00', '2023-07-02'),
(38, '11111111111', 'BAŞAKŞEHİR ÇAM VE SAKURA ŞEHİR HASTANESİ', 'RBC', '5.01', '10 6/uL', '4.00 - 5.50', '2023-07-02'),
(39, '11111111111', 'BAŞAKŞEHİR ÇAM VE SAKURA ŞEHİR HASTANESİ', 'Hgb', '14.9', 'g/dL', '12.00 - 16.00', '2023-07-02'),
(40, '11111111111', 'BAŞAKŞEHİR ÇAM VE SAKURA ŞEHİR HASTANESİ', 'Hct', '43.9', '%', '40.00 - 54.00', '2023-07-02'),
(41, '11111111111', 'BAŞAKŞEHİR ÇAM VE SAKURA ŞEHİR HASTANESİ', 'MCV', '87.6', 'fl', '80.00 - 100.00', '2023-07-02'),
(42, '11111111111', 'BAŞAKŞEHİR ÇAM VE SAKURA ŞEHİR HASTANESİ', 'MCH', '29.7', 'pg', '27.00 - 34.00', '2023-07-02'),
(43, '11111111111', 'BAŞAKŞEHİR ÇAM VE SAKURA ŞEHİR HASTANESİ', 'MCHC', '33.9', 'g/dL', '32.00 - 36.00', '2023-07-02'),
(44, '11111111111', 'BAŞAKŞEHİR ÇAM VE SAKURA ŞEHİR HASTANESİ', 'RDW', '13.1', '%', '11.00 - 16.00', '2023-07-02'),
(45, '11111111111', 'BAŞAKŞEHİR ÇAM VE SAKURA ŞEHİR HASTANESİ', 'Plt', '238', '10 3/uL', '100 - 400', '2023-07-02'),
(46, '11111111111', 'BAŞAKŞEHİR ÇAM VE SAKURA ŞEHİR HASTANESİ', 'MPV', '9.9', 'fl', '6.50 - 12.00', '2023-07-02'),
(47, '11111111111', 'BAŞAKŞEHİR ÇAM VE SAKURA ŞEHİR HASTANESİ', 'Pct', '0.24', '%', '0.108 - 0.282', '2023-07-02'),
(48, '11111111111', 'BAŞAKŞEHİR ÇAM VE SAKURA ŞEHİR HASTANESİ', 'PDW', '16.4', '%', '15.00 - 17.00', '2023-07-02');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `medicalrecords`
--

CREATE TABLE `medicalrecords` (
  `ID` int(11) NOT NULL,
  `PatientTC` varchar(11) DEFAULT NULL,
  `DiseaseName` varchar(100) DEFAULT NULL,
  `StartDate` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Tablo döküm verisi `medicalrecords`
--

INSERT INTO `medicalrecords` (`ID`, `PatientTC`, `DiseaseName`, `StartDate`) VALUES
(1, '11111111111', 'Hypertension', '2022-01-01'),
(2, '11111111111', 'Dermatitis', '2023-06-01'),
(3, '11111111111', 'Migraine', '2023-01-01');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `patients`
--

CREATE TABLE `patients` (
  `ID` int(11) NOT NULL,
  `TCNumber` varchar(11) DEFAULT NULL,
  `FirstName` varchar(100) DEFAULT NULL,
  `LastName` varchar(100) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `Password` varchar(500) DEFAULT NULL,
  `DateOfBirth` date DEFAULT NULL,
  `Gender` char(1) DEFAULT NULL,
  `BloodGroup` char(3) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Tablo döküm verisi `patients`
--

INSERT INTO `patients` (`ID`, `TCNumber`, `FirstName`, `LastName`, `Email`, `Password`, `DateOfBirth`, `Gender`, `BloodGroup`) VALUES
(1, '11111111111', 'Ali', 'Veli', 'ali@mail.com', '$5$rounds=535000$0fXZxckgqyGvB.gp$YDtNq32Kjhj6BqxL1.zvLyGuJ44WflpBkw2008AA20D', '1980-01-01', 'M', 'A+'),
(2, '11111111112', 'Ayşe', 'Yılmaz', 'ayse@mail.com', '$5$rounds=535000$0fXZxckgqyGvB.gp$YDtNq32Kjhj6BqxL1.zvLyGuJ44WflpBkw2008AA20D', '1990-02-02', 'F', 'B-'),
(3, '11111111113', 'Mehmet', 'Kaya', 'mehmet@mail.com', '$5$rounds=535000$0fXZxckgqyGvB.gp$YDtNq32Kjhj6BqxL1.zvLyGuJ44WflpBkw2008AA20D', '1985-03-03', 'M', '0+');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `radiologyimages`
--

CREATE TABLE `radiologyimages` (
  `ID` int(11) NOT NULL,
  `PatientTC` varchar(11) DEFAULT NULL,
  `HospitalName` varchar(200) NOT NULL,
  `ImageType` varchar(100) DEFAULT NULL,
  `ImageLocation` varchar(500) DEFAULT NULL,
  `ImageDate` date DEFAULT NULL,
  `Notes` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Tablo döküm verisi `radiologyimages`
--

INSERT INTO `radiologyimages` (`ID`, `PatientTC`, `HospitalName`, `ImageType`, `ImageLocation`, `ImageDate`, `Notes`) VALUES
(2, '11111111111', 'BAŞAKŞEHİR ÇAM VE SAKURA ŞEHİR HASTANESİ', 'Brain MRI', '/img/11111111111/brain2.nii', '2023-05-05', NULL),
(6, '11111111111', 'BAŞAKŞEHİR ÇAM VE SAKURA ŞEHİR HASTANESİ', 'Brain MRI', '/img/11111111111/brain6.nii', '2023-07-20', NULL),
(8, '11111111112', 'BAŞAKŞEHİR ÇAM VE SAKURA ŞEHİR HASTANESİ', 'Mamografi', '/img/11111111112/2023-12-04/RCC.jpg,/img/11111111112/2023-12-04/LCC.jpg,/img/11111111112/2023-12-04/RMLO.jpg,/img/11111111112/2023-12-04/LMLO.jpg', '2023-12-04', NULL),
(9, '11111111112', 'BAŞAKŞEHİR ÇAM VE SAKURA ŞEHİR HASTANESİ', 'Mamografi', '/img/11111111112/2023-12-06/RCC.jpg,/img/11111111112/2023-12-06/LCC.jpg,/img/11111111112/2023-12-06/RMLO.jpg,/img/11111111112/2023-12-06/LMLO.jpg', '2023-12-06', NULL);

--
-- Dökümü yapılmış tablolar için indeksler
--

--
-- Tablo için indeksler `appointments`
--
ALTER TABLE `appointments`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `PatientTC` (`PatientTC`),
  ADD KEY `DoctorTC` (`DoctorTC`);

--
-- Tablo için indeksler `doctors`
--
ALTER TABLE `doctors`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `TCNumber` (`TCNumber`),
  ADD UNIQUE KEY `Email` (`Email`);

--
-- Tablo için indeksler `hospitalvisits`
--
ALTER TABLE `hospitalvisits`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `PatientTC` (`PatientTC`),
  ADD KEY `DoctorTC` (`DoctorTC`);

--
-- Tablo için indeksler `laboratoryresults`
--
ALTER TABLE `laboratoryresults`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `PatientTC` (`PatientTC`);

--
-- Tablo için indeksler `medicalrecords`
--
ALTER TABLE `medicalrecords`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `PatientTC` (`PatientTC`);

--
-- Tablo için indeksler `patients`
--
ALTER TABLE `patients`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `TCNumber` (`TCNumber`),
  ADD UNIQUE KEY `Email` (`Email`);

--
-- Tablo için indeksler `radiologyimages`
--
ALTER TABLE `radiologyimages`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `PatientTC` (`PatientTC`);

--
-- Dökümü yapılmış tablolar için AUTO_INCREMENT değeri
--

--
-- Tablo için AUTO_INCREMENT değeri `appointments`
--
ALTER TABLE `appointments`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Tablo için AUTO_INCREMENT değeri `doctors`
--
ALTER TABLE `doctors`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Tablo için AUTO_INCREMENT değeri `hospitalvisits`
--
ALTER TABLE `hospitalvisits`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Tablo için AUTO_INCREMENT değeri `laboratoryresults`
--
ALTER TABLE `laboratoryresults`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=50;

--
-- Tablo için AUTO_INCREMENT değeri `medicalrecords`
--
ALTER TABLE `medicalrecords`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Tablo için AUTO_INCREMENT değeri `patients`
--
ALTER TABLE `patients`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Tablo için AUTO_INCREMENT değeri `radiologyimages`
--
ALTER TABLE `radiologyimages`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- Dökümü yapılmış tablolar için kısıtlamalar
--

--
-- Tablo kısıtlamaları `appointments`
--
ALTER TABLE `appointments`
  ADD CONSTRAINT `appointments_ibfk_1` FOREIGN KEY (`PatientTC`) REFERENCES `patients` (`TCNumber`),
  ADD CONSTRAINT `appointments_ibfk_2` FOREIGN KEY (`DoctorTC`) REFERENCES `doctors` (`TCNumber`);

--
-- Tablo kısıtlamaları `hospitalvisits`
--
ALTER TABLE `hospitalvisits`
  ADD CONSTRAINT `hospitalvisits_ibfk_1` FOREIGN KEY (`PatientTC`) REFERENCES `patients` (`TCNumber`),
  ADD CONSTRAINT `hospitalvisits_ibfk_2` FOREIGN KEY (`DoctorTC`) REFERENCES `doctors` (`TCNumber`);

--
-- Tablo kısıtlamaları `laboratoryresults`
--
ALTER TABLE `laboratoryresults`
  ADD CONSTRAINT `laboratoryresults_ibfk_1` FOREIGN KEY (`PatientTC`) REFERENCES `patients` (`TCNumber`);

--
-- Tablo kısıtlamaları `medicalrecords`
--
ALTER TABLE `medicalrecords`
  ADD CONSTRAINT `medicalrecords_ibfk_1` FOREIGN KEY (`PatientTC`) REFERENCES `patients` (`TCNumber`);

--
-- Tablo kısıtlamaları `radiologyimages`
--
ALTER TABLE `radiologyimages`
  ADD CONSTRAINT `radiologyimages_ibfk_1` FOREIGN KEY (`PatientTC`) REFERENCES `patients` (`TCNumber`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
