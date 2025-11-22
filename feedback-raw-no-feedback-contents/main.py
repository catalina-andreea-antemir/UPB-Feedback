import pickle
import json
import os
import random

# --- CONFIGURARE ---
MIN_STUDENTS = 10
MAX_STUDENTS = 35

def load_pickle(filename):
    """ Incarca fisierele .p daca exista """
    if not os.path.exists(filename):
        print(f"[WARNING] Nu gasesc fisierul '{filename}'.")
        return []
    with open(filename, 'rb') as f:
        return pickle.load(f)

def get_random_response(question_type):
    """ Genereaza raspunsuri random respectand logica Moodle """
    if question_type == "grade":
        grade = random.randint(5, 10)
        return str(grade), str(grade)
    
    elif question_type == "likert":
        options = [
            {"raw": "1", "print": "5  - Complet de Acord"},
            {"raw": "2", "print": "4  - ..."},
            {"raw": "3", "print": "3  - ..."},
            {"raw": "4", "print": "2  - ..."},
            {"raw": "5", "print": "1  - Deloc de acord"}
        ]
        choice = random.choice(options)
        return choice["print"], choice["raw"]
    
    elif question_type == "percent":
        options = [
            {"raw": "5", "print": "80% .. 100%"},
            {"raw": "4", "print": "60% .. 80%"},
            {"raw": "3", "print": "40% .. 60%"}
        ]
        choice = random.choice(options)
        return choice["print"], choice["raw"]
        
    return "", ""


def main():
    feedbacks = load_pickle('feedbacks.p')
    courses = load_pickle('courses.p')
    categories = load_pickle('categories.p')

    
    courses_map = {c['id']: c for c in courses}
    categories_map = {cat['id']: cat for cat in categories}

    # 2. Creare folder output
    output_dir = 'feedback_contents'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"[INFO] Am creat folderul '{output_dir}'")

    print(f"[INFO] Am incarcat {len(feedbacks)} formulare si {len(courses)} cursuri.")
    
    count = 0
    for fb in feedbacks:
        fb_id = fb.get('id')
        course_id = fb.get('course')
        
        if fb_id:
            # Gasirea numelui real al cursului
            course_obj = courses_map.get(course_id)
            course_name = "Curs Necunoscut"
            category_name = ""
            
            if course_obj:
                course_name = course_obj.get('fullname', 'Curs Fara Nume')
                cat_id = course_obj.get('category')
                if cat_id and cat_id in categories_map:
                    category_name = categories_map[cat_id].get('name', '')

            # Compunere nume subiect
            full_subject_name = course_name
            if category_name:
                full_subject_name += f" ({category_name})"

            # Date simulate
            teacher_name = f"Prenume NUME"
            num_students = random.randint(MIN_STUDENTS, MAX_STUDENTS)

            # TODO : Generare JSON
            

            # TODO : Salvare fisier
    

if __name__ == "__main__":
    main()




















































import json
import pickle
import os
import random
from fileinput import filename

# Nr minim si maxim de studenti pe curs
MIN_STUDENTS = 30
MAX_STUDENTS = 500

def load_pickle(filename):
    # Fisierele .p
    with open(filename, 'rb') as f:
        return pickle.load(f)

def get_random_feedback(question_type):
    if question_type == "grade":
        grade = random.randint(1, 10);
        return str(grade), str(grade)
    elif question_type == "likert":
        options = [ {"raw": "1", "print": "5  - Complet de Acord"},
                    {"raw": "2", "print": "4  - ..."}, {"raw": "3", "print": "3  - ..."},
                    {"raw": "4", "print": "2  - ..."},
                    {"raw": "5", "print": "1  - Deloc de acord"}]
        choice = random.choice(options)
        return choice["print"], choice["raw"]
    elif question_type == "percent":
        options = [{"raw": "5", "print": "80% .. 100%"},
                   {"raw": "4", "print": "60% .. 80%"},
                   {"raw": "3", "print": "40% .. 60%"}]
        choice = random.choice(options)
        return choice["print"], choice["raw"]
    return "", ""

def generate_json(feedback_id, course_name, teacher_name, num_students):
    anon_attempts = []

    # Exemplu pt feedback_id = 1009
    # Attempt id va fi 100900 si Response id va fi 10090000
    # Ca sa difere id urile, inmultim cu 100 si 10000

    base_attempt_id = feedback_id * 100
    base_response_id = feedback_id * 10000

    curr_response_cnt = base_response_id

    # Template de intrebari
    questions_template = [("Subject", "fixed", course_name),
                        ("Teacher", "fixed", teacher_name),
                        ("Laboratory/seminar/project ...", "fixed", teacher_name),
                        ("Is your assessment of this ...", "likert", ""),
                        ("What grade do you expect to...", "grade", ""),
                        ("Is the general workload in ...", "likert", ""),
                        ("Location / hardware and ...", "likert", ""),
                        ("The approximate number of ...", "percent", ""),
                        ("Does the course tutor have ...", "likert", ""),
                        ("Was the teaching method ...", "likert", ""),
                        ("Did the course stimulate ...", "likert", ""),
                        ("Other personal comments or ...", "text", "")]

    for i in range(num_students):
        responses = []
        curr_attempt_id = base_attempt_id + 1

        for q_name, q_type, q_default in questions_template:
            entry = {"id": curr_response_cnt, # ID unic per raspuns
                    "name": q_name,
                    "printval": "",
                    "rawval": ""}

            if q_type == "fixed":
                entry["printval"] = q_default
                entry["rawval"] = q_default
            elif q_type == "text":
                entry["printval"] = "feedback_scris"
                entry["rawval"] = "feedback_scris"
            else:
                p_val, r_val = get_random_feedback(q_type)
                entry["printval"] = p_val
                entry["rawval"] = r_val

            responses.append(entry)
            curr_response_cnt += 1

        anon_attempts.append({"id": curr_attempt_id,
                            "courseid": 0,
                            "number": i + 1,
                            "responses": responses})
    return {"attempts": [],
            "totalattempts": 0,
            "anonattempts": anon_attempts,
            "totalanonattempts": len(anon_attempts),
            "warnings": []}

def main():
    print("Generarea incepe!")
    print()

    feedbacks = load_pickle('feedbacks.p')
    courses = load_pickle('courses.p')
    categories = load_pickle('categories.p')

    # Acces mai rapid
    courses_map = {c['id']: c for c in courses}
    categories_map = {cat['id']: cat for cat in categories}

    # Facem un folder in care sa stocam fisierele json
    output_dir = 'feedback_contents'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"S-a creat folderul '{output_dir}'")

    print(f"S-au incarcat {len(feedbacks)} formulare si {len(courses)} cursuri.")

    count = 0
    for fb in feedbacks:
        fb_id = fb.get('id')
        course_id = fb.get('course')

        if fb_id:
            # Gasim cursul
            course_obj = courses_map.get(course_id)
            course_name = "Curs Necunoscut"
            category_name = ""

            if course_obj:
                course_name = course_obj.get('fullname', 'LIPSA NUME CURS')
                cat_id = course_obj.get('category')
                if cat_id and cat_id in categories_map:
                    category_name = categories_map[cat_id].get('name', '')

            # Compunem numele cursului
            full_subject_name = course_name
            if category_name:
                full_subject_name += f" ({category_name})"

            # Date simulate
            teacher_name = f"Prenume NUME"
            num_students = random.randint(MIN_STUDENTS, MAX_STUDENTS)

            # Generam
            json_data = generate_json(fb_id, full_subject_name, teacher_name, num_students)

            # Salvam
            filename = os.path.join(output_dir, f"{fb_id}.json")
            with open(filename, 'w', encoding='utf-8') as jf:
                json.dump(json_data, jf, indent=2)

            count += 1
            if count % 50 == 0:
                print(f"   ... S-au generat {count} fisiere ...")

    print(f"\nAm generat {count} fisiere JSON in folderul '{output_dir}'")

if __name__ == "__main__":
    main()
