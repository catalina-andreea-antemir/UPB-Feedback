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
        # ATENTIE: Logica inversata specificata in anon.json
        # Raw 1 = Nota 5 (Complet de acord)
        # Raw 5 = Nota 1 (Deloc)
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

def generate_json_for_feedback(feedback_id, course_name, teacher_name, num_students):
    anon_attempts = []
    
    # --- CALCULAREA ID-urilor ---
    # Folosim multiplicatori diferiti pentru a evita coliziunea ID-urilor
    # Exemplu pentru feedback_id = 1009:
    # Attempt ID va fi ~ 100900
    # Response ID va fi ~ 100900000 (mult mai mare, ca in baza de date reala)
    
    base_attempt_id = feedback_id * 100 
    base_response_id = feedback_id * 100000 
    
    current_response_global_counter = base_response_id

    # Sablonul intrebarilor
    questions_template = [
        ("Subject", "fixed", course_name),
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
        ("Other personal comments or ...", "text", "")
    ]

    for i in range(num_students):
        responses = []
        
        # ID unic per student (attempt)
        current_attempt_id = base_attempt_id + i
        
        for q_name, q_type, q_default in questions_template:
            entry = {
                "id": current_response_global_counter, # ID unic per raspuns
                "name": q_name,
                "printval": "",
                "rawval": ""
            }
            
            if q_type == "fixed":
                entry["printval"] = q_default
                entry["rawval"] = q_default
            elif q_type == "text":
                entry["printval"] = "feedback scris"
                entry["rawval"] = "feedback scris"
            else:
                p_val, r_val = get_random_response(q_type)
                entry["printval"] = p_val
                entry["rawval"] = r_val
            
            responses.append(entry)
            # Incrementam contorul raspunsurilor pentru urmatoarea intrebare
            current_response_global_counter += 1 

        anon_attempts.append({
            "id": current_attempt_id,
            "courseid": 0,
            "number": i + 1,
            "responses": responses
        })

    return {
        "attempts": [],
        "totalattempts": 0,
        "anonattempts": anon_attempts,
        "totalanonattempts": len(anon_attempts),
        "warnings": []
    }

def main():
    print("[INFO] Incepem generarea datelor...")

    # 1. Incarcare fisiere Pickle
    feedbacks = load_pickle('feedbacks.p')
    courses = load_pickle('courses.p')
    categories = load_pickle('categories.p')

    # Mapare pentru acces rapid
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
                course_name = course_obj.get('fullname', 'LIPSA NUME CURS')
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

            # Generare JSON
            json_data = generate_json_for_feedback(fb_id, full_subject_name, teacher_name, num_students)

            # Salvare fisier
            filename = os.path.join(output_dir, f"{fb_id}.json")
            with open(filename, 'w', encoding='utf-8') as jf:
                json.dump(json_data, jf, indent=2)
            
            count += 1
            if count % 50 == 0:
                print(f"   ... generat {count} fisiere ...")

    print(f"\n[SUCCES] Am generat {count} fisiere JSON in folderul '{output_dir}'.")
    print("ID-urile sunt acum separate corect (Attempt vs Response).")

if __name__ == "__main__":
    main()


