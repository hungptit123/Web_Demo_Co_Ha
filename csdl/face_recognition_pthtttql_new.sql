-- phpMyAdmin SQL Dump
-- version 4.9.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Jun 29, 2020 at 10:46 AM
-- Server version: 10.4.11-MariaDB
-- PHP Version: 7.4.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `face_recognition_pthtttql`
--

-- --------------------------------------------------------

--
-- Table structure for table `Attendance`
--

CREATE TABLE `Attendance` (
  `attendanceID` int(11) NOT NULL,
  `sectionID` int(11) NOT NULL,
  `startedTime` text NOT NULL,
  `endedTime` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `ClassRoom`
--

CREATE TABLE `ClassRoom` (
  `roomID` int(11) NOT NULL,
  `roomName` text NOT NULL,
  `description` text NOT NULL,
  `roomCode` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `ClassRoom`
--

INSERT INTO `ClassRoom` (`roomID`, `roomName`, `description`, `roomCode`) VALUES
(1, 'phòng 505A2', 'phòng nhà A2 tầng 5', '505A2'),
(2, 'phòng 404A2', 'phòng nhà A2 tầng 4', '404A2');

-- --------------------------------------------------------

--
-- Table structure for table `ClassSection`
--

CREATE TABLE `ClassSection` (
  `sectionID` int(11) NOT NULL,
  `groupID` int(11) NOT NULL,
  `roomID` int(11) NOT NULL,
  `weekDay` text NOT NULL,
  `startSlot` int(11) NOT NULL,
  `teacherID` int(11) NOT NULL,
  `numberOfStudents` int(11) NOT NULL,
  `attendanceStatus` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `ClassSection`
--

INSERT INTO `ClassSection` (`sectionID`, `groupID`, `roomID`, `weekDay`, `startSlot`, `teacherID`, `numberOfStudents`, `attendanceStatus`) VALUES
(1, 1, 1, '18/25/2020', 7, 3, 6, 0),
(2, 1, 1, '30/6/2020', 7, 3, 6, 0),
(3, 1, 1, '30/06/2020', 11, 3, 6, 0),
(4, 3, 2, '30/06/2020', 1, 3, 4, 0);

-- --------------------------------------------------------

--
-- Table structure for table `Grade`
--

CREATE TABLE `Grade` (
  `gradeID` int(11) NOT NULL,
  `gradeName` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Grade`
--

INSERT INTO `Grade` (`gradeID`, `gradeName`) VALUES
(1, 'D16CQCN01-B'),
(2, 'D16CQCN02-B'),
(3, 'D16CQCN03-B'),
(4, 'D16CQCN04-B');

-- --------------------------------------------------------

--
-- Table structure for table `GroupStudent`
--

CREATE TABLE `GroupStudent` (
  `groupStudentID` int(11) NOT NULL,
  `groupID` int(11) NOT NULL,
  `studentID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `GroupStudent`
--

INSERT INTO `GroupStudent` (`groupStudentID`, `groupID`, `studentID`) VALUES
(1, 1, 1),
(2, 1, 2),
(3, 1, 3),
(4, 1, 4),
(5, 1, 5),
(6, 1, 6),
(7, 3, 1),
(8, 3, 2),
(9, 3, 3),
(10, 3, 4);

-- --------------------------------------------------------

--
-- Table structure for table `GroupSubject`
--

CREATE TABLE `GroupSubject` (
  `groupID` int(11) NOT NULL,
  `subjectID` int(11) NOT NULL,
  `groupName` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `GroupSubject`
--

INSERT INTO `GroupSubject` (`groupID`, `subjectID`, `groupName`) VALUES
(1, 1, 'Nhóm 1'),
(2, 1, 'Nhóm 2'),
(3, 2, 'Nhóm 1'),
(4, 2, 'Nhóm 2');

-- --------------------------------------------------------

--
-- Table structure for table `Image`
--

CREATE TABLE `Image` (
  `imageID` int(11) NOT NULL,
  `studentID` int(11) NOT NULL,
  `bounding_box` text NOT NULL,
  `embeddings` text NOT NULL,
  `image` blob NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `Member`
--

CREATE TABLE `Member` (
  `memberID` int(11) NOT NULL,
  `userName` text NOT NULL,
  `password` text NOT NULL,
  `personID` int(11) NOT NULL,
  `roleID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Member`
--

INSERT INTO `Member` (`memberID`, `userName`, `password`, `personID`, `roleID`) VALUES
(1, 'phanthiha', '123', 10, 1),
(2, 'ngoxuanbach', '123', 8, 1),
(3, 'nguyenmanhhung', '123', 9, 1),
(4, 'admin', '123', 11, 2);

-- --------------------------------------------------------

--
-- Table structure for table `People`
--

CREATE TABLE `People` (
  `personID` int(11) NOT NULL,
  `personName` text NOT NULL,
  `doB` text NOT NULL,
  `gender` int(11) NOT NULL,
  `email` text NOT NULL,
  `contactMobile` text NOT NULL,
  `address` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `People`
--

INSERT INTO `People` (`personID`, `personName`, `doB`, `gender`, `email`, `contactMobile`, `address`) VALUES
(1, 'Đinh Văn Hùng', '18/05/1998', 1, 'hungptitcn1@gmail.com', '0969650671', 'Mê Linh - Hà Nội'),
(2, 'Lê Duy Bách', '10/4/1998', 1, 'bach@gmail.com', '01234567855', 'Hà Nội'),
(4, 'Nguyễn Hà Phương', '10/5/1998', 1, 'haphuong@gmail.com', '01324567855', 'Hà Nội'),
(5, 'Nguyễn Thị Hạnh', '1/1/1998', 0, 'hanh@gmail.com', '054567855', 'Hà Nội'),
(6, 'Phạm Thị Hiên', '4/5/1998', 0, 'hien@gmail.com', '0132457855', 'Hà Nội'),
(7, 'Nguyễn Thùy Vân', '10/6/1998', 0, 'thuyvan@gmail.com', '01324437855', 'Hà Nội'),
(8, 'Ngô Xuân Bách', '6/10/1980', 1, 'xuanbach@gmail.com', '098989898', 'Hà Nội'),
(9, 'Nguyễn Mạnh Hùng', '6/11/1978', 1, 'hungnm@gmail.com', '098989884', 'Hà Nội'),
(10, 'Phạm Thị Hà', '6/10/1980', 0, 'phamthiha@gmail.com', '098989898', 'Hà Nội'),
(11, 'admin', 'no', 1, 'ptit@gmail.com', '190019890', 'Miền Bắc');

-- --------------------------------------------------------

--
-- Table structure for table `Remark`
--

CREATE TABLE `Remark` (
  `remarkID` int(11) NOT NULL,
  `attendanceID` int(11) NOT NULL,
  `isAttendanced` int(11) NOT NULL,
  `studentID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `Role`
--

CREATE TABLE `Role` (
  `roleID` int(11) NOT NULL,
  `roleName` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Role`
--

INSERT INTO `Role` (`roleID`, `roleName`) VALUES
(1, 'giaovien'),
(2, 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `Student`
--

CREATE TABLE `Student` (
  `studentID` int(11) NOT NULL,
  `personID` int(11) NOT NULL,
  `gradeID` int(11) NOT NULL,
  `studentCode` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Student`
--

INSERT INTO `Student` (`studentID`, `personID`, `gradeID`, `studentCode`) VALUES
(1, 1, 1, 'B16DCCN161'),
(2, 2, 1, 'B16DCCN022'),
(3, 4, 1, 'B16DCCN273'),
(4, 7, 1, 'B16DCCN123'),
(5, 6, 1, 'B16DCCN125'),
(6, 5, 1, 'B16DCCN187');

-- --------------------------------------------------------

--
-- Table structure for table `Subject`
--

CREATE TABLE `Subject` (
  `subjectID` int(11) NOT NULL,
  `subjectName` text NOT NULL,
  `credits` int(11) NOT NULL,
  `subjectCode` text NOT NULL,
  `gradeID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Subject`
--

INSERT INTO `Subject` (`subjectID`, `subjectName`, `credits`, `subjectCode`, `gradeID`) VALUES
(1, 'Phân tích hệ thống thông tin quản lý', 3, 'INT1445', 1),
(2, 'Cơ sở dữ liệu phân tán', 3, 'INT1234', 1),
(3, 'Trí tuệ nhân tạo', 2, 'INT1245', 2),
(4, 'Phân tích thiết kệ hệ thống thông tin', 3, 'INT124567', 3);

-- --------------------------------------------------------

--
-- Table structure for table `Teacher`
--

CREATE TABLE `Teacher` (
  `teacherID` int(11) NOT NULL,
  `personID` int(11) NOT NULL,
  `specialize` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Teacher`
--

INSERT INTO `Teacher` (`teacherID`, `personID`, `specialize`) VALUES
(1, 9, 'Công nghệ phần mềm'),
(2, 8, 'AI - ML - NLP'),
(3, 10, 'Hệ thống thông tin');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Attendance`
--
ALTER TABLE `Attendance`
  ADD PRIMARY KEY (`attendanceID`),
  ADD KEY `sectionID` (`sectionID`);

--
-- Indexes for table `ClassRoom`
--
ALTER TABLE `ClassRoom`
  ADD PRIMARY KEY (`roomID`);

--
-- Indexes for table `ClassSection`
--
ALTER TABLE `ClassSection`
  ADD PRIMARY KEY (`sectionID`),
  ADD KEY `teacherID` (`teacherID`),
  ADD KEY `roomID` (`roomID`),
  ADD KEY `groupID` (`groupID`);

--
-- Indexes for table `Grade`
--
ALTER TABLE `Grade`
  ADD PRIMARY KEY (`gradeID`);

--
-- Indexes for table `GroupStudent`
--
ALTER TABLE `GroupStudent`
  ADD PRIMARY KEY (`groupStudentID`),
  ADD KEY `groupID` (`groupID`),
  ADD KEY `studentID` (`studentID`);

--
-- Indexes for table `GroupSubject`
--
ALTER TABLE `GroupSubject`
  ADD PRIMARY KEY (`groupID`),
  ADD KEY `subjectID` (`subjectID`);

--
-- Indexes for table `Image`
--
ALTER TABLE `Image`
  ADD PRIMARY KEY (`imageID`),
  ADD KEY `studentID` (`studentID`);

--
-- Indexes for table `Member`
--
ALTER TABLE `Member`
  ADD PRIMARY KEY (`memberID`),
  ADD KEY `personID` (`personID`),
  ADD KEY `roleID` (`roleID`);

--
-- Indexes for table `People`
--
ALTER TABLE `People`
  ADD PRIMARY KEY (`personID`);

--
-- Indexes for table `Remark`
--
ALTER TABLE `Remark`
  ADD PRIMARY KEY (`remarkID`),
  ADD KEY `studentID` (`studentID`),
  ADD KEY `attendanceID` (`attendanceID`);

--
-- Indexes for table `Role`
--
ALTER TABLE `Role`
  ADD PRIMARY KEY (`roleID`);

--
-- Indexes for table `Student`
--
ALTER TABLE `Student`
  ADD PRIMARY KEY (`studentID`),
  ADD KEY `personID` (`personID`),
  ADD KEY `gradeID` (`gradeID`);

--
-- Indexes for table `Subject`
--
ALTER TABLE `Subject`
  ADD PRIMARY KEY (`subjectID`),
  ADD KEY `gradeID` (`gradeID`);

--
-- Indexes for table `Teacher`
--
ALTER TABLE `Teacher`
  ADD PRIMARY KEY (`teacherID`),
  ADD KEY `personID` (`personID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Attendance`
--
ALTER TABLE `Attendance`
  MODIFY `attendanceID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `ClassRoom`
--
ALTER TABLE `ClassRoom`
  MODIFY `roomID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `ClassSection`
--
ALTER TABLE `ClassSection`
  MODIFY `sectionID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `Grade`
--
ALTER TABLE `Grade`
  MODIFY `gradeID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `GroupStudent`
--
ALTER TABLE `GroupStudent`
  MODIFY `groupStudentID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `GroupSubject`
--
ALTER TABLE `GroupSubject`
  MODIFY `groupID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `Image`
--
ALTER TABLE `Image`
  MODIFY `imageID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `Member`
--
ALTER TABLE `Member`
  MODIFY `memberID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `People`
--
ALTER TABLE `People`
  MODIFY `personID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `Remark`
--
ALTER TABLE `Remark`
  MODIFY `remarkID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `Role`
--
ALTER TABLE `Role`
  MODIFY `roleID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `Student`
--
ALTER TABLE `Student`
  MODIFY `studentID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `Subject`
--
ALTER TABLE `Subject`
  MODIFY `subjectID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `Teacher`
--
ALTER TABLE `Teacher`
  MODIFY `teacherID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Attendance`
--
ALTER TABLE `Attendance`
  ADD CONSTRAINT `Attendance_ibfk_1` FOREIGN KEY (`sectionID`) REFERENCES `ClassSection` (`sectionID`);

--
-- Constraints for table `ClassSection`
--
ALTER TABLE `ClassSection`
  ADD CONSTRAINT `ClassSection_ibfk_2` FOREIGN KEY (`teacherID`) REFERENCES `Teacher` (`teacherID`),
  ADD CONSTRAINT `ClassSection_ibfk_3` FOREIGN KEY (`roomID`) REFERENCES `ClassRoom` (`roomID`),
  ADD CONSTRAINT `ClassSection_ibfk_4` FOREIGN KEY (`groupID`) REFERENCES `GroupSubject` (`groupID`);

--
-- Constraints for table `GroupStudent`
--
ALTER TABLE `GroupStudent`
  ADD CONSTRAINT `GroupStudent_ibfk_1` FOREIGN KEY (`groupID`) REFERENCES `GroupSubject` (`groupID`),
  ADD CONSTRAINT `GroupStudent_ibfk_2` FOREIGN KEY (`studentID`) REFERENCES `Student` (`studentID`);

--
-- Constraints for table `GroupSubject`
--
ALTER TABLE `GroupSubject`
  ADD CONSTRAINT `GroupSubject_ibfk_1` FOREIGN KEY (`subjectID`) REFERENCES `Subject` (`subjectID`);

--
-- Constraints for table `Image`
--
ALTER TABLE `Image`
  ADD CONSTRAINT `Image_ibfk_1` FOREIGN KEY (`studentID`) REFERENCES `Student` (`studentID`);

--
-- Constraints for table `Member`
--
ALTER TABLE `Member`
  ADD CONSTRAINT `Member_ibfk_1` FOREIGN KEY (`personID`) REFERENCES `People` (`personID`),
  ADD CONSTRAINT `Member_ibfk_2` FOREIGN KEY (`roleID`) REFERENCES `Role` (`roleID`);

--
-- Constraints for table `Remark`
--
ALTER TABLE `Remark`
  ADD CONSTRAINT `Remark_ibfk_1` FOREIGN KEY (`studentID`) REFERENCES `Student` (`studentID`),
  ADD CONSTRAINT `Remark_ibfk_2` FOREIGN KEY (`attendanceID`) REFERENCES `Attendance` (`attendanceID`);

--
-- Constraints for table `Student`
--
ALTER TABLE `Student`
  ADD CONSTRAINT `Student_ibfk_1` FOREIGN KEY (`personID`) REFERENCES `People` (`personID`),
  ADD CONSTRAINT `Student_ibfk_2` FOREIGN KEY (`gradeID`) REFERENCES `Grade` (`gradeID`);

--
-- Constraints for table `Subject`
--
ALTER TABLE `Subject`
  ADD CONSTRAINT `Subject_ibfk_1` FOREIGN KEY (`gradeID`) REFERENCES `Grade` (`gradeID`);

--
-- Constraints for table `Teacher`
--
ALTER TABLE `Teacher`
  ADD CONSTRAINT `Teacher_ibfk_1` FOREIGN KEY (`personID`) REFERENCES `People` (`personID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
