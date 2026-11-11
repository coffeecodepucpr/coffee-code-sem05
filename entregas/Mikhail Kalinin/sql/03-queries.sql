-- 1. Full table
select * from subjects;

-- 2. Filter and sort (teacher list)
select user_name, role
from users
where role='teacher'
order by user_name

-- 3. JOIN: days of the week on which the teacher works
select
  u.user_name as teacher,
  s.day_of_week
from users u
join teacher_schedules s on s.user_id = u.user_id
order by u.user_name, s.day_of_week;

-- 4. Aggregation: number of subjects per teacher
select u.user_name as teacher,
  u.role,
  count(ts.user_id) as subjects_per_teacher
from users u
join teacher_subjects ts on ts.user_id = u.user_id
group by u.user_id, u.user_name
order by subjects_per_teacher desc, u.user_name;

-- 5. A specific person's subjects
select u.user_name as student, s.name as subject
from users u
left join lessons l on l.user_id = u.user_id
join teacher_subjects ts        on ts.teach_subj_id = l.teach_subj_id
join subjects s      on s.subject_id = ts.subject_id
where u.email = 'michael.davis@example.com';

-- 6. Additional - all student subjects with teacher info
select
  u.user_name as student,
  s.name as subject,
  t.user_name as teacher,
  l.status
from users u
left join lessons l         on l.user_id = u.user_id
join teacher_subjects ts    on ts.teach_subj_id = l.teach_subj_id
join subjects s             on s.subject_id = ts.subject_id
join users t on ts.user_id = t.user_id
order by u.user_name;

-- 7. Full schedule
select 
    l.day_of_week as day,
    l.start_time as time,
    u.user_name as student,
    s.name as subject, 
    t.user_name as teacher,
    l.status
from users u
join lessons l on l.user_id = u.user_id
join teacher_subjects ts on ts.teach_subj_id = l.teach_subj_id
join subjects s on s.subject_id = ts.subject_id
join users t on ts.user_id = t.user_id
where u.role = 'student'
order by l.day_of_week;

-- lesson status count
select 
    l.status,
    count(l.lesson_id) as lesson_count
from lessons l
group by l.status
order by lesson_count desc;

-- student lessons number
select 
    u.user_name as student,
    count(l.lesson_id) as total_lessons
from users u
join lessons l on u.user_id = l.user_id
where u.role = 'student'
group by u.user_id, u.user_name
order by total_lessons desc;
