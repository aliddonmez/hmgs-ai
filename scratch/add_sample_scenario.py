import psycopg
from app.scenario_storage import _pg_conn_info

def add_sample():
    conn = psycopg.connect(**_pg_conn_info())
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO scenario_cases (
            title, course, topic, scenario_text, question_text, 
            option_a, option_b, option_c, option_d, 
            correct_option, explanation, legal_basis
        ) VALUES (
            'Örnek Hırsızlık Vakası', 
            'Ceza Hukuku', 
            'Hırsızlık', 
            'A, sokakta yürüyen B''nin elindeki çantayı aniden çekip alarak kaçmıştır. B, olayın şokuyla müdahale edememiştir.', 
            'A''nın eylemi Türk Ceza Kanunu kapsamında öncelikle hangi suçu oluşturur?', 
            'Dolandırıcılık', 
            'Hırsızlık', 
            'Yağma (Gasp)', 
            'Güveni Kötüye Kullanma', 
            'B', 
            'Zilyedin rızası olmadan başkasına ait taşınır bir malın, kendisine veya başkasına bir yarar sağlamak maksadıyla bulunduğu yerden alınması hırsızlık suçunu oluşturur.',
            'TCK Madde 141'
        )
    """)
    conn.commit()
    print("Sample scenario added successfully")

if __name__ == "__main__":
    add_sample()
