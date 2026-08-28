-- ===================================================
-- Esquema do Banco de Dados - Sistema de Planos de Aula
-- Compatibilidade: MySQL 8.0+ / MariaDB 10.4+
-- ===================================================

CREATE DATABASE IF NOT EXISTS plano_de_aula CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE plano_de_aula;

-- 1. Tabela de Usuários (Administradores e Professores)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(191) NOT NULL UNIQUE,
    phone VARCHAR(30) NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'professor') NOT NULL DEFAULT 'professor',
    status ENUM('pendente', 'ativo') NOT NULL DEFAULT 'pendente',
    reset_token_hash VARCHAR(255) NULL,
    reset_token_expires_at DATETIME NULL,
    approved_at DATETIME NULL,
    approved_by INT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (approved_by) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB;

-- 2. Tabela de Componentes Curriculares (Disciplinas)
CREATE TABLE IF NOT EXISTS subjects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    education_level ENUM('fundamental', 'medio') NOT NULL,
    active BOOLEAN DEFAULT TRUE,
    UNIQUE KEY uq_subject_level (name, education_level)
) ENGINE=InnoDB;

-- 3. Tabela de Documentos Curriculares (Histórico de PDFs Importados)
CREATE TABLE IF NOT EXISTS curriculum_documents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    subject_id INT NOT NULL,
    education_level ENUM('fundamental', 'medio') NOT NULL,
    grade VARCHAR(50) NOT NULL,
    document_year INT NOT NULL DEFAULT 2026,
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    total_lessons INT DEFAULT 0,
    status ENUM('processado', 'erro') DEFAULT 'processado',
    imported_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 4. Tabela do Escopo-Sequência (Aulas extraídas dos PDFs)
CREATE TABLE IF NOT EXISTS scope_lessons (
    id INT AUTO_INCREMENT PRIMARY KEY,
    subject_id INT NOT NULL,
    education_level ENUM('fundamental', 'medio') NOT NULL,
    grade VARCHAR(50) NOT NULL,
    bimester INT NOT NULL,
    lesson_number INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    learning_objectives TEXT NOT NULL,
    skills VARCHAR(255) NULL,
    essential_learning_code VARCHAR(50) NULL,
    essential_learning TEXT NULL,
    year INT NOT NULL DEFAULT 2026,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE,
    UNIQUE KEY uq_scope_lesson_entry (subject_id, education_level, grade, bimester, lesson_number, year)
) ENGINE=InnoDB;

-- 5. Tabela de Planos de Aula dos Professores
CREATE TABLE IF NOT EXISTS lesson_plans (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    subject_id INT NOT NULL,
    education_level ENUM('fundamental', 'medio') NOT NULL,
    grade VARCHAR(50) NOT NULL,
    bimester INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    number_of_lessons INT NOT NULL DEFAULT 1,
    selected_lesson_titles TEXT NULL,
    contents TEXT NULL,
    objectives TEXT NULL,
    skills TEXT NULL,
    essential_learnings TEXT NULL,
    resources TEXT NULL,
    methodology TEXT NULL,
    evaluation TEXT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE RESTRICT
) ENGINE=InnoDB;

-- 6. Tabela de Turmas Vinculadas ao Plano
CREATE TABLE IF NOT EXISTS lesson_plan_classes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    lesson_plan_id INT NOT NULL,
    class_name VARCHAR(20) NOT NULL,
    FOREIGN KEY (lesson_plan_id) REFERENCES lesson_plans(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 7. Tabela de Aulas do Escopo Vinculadas ao Plano
CREATE TABLE IF NOT EXISTS lesson_plan_lessons (
    id INT AUTO_INCREMENT PRIMARY KEY,
    lesson_plan_id INT NOT NULL,
    scope_lesson_id INT NOT NULL,
    FOREIGN KEY (lesson_plan_id) REFERENCES lesson_plans(id) ON DELETE CASCADE,
    FOREIGN KEY (scope_lesson_id) REFERENCES scope_lessons(id) ON DELETE RESTRICT
) ENGINE=InnoDB;

