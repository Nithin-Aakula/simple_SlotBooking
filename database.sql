-- ============================================================
-- Slot Booking System — Database Schema
-- ============================================================

CREATE DATABASE IF NOT EXISTS booking_system;
USE booking_system;

-- -----------------------------------------------------------
-- Slots table
-- -----------------------------------------------------------
CREATE TABLE IF NOT EXISTS slots (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    start_time DATETIME     NOT NULL,
    end_time   DATETIME     NOT NULL,
    is_booked  BOOLEAN      NOT NULL DEFAULT FALSE
);

-- -----------------------------------------------------------
-- Bookings table
-- -----------------------------------------------------------
CREATE TABLE IF NOT EXISTS bookings (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    slot_id    INT          NOT NULL,
    user_name  VARCHAR(120) NOT NULL,
    user_email VARCHAR(255) NOT NULL,
    created_at DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_bookings_slot
        FOREIGN KEY (slot_id) REFERENCES slots(id)
        ON DELETE CASCADE
);

-- -----------------------------------------------------------
-- Seed sample slots (today + tomorrow, 1-hour blocks)
-- -----------------------------------------------------------
INSERT INTO slots (start_time, end_time) VALUES
    (CONCAT(CURDATE(), ' 09:00:00'), CONCAT(CURDATE(), ' 10:00:00')),
    (CONCAT(CURDATE(), ' 10:00:00'), CONCAT(CURDATE(), ' 11:00:00')),
    (CONCAT(CURDATE(), ' 11:00:00'), CONCAT(CURDATE(), ' 12:00:00')),
    (CONCAT(CURDATE(), ' 13:00:00'), CONCAT(CURDATE(), ' 14:00:00')),
    (CONCAT(CURDATE(), ' 14:00:00'), CONCAT(CURDATE(), ' 15:00:00')),
    (CONCAT(CURDATE(), ' 15:00:00'), CONCAT(CURDATE(), ' 16:00:00')),
    (CONCAT(CURDATE() + INTERVAL 1 DAY, ' 09:00:00'), CONCAT(CURDATE() + INTERVAL 1 DAY, ' 10:00:00')),
    (CONCAT(CURDATE() + INTERVAL 1 DAY, ' 10:00:00'), CONCAT(CURDATE() + INTERVAL 1 DAY, ' 11:00:00'));
