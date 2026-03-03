
CREATE TABLE IF NOT EXISTS quiz_attempt_answers(

    id INTEGER PRIMARY KEY AUTOINCREMENT ,
    attempt_id  TEXT NOT NULL ,
    user_id TEXT NOT NULL , 

    timestamp TEXT NOT NULL ,
    question_id TEXT NOT NULL ,
    ders TEXT ,
    konu TEXT ,
    selected_option INTEGER NOT NULL,
    correct_option INTEGER NOT NULL ,
    is_correct INTEGER NOT NULL,

    confidence REAL,
    retrieval_score REAL
    
);

CREATE INDEX IF NOT EXISTS idx_attempt_id
ON quiz_attempt_answers (attempt_id);

CREATE INDEX IF NOT EXISTS idx_user_id
ON quiz_attempt_answers (user_id);