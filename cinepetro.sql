-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 22/06/2025 às 21:00
-- Versão do servidor: 10.4.32-MariaDB
-- Versão do PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `cinepetro`
--

-- --------------------------------------------------------

--
-- Estrutura para tabela `episodes`
--

CREATE TABLE `episodes` (
  `id` int(11) NOT NULL,
  `series_id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `season_number` int(11) DEFAULT NULL,
  `episode_number` int(11) DEFAULT NULL,
  `duration` int(11) DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `deleted_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `genres`
--

CREATE TABLE `genres` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `deleted_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `genres`
--

INSERT INTO `genres` (`id`, `name`, `created_at`, `updated_at`, `deleted_at`) VALUES
(1, 'Ação', '2025-06-09 17:18:41', '2025-06-09 17:18:41', NULL),
(2, 'Aventura', '2025-06-09 17:18:41', '2025-06-09 17:18:41', NULL),
(3, 'Animação', '2025-06-09 17:18:41', '2025-06-09 17:18:41', NULL),
(4, 'Comédia', '2025-06-09 17:18:41', '2025-06-09 17:18:41', NULL),
(5, 'Comédia Romântica', '2025-06-09 17:18:41', '2025-06-09 17:18:41', NULL),
(6, 'Crime', '2025-06-09 17:18:41', '2025-06-09 17:18:41', NULL),
(7, 'Documentário', '2025-06-09 17:18:41', '2025-06-09 17:18:41', NULL),
(8, 'Drama', '2025-06-09 17:18:41', '2025-06-09 17:18:41', NULL),
(9, 'Épico', '2025-06-09 17:18:41', '2025-06-09 17:18:41', NULL),
(10, 'Espionagem', '2025-06-09 17:18:41', '2025-06-09 17:18:41', NULL),
(11, 'Faroeste', '2025-06-09 17:18:41', '2025-06-09 17:18:41', NULL),
(12, 'Fantasia', '2025-06-09 17:18:41', '2025-06-09 17:18:41', NULL),
(13, 'Ficção Científica', '2025-06-09 17:18:41', '2025-06-09 17:18:41', NULL),
(14, 'Guerra', '2025-06-09 17:18:41', '2025-06-09 17:18:41', NULL),
(15, 'História', '2025-06-09 17:18:41', '2025-06-09 17:18:41', NULL),
(16, 'Mistério', '2025-06-09 17:18:41', '2025-06-09 17:18:41', NULL),
(17, 'Musical', '2025-06-09 17:18:41', '2025-06-09 17:18:41', NULL),
(18, 'Policial', '2025-06-09 17:18:41', '2025-06-09 17:18:41', NULL),
(19, 'Romance', '2025-06-09 17:18:41', '2025-06-09 17:18:41', NULL),
(20, 'Suspense', '2025-06-09 17:18:41', '2025-06-09 17:18:41', NULL),
(21, 'Terror', '2025-06-09 17:18:41', '2025-06-09 17:18:41', NULL),
(22, 'Thriller Psicológico', '2025-06-09 17:18:41', '2025-06-09 17:18:41', NULL),
(23, 'Biografia', '2025-06-09 17:18:41', '2025-06-09 17:18:41', NULL),
(24, 'Filme Noir', '2025-06-09 17:18:41', '2025-06-09 17:18:41', NULL),
(25, 'Infantil', '2025-06-09 17:18:41', '2025-06-09 17:18:41', NULL),
(26, 'Religioso', '2025-06-09 17:18:41', '2025-06-09 17:18:41', NULL),
(27, 'Reality Show', '2025-06-09 17:18:41', '2025-06-09 17:18:41', NULL);

-- --------------------------------------------------------

--
-- Estrutura para tabela `movies`
--

CREATE TABLE `movies` (
  `id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `year` int(11) DEFAULT NULL,
  `duration` int(11) DEFAULT NULL,
  `poster` varchar(255) DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `deleted_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `movies`
--

INSERT INTO `movies` (`id`, `title`, `description`, `year`, `duration`, `poster`, `created_by`, `created_at`, `updated_at`, `deleted_at`) VALUES
(17, 'Vingadores Ultimato', 'Em Vingadores: Ultimato, após Thanos eliminar metade das criaturas vivas em Vingadores: Guerra Infinita, os heróis precisam lidar com a dor da perda de amigos e seus entes queridos. Com Tony Stark (Robert Downey Jr.) vagando perdido no espaço sem água nem comida, o Capitão América/Steve Rogers (Chris Evans) e a Viúva Negra/Natasha Romanov (Scarlett Johansson) precisam liderar a resistência contra o titã louco.', 2019, 181, 'posters/1750365454.948539_vingadores_ultimato.jpeg', 1, '2025-06-19 17:37:34', '2025-06-19 17:37:34', NULL);

-- --------------------------------------------------------

--
-- Estrutura para tabela `movie_genre`
--

CREATE TABLE `movie_genre` (
  `movie_id` int(11) NOT NULL,
  `genre_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `movie_genre`
--

INSERT INTO `movie_genre` (`movie_id`, `genre_id`) VALUES
(17, 1),
(17, 2),
(17, 13);

-- --------------------------------------------------------

--
-- Estrutura para tabela `series`
--

CREATE TABLE `series` (
  `id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `start_year` int(11) DEFAULT NULL,
  `end_year` int(11) DEFAULT NULL,
  `poster` varchar(255) DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `deleted_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `serie_genre`
--

CREATE TABLE `serie_genre` (
  `series_id` int(11) NOT NULL,
  `genre_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(150) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `is_admin` tinyint(1) DEFAULT 0,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `deleted_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `password_hash`, `is_admin`, `created_at`, `updated_at`, `deleted_at`) VALUES
(1, 'Alisson Lima de Souza', 'admin@example.com', '$2b$12$ypmD2Y3WGW/01SZ6CmlEVeyG.zL98E5LGwL21NqlecLQ2gvQON82S', 0, '2025-06-09 16:26:58', '2025-06-10 14:52:26', NULL);

-- --------------------------------------------------------

--
-- Estrutura para tabela `watch_progress`
--

CREATE TABLE `watch_progress` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `movie_id` int(11) DEFAULT NULL,
  `episode_id` int(11) DEFAULT NULL,
  `time_seconds` float NOT NULL DEFAULT 0,
  `updated_at` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `watch_progress`
--

INSERT INTO `watch_progress` (`id`, `user_id`, `movie_id`, `episode_id`, `time_seconds`, `updated_at`) VALUES
(1, 1, 17, NULL, 163, '2025-06-21 14:45:20'),
(2, 1, 17, NULL, 20, '2025-06-21 14:42:29');

--
-- Índices para tabelas despejadas
--

--
-- Índices de tabela `episodes`
--
ALTER TABLE `episodes`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uc_episode` (`series_id`,`season_number`,`episode_number`),
  ADD KEY `created_by` (`created_by`);

--
-- Índices de tabela `genres`
--
ALTER TABLE `genres`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Índices de tabela `movies`
--
ALTER TABLE `movies`
  ADD PRIMARY KEY (`id`),
  ADD KEY `created_by` (`created_by`);

--
-- Índices de tabela `movie_genre`
--
ALTER TABLE `movie_genre`
  ADD PRIMARY KEY (`movie_id`,`genre_id`),
  ADD KEY `genre_id` (`genre_id`);

--
-- Índices de tabela `series`
--
ALTER TABLE `series`
  ADD PRIMARY KEY (`id`),
  ADD KEY `created_by` (`created_by`);

--
-- Índices de tabela `serie_genre`
--
ALTER TABLE `serie_genre`
  ADD PRIMARY KEY (`series_id`,`genre_id`),
  ADD KEY `genre_id` (`genre_id`);

--
-- Índices de tabela `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Índices de tabela `watch_progress`
--
ALTER TABLE `watch_progress`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_user_movie_episode` (`user_id`,`movie_id`,`episode_id`),
  ADD KEY `movie_id` (`movie_id`),
  ADD KEY `episode_id` (`episode_id`);

--
-- AUTO_INCREMENT para tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `episodes`
--
ALTER TABLE `episodes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT de tabela `genres`
--
ALTER TABLE `genres`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- AUTO_INCREMENT de tabela `movies`
--
ALTER TABLE `movies`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT de tabela `series`
--
ALTER TABLE `series`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de tabela `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de tabela `watch_progress`
--
ALTER TABLE `watch_progress`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Restrições para tabelas despejadas
--

--
-- Restrições para tabelas `episodes`
--
ALTER TABLE `episodes`
  ADD CONSTRAINT `episodes_ibfk_1` FOREIGN KEY (`series_id`) REFERENCES `series` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `episodes_ibfk_2` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`);

--
-- Restrições para tabelas `movies`
--
ALTER TABLE `movies`
  ADD CONSTRAINT `movies_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`);

--
-- Restrições para tabelas `movie_genre`
--
ALTER TABLE `movie_genre`
  ADD CONSTRAINT `movie_genre_ibfk_1` FOREIGN KEY (`movie_id`) REFERENCES `movies` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `movie_genre_ibfk_2` FOREIGN KEY (`genre_id`) REFERENCES `genres` (`id`) ON DELETE CASCADE;

--
-- Restrições para tabelas `series`
--
ALTER TABLE `series`
  ADD CONSTRAINT `series_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`);

--
-- Restrições para tabelas `serie_genre`
--
ALTER TABLE `serie_genre`
  ADD CONSTRAINT `serie_genre_ibfk_1` FOREIGN KEY (`series_id`) REFERENCES `series` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `serie_genre_ibfk_2` FOREIGN KEY (`genre_id`) REFERENCES `genres` (`id`) ON DELETE CASCADE;

--
-- Restrições para tabelas `watch_progress`
--
ALTER TABLE `watch_progress`
  ADD CONSTRAINT `watch_progress_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `watch_progress_ibfk_2` FOREIGN KEY (`movie_id`) REFERENCES `movies` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `watch_progress_ibfk_3` FOREIGN KEY (`episode_id`) REFERENCES `episodes` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
