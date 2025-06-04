-- Migration: Add title_selector, desc_selector, link_selector to sites table
ALTER TABLE sites ADD COLUMN title_selector VARCHAR(256);
ALTER TABLE sites ADD COLUMN desc_selector VARCHAR(256);
ALTER TABLE sites ADD COLUMN link_selector VARCHAR(256);
