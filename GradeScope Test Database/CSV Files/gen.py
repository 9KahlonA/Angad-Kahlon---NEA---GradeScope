import pandas as pd
import random
import numpy as np

students_df = pd.read_csv(r'GradeScope Test Database/student_dataset_cleaned/students.csv')
subjects_df = pd.read_csv(r'GradeScope Test Database/student_dataset_cleaned/subjects.csv')
terms_df = pd.read_csv(r'GradeScope Test Database/student_dataset_cleaned/terms.csv')
yeargroups_df = pd.read_csv(r'GradeScope Test Database/student_dataset_cleaned/yeargroups.csv')

year_caps = {
    1: (2, 4),
    2: (3, 5),
    3: (4, 7),
    4: (5, 8),
    5: (6, 9)
}

students_df['yeargroup_id'] = students_df['class_id']

subject_ids = subjects_df.loc[
    subjects_df['subject_name'].str.contains('English', case=False), 'subject_id'
].tolist()
if len(subject_ids) < 2:
    raise ValueError("Both English Language and English Literature subjects must be present in subjects.csv")

terms_list = [1, 2, 3, 4]
grade_records = []

def get_yearcap(yeargroup_id):
    return year_caps.get(yeargroup_id, (2, 4))

for index, student in students_df.iterrows():
    student_id = student['student_id']
    yeargroup_id = student['yeargroup_id']
    language = student['home_language']
    first_language = student['is_efl']

    min_cap, max_cap = get_yearcap(yeargroup_id)

    if first_language == 1 and language == 'English':
        base = random.randint(min_cap + 1, min(min_cap + 2, max_cap))
        prog = random.uniform(0.7, 1.0)
    elif first_language == 1 or language == 'English':
        base = random.randint(min_cap, min_cap + 1)
        prog = random.uniform(0.5, 0.8)
    else:
        base = random.randint(min_cap, min_cap + 1)
        prog = random.uniform(0.3, 0.6)

    for subject_id in subject_ids:
        prev_grade = base
        for term_idx, term_id in enumerate(terms_list):
            if term_idx == 0:
                new_grade = prev_grade
            else:
                r = random.random()
                if r < prog:
                    change = 1
                elif r < prog + 0.15:
                    change = 0
                else:
                    change = -1
                new_grade = prev_grade + change

            if random.random() < 0.05:
                outlier = random.choice([-1, 1])
                new_grade += outlier

            new_grade = max(min_cap - 1, min(max_cap + 1, new_grade))

            grade_records.append({
                'grade_id': len(grade_records) + 1,
                'student_id': student_id,
                'subject_id': subject_id,
                'term_id': term_id,
                'grade': new_grade
            })
            prev_grade = new_grade

grades_df = pd.DataFrame(grade_records)

grades_df = grades_df[['grade_id', 'student_id', 'subject_id', 'term_id', 'grade']]
grades_df = grades_df.sort_values(['student_id', 'subject_id', 'term_id']).reset_index(drop=True)
grades_df['grade_id'] = grades_df.index + 1

expected_entries = len(students_df) * len(subject_ids) * len(terms_list)
if len(grades_df) != expected_entries:
    raise ValueError(f"Expected {expected_entries} grade records, got {len(grades_df)}.")

grades_df.to_csv('grades.csv', index=False)

print("Grades CSV generated successfully.")

print("\nSample student records by yeargroup:")
for yg in range(1, 6):
    students_in_yg = students_df[students_df['yeargroup_id'] == yg].head(2)
    for _, stu in students_in_yg.iterrows():
        print(f"\nStudent ID: {stu['student_id']}, Name: {stu['first_name']} {stu['last_name']}, Yeargroup: {yg}, Home Lang: {stu['home_language']}, EFL: {stu['is_efl']}")
        for subject_id in subject_ids:
            subject_name = subjects_df.loc[subjects_df['subject_id'] == subject_id, 'subject_name'].values[0]
            print(f"  Subject: {subject_name}")
            stu_grades = grades_df[(grades_df['student_id'] == stu['student_id']) & (grades_df['subject_id'] == subject_id)].sort_values('term_id')
            print(stu_grades[['term_id', 'grade']].to_string(index=False))