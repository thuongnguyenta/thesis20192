-- phpMyAdmin SQL Dump
-- version 5.0.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 15, 2020 at 02:20 AM
-- Server version: 10.4.11-MariaDB
-- PHP Version: 7.2.27

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
(1, 'thuonghy961@gmail.com', 'Thưởng', 'mot2ba4nam7', 987654321, 'Ngọc Thanh - Kim Động - Hưng Yên', '/static/image/people/tiep.jpg', 1),
(2, 'manhpc@gmail.com', 'Thưởng', '2', 123456789, 'Nam Định- Việt Nam', '/static/image/people/tiep.jpg', 2),
(3, 'thuong.nt153740@sis.hust.edu.vn', 'Pig', '2', 987654321, 'Ngọc Thanh- Kim Động - Hưng Yên', '/static/image/people/tiep.jpg', 2),
(4, 'thuongnt32@viettel.com', 'Thưởng', '2', 987456321, 'Ngọc Thanh', '/static/image/people/tiep.jpg', 2),
(5, 'thuongnt33@viettel.com', 'Mạnh', '2', 147852369, 'Nam Định', '/static/image/people/tiep.jpg', 2),
(6, 'thuongnt34@viettel.com', 'Thưởng', '2', 147852369, 'Ngọc Thanh', '/static/image/people/tiep.jpg', 2),
(14, 'thuonghy962@gmail.com', 'Thưởng', 'mot2ba4nam7', 321654978, 'Ahihi', 'NULL', 2),
(15, 'thuonghy962@gmail.com', 'Thưởng', 'mot2ba4nam7', 321654978, 'Ahihi', 'NULL', 2);

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
(15, 1, 2, 13788100);

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
(25, 3, 6, 42, 15, 1, 7919100),
(26, 5, 8, 42, 15, 1, 5869000);

-- --------------------------------------------------------

--
-- Table structure for table `comment`
--

CREATE TABLE `comment` (
  `id_comment` int(11) NOT NULL,
  `id_user` int(11) NOT NULL,
  `id_shoes` int(11) NOT NULL,
  `star` int(1) NOT NULL,
  `comments` varchar(300) NOT NULL,
  `time_review` datetime NOT NULL,
  `status` int(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `comment`
--

INSERT INTO `comment` (`id_comment`, `id_user`, `id_shoes`, `star`, `comments`, `time_review`, `status`) VALUES
(1, 2, 5, 5, 'Giày đi rất êm và thoải mái\r\n', '2020-03-09 21:07:29', 0),
(2, 2, 1, 4, 'Giày đi thoáng và rất thoải mái', '2020-03-16 21:07:20', 1),
(3, 2, 1, 3, 'Cũng bình thường', '2020-03-17 21:06:40', 0),
(4, 2, 1, 5, 'Sản phẩm cũng tạm được thôi nhưng mình thích cho 5 sao !\r\n', '2020-03-17 21:05:11', 1),
(5, 2, 1, 1, '                    Không có gì chỉ là ghét nhau tí thôi !', '2020-03-17 21:20:01', 1),
(6, 2, 1, 4, 'I like it !', '2020-04-09 21:01:41', 0),
(7, 2, 5, 5, 'Shoe is very comfortable and i really like it ! Thank a lot ', '2020-04-27 08:37:21', 0),
(8, 2, 5, 4, 'It is ok !', '2020-04-27 08:39:53', 1),
(9, 2, 5, 4, 'nice', '2020-04-27 08:44:41', 1),
(10, 2, 5, 5, 'nice', '2020-04-27 08:45:54', 1),
(11, 2, 5, 5, 'noon', '2020-04-27 08:47:17', 1),
(12, 2, 5, 5, 'moon', '2020-04-27 08:47:51', 1);

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
(2, 5, 8, 1, 42, 1, 5869000),
(3, 4, 7, 1, 40, 6, 3519000),
(4, 1, 1, 1, 36, 6, 4699000),
(5, 3, 6, 1, 36, 6, 7919100),
(6, 1, 4, 2, 43, 6, 4699000),
(7, 3, 6, 1, 42, 7, 7919100),
(8, 1, 1, 1, 42, 8, 4699000),
(9, 5, 9, 1, 39, 9, 5869000),
(10, 3, 6, 1, 42, 10, 7919100),
(11, 3, 6, 1, 42, 11, 7919100),
(12, 1, 1, 1, 42, 11, 4699000),
(13, 3, 6, 1, 36, 12, 7919100),
(14, 1, 1, 1, 36, 13, 4699000),
(15, 4, 7, 1, 42, 14, 3519000),
(16, 5, 8, 1, 42, 14, 5869000),
(17, 1, 1, 1, 42, 15, 4699000),
(18, 1, 1, 1, 42, 16, 4699000),
(19, 1, 4, 1, 43, 17, 4699000),
(20, 1, 2, 1, 43, 18, 4699000),
(21, 1, 1, 1, 43, 19, 4699000),
(22, 1, 1, 1, 42, 20, 4699000),
(23, 3, 6, 1, 41, 20, 7919100),
(24, 1, 1, 1, 42, 20, 4699000),
(25, 3, 6, 1, 42, 21, 7919100),
(26, 1, 1, 2, 42, 21, 4699000),
(27, 1, 4, 1, 42, 22, 4699000),
(28, 5, 8, 2, 41, 22, 5869000),
(29, 5, 8, 3, 42, 23, 5869000),
(30, 5, 8, 3, 42, 24, 5869000),
(31, 3, 6, 1, 42, 24, 7919100),
(32, 1, 2, 1, 42, 24, 4699000);

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
(1, 1, 'Nam Định', 12345678, 'Phạm Công Mạnh', 'Hoàn Thành'),
(3, 6, 'Ngọc Thanh- Kim Động -Hưng Yên', 1234567890, 'Thưởng', 'Hoàn Thành'),
(4, 8, 'Hưng Yên', 1234567890, 'Thưởng', 'Giao Hàng'),
(5, 7, 'Tàu KHựa', 1234567890, 'Nguyễn Tá Thưởng', 'Giao Hàng'),
(6, 9, 'Hưng Yên', 1234567890, 'Thưởng', 'Giao Hàng'),
(7, 10, 'Hưng Yên', 1234567890, 'Thưởng', 'Giao Hàng'),
(8, 11, 'Hưng Yên', 1234567890, 'Thưởng', 'Hoàn Thành'),
(9, 12, 'Hưng Yên', 1234567890, 'Thưởng', 'Giao Hàng'),
(10, 13, 'Hưng Yên', 1234567890, 'Thưởng', 'Giao Hàng'),
(11, 14, 'Hưng Yên', 1234567890, 'Thưởng', 'Giao Hàng'),
(12, 15, 'Hưng Yên', 1234567890, 'Thưởng', 'Giao Hàng'),
(13, 16, 'Hưng Yên', 1234567890, 'Thưởng', 'Giao Hàng'),
(14, 17, 'Hưng Yên', 1234567890, 'Thưởng', 'Giao Hàng'),
(15, 18, 'Hưng Yên', 1234567890, 'Thưởng', 'Giao Hàng'),
(16, 19, 'Nam Định- Việt Nam', 987654321, 'Mạnh', 'Giao Hàng'),
(17, 20, 'Nam Định- Việt Nam', 987654321, 'Mạnh', 'Giao Hàng'),
(18, 21, 'Nam Định- Việt Nam', 987654321, 'Mạnh', 'Hoàn Thành'),
(19, 22, 'Nam Định- Việt Nam', 987654321, 'Mạnh', 'Giao Hàng'),
(20, 24, 'Nam Định- Việt Nam', 123456789, 'Thưởng', 'Giao Hàng');

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
(1, 'Nike React Infinity Run Flyknit', 'Both', 'Running', 'Waterproof', 4699000, NULL, 0, 'Snacker', 'Shoes suitable for every one,!'),
(3, 'Nike Mercurial Superfly 7 Elite MDS FG', 'Man', 'Football', 'Reflection', 8799000, 'Cristiano Ronaldo', 10, 'Boot', 'Has alot of Surface and has durable with time\r\n'),
(4, 'Nike Air Max 200', 'Woman', 'Training', 'Waterproof', 3519000, '', 0, 'Sandals', 'Comfortable for Woman and has style perfect\r\n'),
(5, 'LeBron 7 QS', 'Man', 'Basketball', 'Reflection', 5869000, 'LeBron James', 0, 'Boot', 'Make your head-turning journey to the top comfortable. Built strong and sleek, the LeBron 7 QS features a mix of materials on the upper for a look that lasts. Metal accents and multiple LeBron crests celebrate a king, while full-length cushioning graces your every step.'),
(6, 'Giày Test', 'Both', 'Running', 'None', 1234000, NULL, 0, 'Boot', 'test'),
(8, 'Air Jordan XXXIV PF', 'Man', 'Basketball', 'Reflection', 5129000, NULL, 0, 'Snacker', 'The Air Jordan XXXIV PF continues the legacy of a cultural icon. Light, responsive sculpted'),
(10, 'Nike Air Max Plus III', 'Man', 'Life Style', 'Reflection', 4699000, NULL, 0, 'Snacker', 'Product has many color for customer using and suitable with a lot of people has detail style'),
(11, 'Nike Air VaporMax Flyknit 3', 'Man', 'Basketball', 'Reflection', 3519000, NULL, 0, 'Snacker', 'The Air Jordan 8 made its debut during MJ\'s \'three-peat\' 1992–93 championship season. The Air Jordan 8 Retro features the same moulded details, midfoot straps and cushioned comfort that quickly established the original as a fan favourite.'),
(12, 'Nike Epic Phantom React AIR Cody Hudson', 'Man', 'Running', 'Waterproof', 5129000, NULL, 10, 'Snacker', 'This product founder and creative director Matthew M. Williams is known for sustainability, using his creative direction to push fashion into new spaces. His work on the Nike x MMW Free TR 3 continues that trend, delivering a design that is both dynamic enough for the gym and equally resilient in extreme urban climates'),
(13, 'Nike Free Metcon 3', 'Both', 'Life Style', 'Reflection', 3219000, NULL, 0, 'Sandals', 'The legend lives on in the Nike Free Metcon 3—a modern take on the iconic AF1 that blends classic style with sweet details. A stitched tag logo runs down the tongue while over-branding throughout reinforces Nike heritage'),
(14, 'Nike Mercurial Superfly 7 Academy MG', 'Both', 'Life Style', 'None', 4299000, NULL, 0, 'Sandals', 'The Nike Mercurial Superfly 7 Academy MG Shoe draws inspiration from the Monarch franchise and pushes it into today with a futuristic heel counter and plush tongue for additional comfort.'),
(15, 'Nike x Undercover React', 'Woman', 'Life Style', 'Reflection', 3299000, NULL, 0, 'Boot', 'Clean lines, versatile and timeless—the people\'s shoe returns with the Nike x Undercover React. Featuring the same iconic Waffle sole, stitched overlays and classic TPU accents you\'ve come to love, it lets you walk among the pantheon of Air.'),
(16, 'Nike Zoom Fly 3', 'Woman', 'Life Style', 'Reflection', 2999000, NULL, 0, 'Snacker', 'Clean lines, versatile and timeless—the people\'s shoe returns with the Nike Zoom Fly 3. Featuring the same iconic Waffle sole, stitched overlays and classic TPU accents you\'ve come to love, it lets you walk among the pantheon of Air.'),
(17, 'Nike MX-720-818', 'Both', 'Life Style', 'Reflection', 5589000, NULL, 0, 'Snacker', 'Float on Air with the Nike MX-720-818. Featuring a quilted upper inspired by space suits and the largest Air unit to date, it adds a futuristic look to your stride. The mesh upper keeps your feet cool while the translucent sole has a burst of colour reminiscent of distant galaxies.');

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
(2, 1, 'Orange'),
(4, 1, 'White'),
(5, 1, 'Red'),
(6, 3, 'Blue'),
(7, 4, 'Purple'),
(8, 5, 'Blue'),
(9, 5, 'Gold'),
(10, 8, 'Black'),
(11, 8, 'Grey'),
(12, 8, 'Red'),
(13, 8, 'White'),
(15, 10, 'Black'),
(16, 10, 'Blue'),
(17, 11, 'White'),
(18, 11, 'Blue'),
(19, 11, 'Grey'),
(20, 12, 'Black'),
(21, 13, 'Black'),
(22, 13, 'White'),
(23, 13, 'Red'),
(24, 14, 'Blue'),
(25, 14, 'Red'),
(26, 15, 'Black'),
(27, 15, 'Orange'),
(28, 16, 'White'),
(29, 16, 'Grey'),
(30, 16, 'Orange'),
(31, 16, 'Purple'),
(32, 17, 'White'),
(33, 17, 'Green');

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
(2, 2, '1/Laser Orange/react-infinity-run-flyknit-running-shoe-ZjGHFz.jpg'),
(3, 4, '1/White/react-infinity-run-flyknit-running-shoe-ZjGHFz.jpg'),
(4, 5, '1/Red/react-infinity-run-flyknit-running-shoe-ZjGHFz (1).jpg'),
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
(42, 9, '4/Gold White/31334267-e41f-45f1-a46f-dc6edad5ddcb.webp'),
(43, 10, '8/Black/3d7b03ea-3466-4056-a344-3492e88f8b6c.webp'),
(45, 11, '8/Grey/760e84b0-2c43-40e9-b09c-20f445d45f59.webp'),
(56, 11, '8/Grey/MG_6870-150x150.jpg'),
(60, 10, '8/Black/MG_5858-150x150.jpg'),
(61, 10, '8/Black/MG_5859-150x150.jpg'),
(62, 10, '8/Black/MG_5860-150x150.jpg'),
(63, 10, '8/Black/MG_5861-150x150.jpg'),
(101, 15, '10/Black/air-max-plus-iii-shoe-Qw64gh_1.jpg'),
(102, 15, '10/Black/air-max-plus-iii-shoe-Qw64gh_2.jpg'),
(103, 15, '10/Black/air-max-plus-iii-shoe-Qw64gh_3.jpg'),
(104, 15, '10/Black/air-max-plus-iii-shoe-Qw64gh_4.jpg'),
(105, 15, '10/Black/air-max-plus-iii-shoe-Qw64gh_5.jpg'),
(106, 15, '10/Black/air-max-plus-iii-shoe-Qw64gh_6.jpg'),
(107, 16, '10/Blue/air-max-plus-iii-shoe-Qw64gh_11.jpg'),
(108, 16, '10/Blue/air-max-plus-iii-shoe-Qw64gh_12.jpg'),
(109, 16, '10/Blue/air-max-plus-iii-shoe-Qw64gh_13.jpg'),
(110, 16, '10/Blue/air-max-plus-iii-shoe-Qw64gh_14.jpg'),
(111, 16, '10/Blue/air-max-plus-iii-shoe-Qw64gh_15.jpg'),
(112, 16, '10/Blue/air-max-plus-iii-shoe-Qw64gh_16.jpg'),
(113, 17, '11/White/air-vapormax-flyknit-3-shoe-xr9cgR_21.jpg'),
(114, 17, '11/White/air-vapormax-flyknit-3-shoe-xr9cgR_22.jpg'),
(115, 17, '11/White/air-vapormax-flyknit-3-shoe-xr9cgR_23.jpg'),
(116, 17, '11/White/air-vapormax-flyknit-3-shoe-xr9cgR_24.jpg'),
(117, 17, '11/White/air-vapormax-flyknit-3-shoe-xr9cgR_25.jpg'),
(118, 17, '11/White/air-vapormax-flyknit-3-shoe-xr9cgR_26.jpg'),
(119, 18, '11/Blue/air-vapormax-flyknit-3-shoe-xr9cgR_1.jpg'),
(120, 18, '11/Blue/air-vapormax-flyknit-3-shoe-xr9cgR_2.jpg'),
(121, 18, '11/Blue/air-vapormax-flyknit-3-shoe-xr9cgR_3.jpg'),
(122, 18, '11/Blue/air-vapormax-flyknit-3-shoe-xr9cgR_4.jpg'),
(123, 18, '11/Blue/air-vapormax-flyknit-3-shoe-xr9cgR_5.jpg'),
(124, 18, '11/Blue/air-vapormax-flyknit-3-shoe-xr9cgR_6.jpg'),
(125, 19, '11/Grey/air-vapormax-flyknit-3-shoe-xr9cgR_11.jpg'),
(126, 19, '11/Grey/air-vapormax-flyknit-3-shoe-xr9cgR_12.jpg'),
(127, 19, '11/Grey/air-vapormax-flyknit-3-shoe-xr9cgR_13.jpg'),
(128, 19, '11/Grey/air-vapormax-flyknit-3-shoe-xr9cgR_14.jpg'),
(129, 19, '11/Grey/air-vapormax-flyknit-3-shoe-xr9cgR_15.jpg'),
(130, 19, '11/Grey/air-vapormax-flyknit-3-shoe-xr9cgR_16.jpg'),
(131, 20, '12/Black/epic-phantom-react-air-cody-hudson-running-shoe-ctX7Zl_1.jpg'),
(132, 20, '12/Black/epic-phantom-react-air-cody-hudson-running-shoe-ctX7Zl_2.jpg'),
(133, 20, '12/Black/epic-phantom-react-air-cody-hudson-running-shoe-ctX7Zl_3.jpg'),
(134, 20, '12/Black/epic-phantom-react-air-cody-hudson-running-shoe-ctX7Zl_4.jpg'),
(135, 20, '12/Black/epic-phantom-react-air-cody-hudson-running-shoe-ctX7Zl_5.jpg'),
(136, 20, '12/Black/epic-phantom-react-air-cody-hudson-running-shoe-ctX7Zl_6.jpg'),
(137, 21, '13/Black/free-metcon-3-training-shoe-cJBhpW_11.jpg'),
(138, 21, '13/Black/free-metcon-3-training-shoe-cJBhpW_12.jpg'),
(139, 21, '13/Black/free-metcon-3-training-shoe-cJBhpW_13.jpg'),
(140, 21, '13/Black/free-metcon-3-training-shoe-cJBhpW_14.jpg'),
(141, 21, '13/Black/free-metcon-3-training-shoe-cJBhpW_15.jpg'),
(142, 21, '13/Black/free-metcon-3-training-shoe-cJBhpW_16.jpg'),
(143, 22, '13/White/free-metcon-3-training-shoe-cJBhpW_31.jpg'),
(144, 22, '13/White/free-metcon-3-training-shoe-cJBhpW_32.jpg'),
(145, 22, '13/White/free-metcon-3-training-shoe-cJBhpW_33.jpg'),
(146, 22, '13/White/free-metcon-3-training-shoe-cJBhpW_34.jpg'),
(147, 22, '13/White/free-metcon-3-training-shoe-cJBhpW_35.jpg'),
(148, 22, '13/White/free-metcon-3-training-shoe-cJBhpW_36.jpg'),
(149, 23, '13/Red/free-metcon-3-training-shoe-cJBhpW_21.jpg'),
(150, 23, '13/Red/free-metcon-3-training-shoe-cJBhpW_22.jpg'),
(151, 23, '13/Red/free-metcon-3-training-shoe-cJBhpW_23.jpg'),
(152, 23, '13/Red/free-metcon-3-training-shoe-cJBhpW_24.jpg'),
(153, 23, '13/Red/free-metcon-3-training-shoe-cJBhpW_25.jpg'),
(154, 23, '13/Red/free-metcon-3-training-shoe-cJBhpW_26.jpg'),
(155, 24, '14/Blue/mercurial-superfly-7-academy-mg-multi-ground-football-boot-9c8jVQ_11.jpg'),
(156, 24, '14/Blue/mercurial-superfly-7-academy-mg-multi-ground-football-boot-9c8jVQ_12.jpg'),
(157, 24, '14/Blue/mercurial-superfly-7-academy-mg-multi-ground-football-boot-9c8jVQ_13.jpg'),
(158, 24, '14/Blue/mercurial-superfly-7-academy-mg-multi-ground-football-boot-9c8jVQ_14.jpg'),
(159, 24, '14/Blue/mercurial-superfly-7-academy-mg-multi-ground-football-boot-9c8jVQ_15.jpg'),
(160, 24, '14/Blue/mercurial-superfly-7-academy-mg-multi-ground-football-boot-9c8jVQ_16.jpg'),
(161, 24, '14/Blue/mercurial-superfly-7-academy-mg-multi-ground-football-boot-9c8jVQ_17.jpg'),
(162, 25, '14/Red/mercurial-superfly-7-academy-mg-multi-ground-football-boot-9c8jVQ_21.jpg'),
(163, 25, '14/Red/mercurial-superfly-7-academy-mg-multi-ground-football-boot-9c8jVQ_22.jpg'),
(164, 25, '14/Red/mercurial-superfly-7-academy-mg-multi-ground-football-boot-9c8jVQ_23.jpg'),
(165, 25, '14/Red/mercurial-superfly-7-academy-mg-multi-ground-football-boot-9c8jVQ_24.jpg'),
(166, 25, '14/Red/mercurial-superfly-7-academy-mg-multi-ground-football-boot-9c8jVQ_25.jpg'),
(167, 25, '14/Red/mercurial-superfly-7-academy-mg-multi-ground-football-boot-9c8jVQ_26.jpg'),
(168, 25, '14/Red/mercurial-superfly-7-academy-mg-multi-ground-football-boot-9c8jVQ_27.jpg'),
(169, 26, '15/Black/undercover-react-boot-727MRT_11.jpg'),
(170, 26, '15/Black/undercover-react-boot-727MRT_12.jpg'),
(171, 26, '15/Black/undercover-react-boot-727MRT_13.jpg'),
(172, 26, '15/Black/undercover-react-boot-727MRT_14.jpg'),
(173, 26, '15/Black/undercover-react-boot-727MRT_15.jpg'),
(174, 26, '15/Black/undercover-react-boot-727MRT_16.jpg'),
(175, 27, '15/Orange/undercover-react-boot-727MRT_21.jpg'),
(176, 27, '15/Orange/undercover-react-boot-727MRT_22.jpg'),
(177, 27, '15/Orange/undercover-react-boot-727MRT_23.jpg'),
(178, 27, '15/Orange/undercover-react-boot-727MRT_24.jpg'),
(179, 27, '15/Orange/undercover-react-boot-727MRT_25.jpg'),
(180, 27, '15/Orange/undercover-react-boot-727MRT_26.jpg'),
(187, 28, '16/White/zoom-fly-3-running-shoe-M5N4X5_41.jpg'),
(188, 28, '16/White/zoom-fly-3-running-shoe-M5N4X5_42.jpg'),
(189, 28, '16/White/zoom-fly-3-running-shoe-M5N4X5_43.jpg'),
(190, 28, '16/White/zoom-fly-3-running-shoe-M5N4X5_44.jpg'),
(191, 28, '16/White/zoom-fly-3-running-shoe-M5N4X5_45.jpg'),
(192, 28, '16/White/zoom-fly-3-running-shoe-M5N4X5_46.jpg'),
(193, 29, '16/Grey/zoom-fly-3-running-shoe-M5N4X5_11.jpg'),
(194, 29, '16/Grey/zoom-fly-3-running-shoe-M5N4X5_12.jpg'),
(195, 29, '16/Grey/zoom-fly-3-running-shoe-M5N4X5_13.jpg'),
(196, 29, '16/Grey/zoom-fly-3-running-shoe-M5N4X5_14.jpg'),
(197, 29, '16/Grey/zoom-fly-3-running-shoe-M5N4X5_15.jpg'),
(198, 29, '16/Grey/zoom-fly-3-running-shoe-M5N4X5_16.jpg'),
(199, 30, '16/Orange/zoom-fly-3-running-shoe-M5N4X5_21.jpg'),
(200, 30, '16/Orange/zoom-fly-3-running-shoe-M5N4X5_22.jpg'),
(201, 30, '16/Orange/zoom-fly-3-running-shoe-M5N4X5_23.jpg'),
(202, 30, '16/Orange/zoom-fly-3-running-shoe-M5N4X5_24.jpg'),
(203, 30, '16/Orange/zoom-fly-3-running-shoe-M5N4X5_25.jpg'),
(204, 30, '16/Orange/zoom-fly-3-running-shoe-M5N4X5_26.jpg'),
(205, 31, '16/Purple/zoom-fly-3-running-shoe-M5N4X5_31.jpg'),
(206, 31, '16/Purple/zoom-fly-3-running-shoe-M5N4X5_32.jpg'),
(207, 31, '16/Purple/zoom-fly-3-running-shoe-M5N4X5_33.jpg'),
(208, 31, '16/Purple/zoom-fly-3-running-shoe-M5N4X5_34.jpg'),
(209, 31, '16/Purple/zoom-fly-3-running-shoe-M5N4X5_35.jpg'),
(210, 31, '16/Purple/zoom-fly-3-running-shoe-M5N4X5_36.jpg'),
(211, 32, '17/White/mx-720-818-shoe-s6Cxx2_21.jpg'),
(212, 32, '17/White/mx-720-818-shoe-s6Cxx2_22.jpg'),
(213, 32, '17/White/mx-720-818-shoe-s6Cxx2_23.jpg'),
(214, 32, '17/White/mx-720-818-shoe-s6Cxx2_24.jpg'),
(215, 32, '17/White/mx-720-818-shoe-s6Cxx2_25.jpg'),
(216, 32, '17/White/mx-720-818-shoe-s6Cxx2_26.jpg'),
(217, 33, '17/Green/mx-720-818-shoe-s6Cxx2_11.jpg'),
(218, 33, '17/Green/mx-720-818-shoe-s6Cxx2_12.jpg'),
(219, 33, '17/Green/mx-720-818-shoe-s6Cxx2_13.jpg'),
(220, 33, '17/Green/mx-720-818-shoe-s6Cxx2_14.jpg'),
(221, 33, '17/Green/mx-720-818-shoe-s6Cxx2_15.jpg'),
(222, 33, '17/Green/mx-720-818-shoe-s6Cxx2_16.jpg');

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
(11, 5, 'Multi Ground'),
(13, 8, 'Artificial Grass'),
(14, 8, 'Multi Ground'),
(15, 8, 'Indoor'),
(16, 8, 'Grass'),
(17, 1, 'Soft Ground'),
(18, 3, 'Soft Ground'),
(19, 10, 'Grass'),
(20, 10, 'Multi Ground'),
(21, 10, 'Indoor'),
(22, 11, 'Firm Ground'),
(23, 11, 'Artificial Grass'),
(24, 11, 'Multi Ground'),
(25, 12, 'Grass'),
(26, 12, 'Firm Ground'),
(27, 12, 'Artificial Grass'),
(28, 12, 'Indoor'),
(29, 13, 'Grass'),
(30, 13, 'Artificial Grass'),
(31, 13, 'Multi Ground'),
(32, 14, 'Grass'),
(33, 14, 'Multi Ground'),
(34, 14, 'Indoor'),
(35, 14, 'Soft Ground'),
(36, 15, 'Multi Ground'),
(37, 15, 'Indoor'),
(38, 15, 'Soft Ground'),
(39, 16, 'Multi Ground'),
(40, 16, 'Indoor'),
(41, 16, 'Soft Ground'),
(42, 17, 'Artificial Grass'),
(43, 17, 'Multi Ground'),
(44, 17, 'Soft Ground');

-- --------------------------------------------------------

--
-- Table structure for table `user_order`
--

CREATE TABLE `user_order` (
  `id_order` int(11) NOT NULL,
  `id_user` int(11) NOT NULL,
  `order_quantity` int(11) NOT NULL,
  `total_price` float NOT NULL,
  `time_order` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user_order`
--

INSERT INTO `user_order` (`id_order`, `id_user`, `order_quantity`, `total_price`, `time_order`) VALUES
(1, 2, 2, 9388000, '2020-02-02 19:10:00'),
(6, 2, 5, 25535100, '2020-03-15 14:37:55'),
(7, 2, 1, 7919100, '2020-03-15 14:56:43'),
(8, 2, 1, 4699000, '2020-03-15 14:58:57'),
(9, 2, 1, 5869000, '2020-03-15 16:06:45'),
(10, 2, 1, 7919100, '2020-03-16 19:44:46'),
(11, 2, 2, 12618100, '2020-03-16 21:57:22'),
(12, 1, 1, 7919100, '2020-03-16 22:03:37'),
(13, 1, 1, 4699000, '2020-03-16 22:04:59'),
(14, 1, 2, 9388000, '2020-03-16 22:06:00'),
(15, 1, 1, 4699000, '2020-03-16 22:07:07'),
(16, 2, 1, 4699000, '2020-03-16 22:08:12'),
(17, 1, 1, 4699000, '2020-03-16 22:10:41'),
(18, 2, 1, 4699000, '2020-03-16 22:12:11'),
(19, 2, 1, 4699000, '2020-03-23 08:42:20'),
(20, 2, 3, 17317100, '2020-03-24 16:11:04'),
(21, 2, 3, 17317100, '2020-04-01 07:16:10'),
(22, 2, 3, 16437000, '2020-04-10 16:47:23'),
(23, 2, 5, 30225100, '2020-04-27 08:53:44'),
(24, 2, 5, 30225100, '2020-04-27 08:54:34');

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
  MODIFY `id_account` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `cart`
--
ALTER TABLE `cart`
  MODIFY `id_cart` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `cart_detail`
--
ALTER TABLE `cart_detail`
  MODIFY `id_cart_detail` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=42;

--
-- AUTO_INCREMENT for table `comment`
--
ALTER TABLE `comment`
  MODIFY `id_comment` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `order_detail`
--
ALTER TABLE `order_detail`
  MODIFY `id_order_detail` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT for table `ship`
--
ALTER TABLE `ship`
  MODIFY `id_ship` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `shoes`
--
ALTER TABLE `shoes`
  MODIFY `id_shoes` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `shoes_color`
--
ALTER TABLE `shoes_color`
  MODIFY `id_shoes_color` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT for table `shoes_color_image`
--
ALTER TABLE `shoes_color_image`
  MODIFY `id_shoes_color_image` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=223;

--
-- AUTO_INCREMENT for table `shoes_surface`
--
ALTER TABLE `shoes_surface`
  MODIFY `id_shoes_surface` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=45;

--
-- AUTO_INCREMENT for table `user_order`
--
ALTER TABLE `user_order`
  MODIFY `id_order` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

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
