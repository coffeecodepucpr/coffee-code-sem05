insert into subjects (name, code) values
  ('Mathematics', 'MAT101'),
  ('Physics',     'PHY101'),
  ('Programming', 'PRO101'),
  ('History',     'HIS101'),
  ('Literature',  'LIT101'),
  ('Chemistry',   'CHE101');

insert into users (user_name, role, email) values
  ('James Anderson',  'teacher', 'james.anderson@example.com'),
  ('Emily Thompson',  'teacher', 'emily.thompson@example.com'),
  ('Michael Davis',   'student', 'michael.davis@example.com'),
  ('Sarah Wilson',    'student', 'sarah.wilson@example.com'),
  ('David Martinez',  'student', 'david.martinez@example.com'),
  ('Jessica Brown',   'student', 'jessica.brown@example.com'),
  ('Christopher Lee', 'student', 'christopher.lee@example.com'),
  ('Olivia Taylor',   'student', 'olivia.taylor@example.com');

-- user_id = teacher
insert into teacher_subjects (user_id, subject_id, created_at) values
  (1, 1, '2026-09-01'),
  (1, 2, '2026-09-02'),
  (1, 3, '2026-09-03'),
  (2, 4, '2026-09-04'),
  (2, 5, '2026-09-05'),
  (1, 6, '2026-09-06'),
  (1, 1, '2026-09-07');

-- user_id = student
insert into lessons (user_id, teach_subj_id, day_of_week, start_time, end_time, status) values
  (7, 1, 1, '18:00', '19:00', 'completed'),
  (4, 2, 2, '19:00', '20:00', 'canceled'),
  (6, 3, 3, '10:00', '11:00', 'canceled'),
  (3, 4, 4, '19:30', '20:30', 'scheduled'),
  (8, 5, 5, '17:00', '18:00', 'scheduled'),
  (3, 6, 6, '18:30', '19:30', 'scheduled'),
  (5, 7, 7, '16:00', '17:00', 'scheduled');

-- user_id = teacher
insert into teacher_schedules (user_id, day_of_week, start_time, end_time) values
  (1, 1, '9:00', '21:00'),
  (1, 2, '9:00', '21:00'),
  (1, 3, '9:00', '21:00'),
  (1, 4, '9:00', '21:00'),
  (1, 5, '9:00', '21:00'),
  (1, 6, '9:00', '21:00'),
  (1, 7, '9:00', '21:00'),
  (2, 1, '9:00', '21:00'),
  (2, 2, '9:00', '21:00'),
  (2, 3, '9:00', '21:00'),
  (2, 4, '9:00', '21:00'),
  (2, 5, '9:00', '21:00'),
  (2, 6, '9:00', '21:00'),
  (2, 7, '9:00', '21:00');
