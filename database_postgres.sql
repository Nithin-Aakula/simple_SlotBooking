-- ============================================================
-- Slot Booking System — Database Schema (PostgreSQL/Neon)
-- ============================================================

-- Drop tables if they exist (clean slate)
DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS slots;

-- -----------------------------------------------------------
-- Slots table
-- -----------------------------------------------------------
CREATE TABLE slots (
    id         SERIAL PRIMARY KEY,
    start_time TIMESTAMP    NOT NULL,
    end_time   TIMESTAMP    NOT NULL,
    is_booked  BOOLEAN      NOT NULL DEFAULT FALSE
);

-- -----------------------------------------------------------
-- Bookings table
-- -----------------------------------------------------------
CREATE TABLE bookings (
    id         SERIAL PRIMARY KEY,
    slot_id    INT          NOT NULL,
    user_name  VARCHAR(120) NOT NULL,
    user_email VARCHAR(255) NOT NULL,
    created_at TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_bookings_slot
        FOREIGN KEY (slot_id) REFERENCES slots(id)
        ON DELETE CASCADE
);

-- -----------------------------------------------------------
-- Seed sample slots (PostgreSQL syntax)
-- -----------------------------------------------------------
INSERT INTO slots (start_time, end_time) VALUES
    (CURRENT_DATE + TIME '09:00:00', CURRENT_DATE + TIME '10:00:00'),
    (CURRENT_DATE + TIME '10:00:00', CURRENT_DATE + TIME '11:00:00'),
    (CURRENT_DATE + TIME '11:00:00', CURRENT_DATE + TIME '12:00:00'),
    (CURRENT_DATE + TIME '13:00:00', CURRENT_DATE + TIME '14:00:00'),
    (CURRENT_DATE + TIME '14:00:00', CURRENT_DATE + TIME '15:00:00'),
    (CURRENT_DATE + TIME '15:00:00', CURRENT_DATE + TIME '16:00:00'),
    (CURRENT_DATE + INTERVAL '1 day' + TIME '09:00:00', CURRENT_DATE + INTERVAL '1 day' + TIME '10:00:00'),
    (CURRENT_DATE + INTERVAL '1 day' + TIME '10:00:00', CURRENT_DATE + INTERVAL '1 day' + TIME '11:00:00');
