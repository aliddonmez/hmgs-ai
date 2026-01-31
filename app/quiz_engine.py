#app/quiz_engine.py

##--QUİZ MOTORU--


## soru yüklenir , mevcut indeks ve skor 0 dan başlanır cevaplar ileride analiz yapabilmemiz icin saklanacak . 
def start_quiz (questions):
    return{
        "questions":questions,
        "current_index":0,
        "score":0,
        "answers":[]
    }

#Bulunduğumuz soruyu gösterme 
def get_current_question(quiz_state):

    idx=quiz_state["current_index"]
    questions=quiz_state["questions"]

    if idx>= len(questions):
        return None
    return questions[idx]

## şık seçildiğinde çalışır 
def submit_answer(quiz_state,user_answer_index):

    question=get_current_question(quiz_state)

    if question is None:
        return None 
    
    ## doğru mu kontrolü 
    correct_index=question["dogru_cevap"]
    is_correct=user_answer_index==correct_index

    ##skor güncellemesi 
    if is_correct:
        quiz_state["score"]+=1
    

    ##cevap geçmişi kaydetme 
    quiz_state["answers"].append({
        "question_id": question["id"],
        "selected": user_answer_index,
        "correct": is_correct,
        "zorluk": question["zorluk"]
    })

    ## var olan index arttırma 
    quiz_state["current_index"]+=1
    
    ##cıktı verme 
    return  {
        "dogru_mu":is_correct,
        "aciklama":question["aciklama"],
        "kaynak":question["kaynak"]
    }


def is_quiz_finished(quiz_state):
    return quiz_state["current_index"] >= len(quiz_state["questions"])



