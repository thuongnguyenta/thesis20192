-- phpMyAdmin SQL Dump
-- version 4.9.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 09, 2020 at 08:42 AM
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
-- Database: `20192`
--

-- --------------------------------------------------------

--
-- Table structure for table `account`
--

CREATE TABLE `account` (
  `id_account` int(11) NOT NULL,
  `email` varchar(100) NOT NULL,
  `username` varchar(45) NOT NULL,
  `password` varchar(45) NOT NULL,
  `phone_number` int(11) NOT NULL,
  `address` varchar(100) NOT NULL,
  `cover_image` varchar(200) DEFAULT NULL,
  `role` int(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `account`
--

INSERT INTO `account` (`id_account`, `email`, `username`, `password`, `phone_number`, `address`, `cover_image`, `role`) VALUES
(1, 'thuonghy961@gmail.com', 'Thưởng', 'mot2ba4nam7', 987654321, 'Ngọc Thanh - Kim Động - Hưng Yên', NULL, 1),
(2, 'manhpc@gmail.com', 'Mạnh', '2', 123456789, 'Nam Định- Việt Nam', NULL, 2);

-- --------------------------------------------------------

--
-- Table structure for table `cart`
--

CREATE TABLE `cart` (
  `id_cart` int(11) NOT NULL,
  `id_user` int(11) NOT NULL,
  `cart_quantity` int(11) NOT NULL,
  `cart_total_price` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `cart`
--

INSERT INTO `cart` (`id_cart`, `id_user`, `cart_quantity`, `cart_total_price`) VALUES
(1, 2, 3, 14087000);

-- --------------------------------------------------------

--
-- Table structure for table `cart_detail`
--

CREATE TABLE `cart_detail` (
  `id_cart_detail` int(11) NOT NULL,
  `id_shoes` int(11) NOT NULL,
  `id_color` int(11) NOT NULL,
  `size` int(2) NOT NULL,
  `id_cart` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `price_per_product` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `cart_detail`
--

INSERT INTO `cart_detail` (`id_cart_detail`, `id_shoes`, `id_color`, `size`, `id_cart`, `quantity`, `price_per_product`) VALUES
(1, 4, 7, 40, 1, 1, 3519000),
(2, 5, 9, 43, 1, 1, 5869000),
(3, 1, 1, 36, 1, 1, 4699000);

-- --------------------------------------------------------

--
-- Table structure for table `comment`
--

CREATE TABLE `comment` (
  `id_comment` int(11) NOT NULL,
  `id_user` int(11) NOT NULL,
  `id_shoes` int(11) NOT NULL,
  `star` int(1) NOT NULL,
  `comments` varchar(300) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `comment`
--

INSERT INTO `comment` (`id_comment`, `id_user`, `id_shoes`, `star`, `comments`) VALUES
(1, 2, 5, 5, 'Giày đi rất êm và thoải mái\r\n'),
(2, 2, 1, 4, 'Giày đi thoáng và rất thoải mái'),
(3, 2, 1, 3, 'Cũng bình thường');

-- --------------------------------------------------------

--
-- Table structure for table `order_detail`
--

CREATE TABLE `order_detail` (
  `id_order_detail` int(11) NOT NULL,
  `id_shoes` int(11) NOT NULL,
  `id_shoes_color` int(11) NOT NULL,
  `order_detail_quantity` int(11) NOT NULL,
  `order_size` int(11) NOT NULL,
  `id_order` int(11) NOT NULL,
  `price_per_order` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `order_detail`
--

INSERT INTO `order_detail` (`id_order_detail`, `id_shoes`, `id_shoes_color`, `order_detail_quantity`, `order_size`, `id_order`, `price_per_order`) VALUES
(1, 4, 7, 1, 40, 1, 3519000),
(2, 5, 8, 1, 42, 1, 5869000);

-- --------------------------------------------------------

--
-- Table structure for table `ship`
--

CREATE TABLE `ship` (
  `id_ship` int(11) NOT NULL,
  `id_order` int(11) NOT NULL,
  `address_order` varchar(200) NOT NULL,
  `phone` int(11) NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  `status` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `ship`
--

INSERT INTO `ship` (`id_ship`, `id_order`, `address_order`, `phone`, `name`, `status`) VALUES
(1, 1, 'Nam Định', 12345678, 'Phạm Công Mạnh', 'Đã Hoàn Thành');

-- --------------------------------------------------------

--
-- Table structure for table `shoes`
--

CREATE TABLE `shoes` (
  `id_shoes` int(11) NOT NULL,
  `shoes_name` varchar(45) NOT NULL,
  `gender_shoes` varchar(5) NOT NULL,
  `shoes_type` varchar(45) NOT NULL,
  `feature` varchar(200) DEFAULT NULL,
  `price` float NOT NULL,
  `athleter` varchar(100) DEFAULT NULL,
  `sale` int(2) NOT NULL,
  `catalogy` varchar(45) NOT NULL,
  `describe` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `shoes`
--

INSERT INTO `shoes` (`id_shoes`, `shoes_name`, `gender_shoes`, `shoes_type`, `feature`, `price`, `athleter`, `sale`, `catalogy`, `describe`) VALUES
(1, 'Nike React Infinity Run Flyknit', 'Both', 'Running', 'Waterproof', 4699000, NULL, 0, 'Snacker', 'Giày tốt cho vận động nhẹ nhàng, bền, đẹp'),
(3, 'Nike Mercurial Superfly 7 Elite MDS FG', 'Man', 'Football', 'Reflection', 8799000, 'Cristiano Ronaldo', 10, 'Boot', 'Giày phù hợp với nhiều địa hình di chuyển, bền thuận cho chuyển động linh hoạt,...'),
(4, 'Nike Air Max 200', 'Woman', 'Training', 'Waterproof', 3519000, NULL, 0, 'Sandals', 'Giày đi thoáng và thoải mái, Truyền cảm hứng từ năng lượng trái đất'),
(5, 'LeBron 7 QS', 'Man', 'Basketball', 'Reflection', 5869000, 'LeBron James', 0, 'Boot', 'Giúp cho đôi chân của bạn cực kì thoải mái, Xây dựng sức mạnh tối đa phối hợp nhiều chất liệu nhiều mặt, ...'),
(6, 'Giày Test', 'Both', 'Running', NULL, 1234000, NULL, 0, 'Boot', 'Giày để test');

-- --------------------------------------------------------

--
-- Table structure for table `shoes_color`
--

CREATE TABLE `shoes_color` (
  `id_shoes_color` int(11) NOT NULL,
  `id_shoes` int(11) NOT NULL,
  `color` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `shoes_color`
--

INSERT INTO `shoes_color` (`id_shoes_color`, `id_shoes`, `color`) VALUES
(1, 1, 'Black'),
(2, 1, 'Laser Orange'),
(4, 1, 'White'),
(5, 1, 'Red'),
(6, 3, 'Lemon Venom'),
(7, 4, 'White Purple'),
(8, 5, 'Blue'),
(9, 5, 'Gold White');

-- --------------------------------------------------------

--
-- Table structure for table `shoes_color_image`
--

CREATE TABLE `shoes_color_image` (
  `id_shoes_color_image` int(11) NOT NULL,
  `id_shoes_color` int(11) NOT NULL,
  `image` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `shoes_color_image`
--

INSERT INTO `shoes_color_image` (`id_shoes_color_image`, `id_shoes_color`, `image`) VALUES
(1, 1, '1/Black/52600ab1-4a17-4822-91f1-cfeb580c3004.webp'),
(2, 2, '1/Laser Orange/148cc626-4dbc-4869-b83b-d26b2da1755a.webp'),
(3, 4, '1/White/0c95d5ba-3ed3-4000-b073-537472bda3d3.webp'),
(4, 5, '1/Red/652d3200-ef4c-44a9-b35e-01b6df66e907.webp'),
(5, 4, '1/White/7d2b8bee-a73a-4021-b839-5191ad7709e4.webp'),
(6, 4, '1/White/a7c26b3b-4fa6-4a7a-a225-f5fb55258292.webp'),
(7, 4, '1/White/ef03abcb-b457-4d0c-81ef-74ddd36bf82b.webp'),
(8, 4, '1/White/a18ffc7e-f172-47f2-87eb-1b4de4163b10.webp'),
(9, 5, '1/Red/8cf1055f-7a7d-421a-b93d-86dd0ca616fc.webp'),
(10, 5, '1/Red/22a690d6-6af9-4f44-a5fa-9b3baf08ea08.webp'),
(11, 5, '1/Red/8b36083a-b066-447c-8c70-e67cf7a62cd6.webp'),
(12, 5, '1/Red/b8470998-1861-4b17-9db7-1b78c322cd9e.webp'),
(13, 1, '1/Black/5a2f7ee8-1ad2-4652-b1cf-12e1e59a9e99.webp'),
(14, 1, '1/Black/5edd8108-fc14-477a-a63a-12fcb80d1b1d.webp'),
(15, 1, '1/Black/760e84b0-2c43-40e9-b09c-20f445d45f59.webp'),
(16, 1, '1/Black/e7fa0330-b4e4-46aa-bbff-bfd6287f5dd1.webp'),
(17, 2, '1/Laser Orange/0e1faaca-6467-4f0a-a89a-24dcfbf55b9c.webp'),
(18, 2, '1/Laser Orange/9d9cc57b-f750-4376-8e55-ba9986da95d2.webp'),
(19, 2, '1/Laser Orange/58901440-8cd6-41a7-bafb-7ea9ee4cac04.webp'),
(20, 2, '1/Laser Orange/f0ac4fc5-415a-43e7-b02f-ab3713276bc2.webp'),
(21, 6, '2/Lemon Venom/i1-e43bc0a3-290d-4620-983e-4d3d0a4688aa.webp'),
(22, 6, '2/Lemon Venom/i1-436b914b-fbff-42a0-8346-99e6f7152545.webp'),
(23, 6, '2/Lemon Venom/i1-480edce9-431e-478a-b4fc-888d17cfe797.webp'),
(24, 6, '2/Lemon Venom/i1-6597e2a9-4c4e-47bb-b25f-c0bbdbb2ec1b.webp'),
(25, 6, '2/Lemon Venom/i1-cb50e780-409e-4e55-bce8-5288ba735e83.webp'),
(26, 7, '3/White Purple/112ade84-3b68-4b31-962f-8ce56d55ca71.webp'),
(27, 7, '3/White Purple/10b8538a-05a5-4be1-8fa5-50320bb3e6a5.webp'),
(28, 7, '3/White Purple/360cf9d1-ef98-42b7-832d-9a2aeab1ef87.webp'),
(29, 7, '3/White Purple/506bc0dd-2bde-4394-bbd4-e3e894da422c.webp'),
(30, 7, '3/White Purple/e0c0dca6-86e6-42f0-a055-7f65e0ee0c9e.webp'),
(31, 8, '4/Blue/i1-aad4a369-9ec7-4e34-9390-46dd65541dda.webp'),
(32, 8, '4/Blue/i1-c748c859-0969-47d2-bb48-7eb19b79317e.webp'),
(33, 8, '4/Blue/i1-3eaac47e-b280-4b33-bfce-e84a91216a7b.webp'),
(34, 8, '4/Blue/i1-6146724f-bd5b-4a13-8147-308aecf9f9e8.webp'),
(35, 8, '4/Blue/i1-d57695a9-f086-40be-9dad-682306e29fcc.webp'),
(36, 8, '4/Blue/i1-a38c4564-0574-4026-8b9d-9f084ee63b09.webp'),
(37, 9, '4/Gold White/a79a34d6-eded-466a-a156-ebae7b4efdab.webp'),
(38, 9, '4/Gold White/36901f5a-5e72-4dca-b32d-eb0a5558e427.webp'),
(39, 9, '4/Gold White/73c72a30-b34b-4c73-97a6-217d3d1a5607.webp'),
(40, 9, '4/Gold White/0373d2d1-9a8d-453e-ae21-e5506ab6cbb2.webp'),
(41, 9, '4/Gold White/09715102-6fe5-4ed5-a09e-2e6939206e0e.webp'),
(42, 9, '4/Gold White/31334267-e41f-45f1-a46f-dc6edad5ddcb.webp');

-- --------------------------------------------------------

--
-- Table structure for table `shoes_surface`
--

CREATE TABLE `shoes_surface` (
  `id_shoes_surface` int(11) NOT NULL,
  `id_shoes` int(11) NOT NULL,
  `surface` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `shoes_surface`
--

INSERT INTO `shoes_surface` (`id_shoes_surface`, `id_shoes`, `surface`) VALUES
(1, 1, 'Grass'),
(2, 1, 'Firm Ground'),
(3, 1, 'Artificial Grass'),
(4, 3, 'Grass'),
(5, 3, 'Firm Ground'),
(6, 3, 'Artificial Grass'),
(7, 4, 'Multi Ground'),
(8, 4, 'Indoor'),
(9, 5, 'Soft Ground'),
(10, 5, 'Outdoor'),
(11, 5, 'Multi Ground');

-- --------------------------------------------------------

--
-- Table structure for table `user_order`
--

CREATE TABLE `user_order` (
  `id_order` int(11) NOT NULL,
  `id_user` int(11) NOT NULL,
  `order_quantity` int(11) NOT NULL,
  `total_price` float NOT NULL,
  `time_order` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user_order`
--

INSERT INTO `user_order` (`id_order`, `id_user`, `order_quantity`, `total_price`, `time_order`) VALUES
(1, 2, 2, 9388000, '2020-03-02');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `account`
--
ALTER TABLE `account`
  ADD PRIMARY KEY (`id_account`);

--
-- Indexes for table `cart`
--
ALTER TABLE `cart`
  ADD PRIMARY KEY (`id_cart`),
  ADD KEY `fk_cart_1` (`id_user`);

--
-- Indexes for table `cart_detail`
--
ALTER TABLE `cart_detail`
  ADD PRIMARY KEY (`id_cart_detail`),
  ADD KEY `fk_cd_1` (`id_cart`),
  ADD KEY `fk_cd_2` (`id_shoes`),
  ADD KEY `fk_cd_3` (`id_color`);

--
-- Indexes for table `comment`
--
ALTER TABLE `comment`
  ADD PRIMARY KEY (`id_comment`),
  ADD KEY `fk_cm_1` (`id_user`),
  ADD KEY `fk_cm_2` (`id_shoes`);

--
-- Indexes for table `order_detail`
--
ALTER TABLE `order_detail`
  ADD PRIMARY KEY (`id_order_detail`),
  ADD KEY `fk_od_1` (`id_order`),
  ADD KEY `fk_od_2` (`id_shoes`),
  ADD KEY `fk_od_3` (`id_shoes_color`);

--
-- Indexes for table `ship`
--
ALTER TABLE `ship`
  ADD PRIMARY KEY (`id_ship`),
  ADD KEY `fk_ship_1` (`id_order`);

--
-- Indexes for table `shoes`
--
ALTER TABLE `shoes`
  ADD PRIMARY KEY (`id_shoes`),
  ADD KEY `fk_shoes_2` (`feature`);

--
-- Indexes for table `shoes_color`
--
ALTER TABLE `shoes_color`
  ADD PRIMARY KEY (`id_shoes_color`),
  ADD KEY `fk_sc_1` (`id_shoes`);

--
-- Indexes for table `shoes_color_image`
--
ALTER TABLE `shoes_color_image`
  ADD PRIMARY KEY (`id_shoes_color_image`),
  ADD KEY `fk_sci_1` (`id_shoes_color`);

--
-- Indexes for table `shoes_surface`
--
ALTER TABLE `shoes_surface`
  ADD PRIMARY KEY (`id_shoes_surface`),
  ADD KEY `fk_ss_1` (`id_shoes`);

--
-- Indexes for table `user_order`
--
ALTER TABLE `user_order`
  ADD PRIMARY KEY (`id_order`),
  ADD KEY `fk_uo_1` (`id_user`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `account`
--
ALTER TABLE `account`
  MODIFY `id_account` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `cart`
--
ALTER TABLE `cart`
  MODIFY `id_cart` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `cart_detail`
--
ALTER TABLE `cart_detail`
  MODIFY `id_cart_detail` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `comment`
--
ALTER TABLE `comment`
  MODIFY `id_comment` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `order_detail`
--
ALTER TABLE `order_detail`
  MODIFY `id_order_detail` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `ship`
--
ALTER TABLE `ship`
  MODIFY `id_ship` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `shoes`
--
ALTER TABLE `shoes`
  MODIFY `id_shoes` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `shoes_color`
--
ALTER TABLE `shoes_color`
  MODIFY `id_shoes_color` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `shoes_color_image`
--
ALTER TABLE `shoes_color_image`
  MODIFY `id_shoes_color_image` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=43;

--
-- AUTO_INCREMENT for table `shoes_surface`
--
ALTER TABLE `shoes_surface`
  MODIFY `id_shoes_surface` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `user_order`
--
ALTER TABLE `user_order`
  MODIFY `id_order` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `cart`
--
ALTER TABLE `cart`
  ADD CONSTRAINT `fk_cart_1` FOREIGN KEY (`id_user`) REFERENCES `account` (`id_account`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `cart_detail`
--
ALTER TABLE `cart_detail`
  ADD CONSTRAINT `fk_cd_1` FOREIGN KEY (`id_cart`) REFERENCES `cart` (`id_cart`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_cd_2` FOREIGN KEY (`id_shoes`) REFERENCES `shoes` (`id_shoes`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_cd_3` FOREIGN KEY (`id_color`) REFERENCES `shoes_color` (`id_shoes_color`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `comment`
--
ALTER TABLE `comment`
  ADD CONSTRAINT `fk_cm_1` FOREIGN KEY (`id_user`) REFERENCES `account` (`id_account`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_cm_2` FOREIGN KEY (`id_shoes`) REFERENCES `shoes` (`id_shoes`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `order_detail`
--
ALTER TABLE `order_detail`
  ADD CONSTRAINT `fk_od_1` FOREIGN KEY (`id_order`) REFERENCES `user_order` (`id_order`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_od_2` FOREIGN KEY (`id_shoes`) REFERENCES `shoes` (`id_shoes`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_od_3` FOREIGN KEY (`id_shoes_color`) REFERENCES `shoes_color` (`id_shoes_color`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `ship`
--
ALTER TABLE `ship`
  ADD CONSTRAINT `fk_ship_1` FOREIGN KEY (`id_order`) REFERENCES `user_order` (`id_order`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `shoes_color`
--
ALTER TABLE `shoes_color`
  ADD CONSTRAINT `fk_sc_1` FOREIGN KEY (`id_shoes`) REFERENCES `shoes` (`id_shoes`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `shoes_color_image`
--
ALTER TABLE `shoes_color_image`
  ADD CONSTRAINT `fk_sci_1` FOREIGN KEY (`id_shoes_color`) REFERENCES `shoes_color` (`id_shoes_color`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `shoes_surface`
--
ALTER TABLE `shoes_surface`
  ADD CONSTRAINT `fk_ss_1` FOREIGN KEY (`id_shoes`) REFERENCES `shoes` (`id_shoes`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `user_order`
--
ALTER TABLE `user_order`
  ADD CONSTRAINT `fk_uo_1` FOREIGN KEY (`id_user`) REFERENCES `account` (`id_account`) ON DELETE NO ACTION ON UPDATE NO ACTION;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
