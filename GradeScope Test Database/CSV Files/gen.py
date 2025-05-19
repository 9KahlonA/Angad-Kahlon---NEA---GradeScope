import pandas as pd
import random
import numpy as np

# Load your data files
students_df = pd.read_csv(r'GradeScope Test Database/student_dataset_cleaned/students.csv')  # Your student demographic data
subjects_df = pd.read_csv(r'GradeScope Test Database/student_dataset_cleaned/subjects.csv')
terms_df = pd.read_csv(r'GradeScope Test Database/student_dataset_cleaned/terms.csv')
yeargroups_df = pd.read_csv(r'GradeScope Test Database/student_dataset_cleaned/yeargroups.csv')

# Define year group grade caps
year_caps = {
    1: (2, 4),
    2: (3, 5),
    3: (4, 7),
    4: (5, 8),
    5: (6, 9)
}

# Create a mapping for student info
students_df['yeargroup_id'] = students_df['class_id']

# Find subject_ids for both English Language and English Literature
subject_ids = subjects_df.loc[
    subjects_df['subject_name'].str.contains('English', case=False), 'subject_id'
].tolist()
# Ensure both subjects are present
if len(subject_ids) < 2:
    raise ValueError("Both English Language and English Literature subjects must be present in subjects.csv")

# Total number of entries needed: number of students * number of terms
terms_list = [1, 2, 3, 4]
grade_records = []

# Helper function to get grade cap for a student
def get_yearcap(yeargroup_id):
    return year_caps.get(yeargroup_id, (2, 4))

# For each student, generate progressive grades over terms for both subjects
for index, student in students_df.iterrows():
    student_id = student['student_id']
    yeargroup_id = student['yeargroup_id']
    language = student['home_language']
    first_language = student['is_efl']

    min_cap, max_cap = get_yearcap(yeargroup_id)

    # English background adjustment
    if first_language == 1 and language == 'English':
        base = random.randint(min_cap + 1, min(min_cap + 2, max_cap))
        prog = random.uniform(0.7, 1.0)  # strong progress
    elif first_language == 1 or language == 'English':
        base = random.randint(min_cap, min_cap + 1)
        prog = random.uniform(0.5, 0.8)  # moderate progress
    else:
        base = random.randint(min_cap, min_cap + 1)
        prog = random.uniform(0.3, 0.6)  # slower progress

    # Generate grades for both subjects
    for subject_id in subject_ids:
        prev_grade = base
        for term_idx, term_id in enumerate(terms_list):
            # Progression: generally up, rarely down
            if term_idx == 0:
                new_grade = prev_grade
            else:
                # 80% chance to go up, 15% stay, 5% go down
                r = random.random()
                if r < prog:
                    change = 1
                elif r < prog + 0.15:
                    change = 0
                else:
                    change = -1
                new_grade = prev_grade + change

            # Soft cap: allow 5% outliers above/below
            if random.random() < 0.05:
                outlier = random.choice([-1, 1])
                new_grade += outlier

            # Clamp to min/max cap, but allow 1 above/below for rare outliers
            new_grade = max(min_cap - 1, min(max_cap + 1, new_grade))

            # Append record
            grade_records.append({
                'grade_id': len(grade_records) + 1,
                'student_id': student_id,
                'subject_id': subject_id,
                'term_id': term_id,
                'grade': new_grade
            })
            prev_grade = new_grade

# Save to CSV
grades_df = pd.DataFrame(grade_records)

# Ensure correct format and number of entries
grades_df = grades_df[['grade_id', 'student_id', 'subject_id', 'term_id', 'grade']]
grades_df = grades_df.sort_values(['student_id', 'subject_id', 'term_id']).reset_index(drop=True)
grades_df['grade_id'] = grades_df.index + 1

# Check for correct number of entries
expected_entries = len(students_df) * len(subject_ids) * len(terms_list)
if len(grades_df) != expected_entries:
    raise ValueError(f"Expected {expected_entries} grade records, got {len(grades_df)}.")

grades_df.to_csv('grades.csv', index=False)

print("Grades CSV generated successfully.")

# --- Show 2 example students per yeargroup ---
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
