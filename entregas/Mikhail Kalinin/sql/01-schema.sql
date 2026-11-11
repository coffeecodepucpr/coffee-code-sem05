create table users (
  user_id    bigint generated always as identity primary key,
  role       text not null,
  user_name  text not null,
  email      text not null unique,
  created_at timestamptz not null default now()
);

create table subjects (
  subject_id  bigint generated always as identity primary key,
  name        text not null unique,
  code        text not null unique
);

-- associative table: resolves the N:N relationship between users (teachers) and subjects
create table teacher_subjects (
  teach_subj_id  bigint generated always as identity primary key,  
  user_id        bigint not null references users (user_id) on delete cascade,
  subject_id     bigint not null references subjects (subject_id) on delete cascade,
  created_at     date not null default current_date
);

create table lessons (
  lesson_id        bigint generated always as identity primary key,
  user_id          bigint not null references users (user_id),
  teach_subj_id    bigint not null references teacher_subjects (teach_subj_id),
  day_of_week      smallint not null check (day_of_week between 1 and 7),  -- 1 = monday, 7 = sunday
  start_time       time not null,
  end_time         time not null,
  status           text not null
);

create table teacher_schedules (
  sch_id        bigint generated always as identity primary key,
  user_id       bigint not null references users (user_id),
  day_of_week   smallint not null check (day_of_week between 1 and 7),  -- 1 = monday, 7 = sunday
  start_time    time not null,
  end_time      time not null
);

alter table users              enable row level security;
alter table subjects           enable row level security;
alter table teacher_subjects   enable row level security;
alter table lessons            enable row level security;
alter table teacher_schedules  enable row level security;
