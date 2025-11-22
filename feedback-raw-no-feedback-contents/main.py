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
