import matplotlib.pyplot as plt
import numpy as np
import random

class Student:
    def __init__(self, student_id, reading_age, is_efl, ethnicity, current_year, first_name="Unknown", last_name="Student", class_code="Unknown Class"):
        self.student_id = student_id
        self.reading_age = reading_age
        self.is_efl = is_efl
        self.ethnicity = ethnicity
        self.current_year = current_year
        self.first_name = first_name
        self.last_name = last_name
        self.class_code = class_code
        self.subjects = {}

    def add_grades(self, subject, grades_by_term):
        self.subjects[subject] = grades_by_term

class ModifierEngine:
    @staticmethod
    def get_ethnicity_modifiers():
        return {
            'Indian': 1.28,
            'Asian': 1.16,
            'Mixed': 1.00,
            'Black': 0.94,
            'White': 0.98,
        }

    @staticmethod
    def apply_feature_modifiers(student, growth_rate):
        if student.is_efl:
            growth_rate *= 0.85
        if student.reading_age < 11.0:
            growth_rate *= 0.92
        elif student.reading_age > 12.0:
            growth_rate *= 1.08

        years_left = 11 - student.current_year
        if years_left > 0:
            growth_rate *= 1 + (years_left * 0.03)

        return growth_rate

    @staticmethod
    def apply_ethnicity_modifiers(student, growth_rate):
        ethnicity_modifiers = ModifierEngine.get_ethnicity_modifiers()
        ethnicity = getattr(student, 'ethnicity', 'White British')
        
        if ethnicity in ethnicity_modifiers:
            growth_rate *= ethnicity_modifiers[ethnicity]

        gender = getattr(student, 'gender', 'Male')
        if gender == 'Female':
            growth_rate *= 1.05


        return growth_rate

class GradeLimiter:
    @staticmethod
    def get_age_appropriate_max(target_year, ethnicity, base_max):
        if target_year == 7:
            return 6
        elif target_year == 8:
            return 6
        elif target_year == 9:
            return 7
        elif target_year == 10:
            if ethnicity in ['Indian', 'Asian']:
                return 8
            else:
                return random.choice([7, 8])
        else:
            if base_max >= 9 and ethnicity == 'Indian':
                return 9 if random.random() < 0.25 else 8
            elif base_max >= 9 and ethnicity == 'Asian':
                return 9 if random.random() < 0.20 else 8
            elif base_max >= 9:
                return 9 if random.random() < 0.15 else 8
            else:
                return min(base_max, 8)

    @staticmethod
    def get_base_max_grade(current_max, ethnicity):
        if current_max >= 7:
            if ethnicity == 'Indian':
                return 8
            elif ethnicity == 'Asian':
                return 8
            else:
                return 8
        elif current_max >= 6:
            if ethnicity in ['Indian', 'Asian']:
                return 7
            else:
                return 7
        elif current_max >= 5:
            if ethnicity in ['Indian', 'Asian']:
                return 6
            else:
                return 6
        else:
            return 5

class ChallengeSimulator:
    @staticmethod
    def apply_realistic_challenges(projected, current_term, year_offset, term, student_current_year):
        if year_offset == 11 and term <= 2:
            if random.random() < 0.2:
                projected -= random.uniform(0.2, 0.5)

        if term == 1 and year_offset > student_current_year:
            if random.random() < 0.25:
                projected -= random.uniform(0.1, 0.3)

        if year_offset == 10 and term in [2, 3]:
            if random.random() < 0.25:
                projected -= random.uniform(0.2, 0.6)

        if current_term > 8 and random.random() < 0.15:
            projected -= random.uniform(0.1, 0.3)

        if random.random() < 0.1:
            projected -= random.uniform(0.2, 0.5)

        return projected

class GrowthCalculator:
    @staticmethod
    def calculate_base_growth(numeric_grades):
        if len(numeric_grades) > 1:
            total_growth = numeric_grades[-1] - numeric_grades[0]
            base_growth = total_growth / (len(numeric_grades) - 1)
        else:
            base_growth = 0.25

        base_growth = max(base_growth, 0.15)
        return base_growth

    @staticmethod
    def apply_gcse_reality_check(base_growth, current_max):
        if current_max <= 4:
            base_growth *= 0.8
        elif current_max >= 7:
            base_growth *= 0.9
        return base_growth

class GradePredictor:
    def __init__(self, student: Student):
        self.student = student
        self.projections = {}

    def _process_subject_grades(self, grades):
        term_order = ['Autumn', 'Spring', 'Summer']
        numeric_grades = []
        
        for term in term_order:
            if term in grades and grades[term] != "N/A":
                numeric_grades.append(float(grades[term]))
        
        return numeric_grades

    def _calculate_growth_rate(self, numeric_grades):
        base_growth = GrowthCalculator.calculate_base_growth(numeric_grades)
        base_growth = GrowthCalculator.apply_gcse_reality_check(base_growth, max(numeric_grades))
        
        growth = ModifierEngine.apply_feature_modifiers(self.student, base_growth)
        growth = ModifierEngine.apply_ethnicity_modifiers(self.student, growth)
        
        return growth

    def _generate_term_projection(self, year_offset, term, last_grade, growth, total_terms, 
                                 current_term, target_year_max, ethnicity):
        terms_per_year = 4
        term_growth = growth / terms_per_year
        
        base_variability = 0.15
        time_factor = current_term / max(total_terms, 1)
        variability = np.random.uniform(-base_variability, base_variability) * (1 + time_factor * 0.5)
        
        term_progression = current_term * term_growth
        projected = last_grade + term_progression + variability
        
        min_progression = 0.1
        if term_progression < min_progression:
            projected = last_grade + min_progression + variability
        
        projected = ChallengeSimulator.apply_realistic_challenges(
            projected, current_term, year_offset, term, self.student.current_year
        )
        
        if term == 4:
            projected += 0.1
        
        if year_offset >= 10:
            projected += 0.2
        
        if year_offset == 11 and term >= 3:
            projected += random.uniform(0.1, 0.3)
        
        if year_offset == 11 and term == 4:
            projected = max(2, min(9, round(projected)))
        else:
            projected = max(2, min(target_year_max, round(projected * 10) / 10))
        
        return projected

    def predict(self):
        random.seed(self.student.student_id)
        np.random.seed(self.student.student_id)
        
        for subject, grades in self.student.subjects.items():
            numeric_grades = self._process_subject_grades(grades)
            
            if not numeric_grades:
                self.projections[subject] = {"Year 11": "N/A"}
                continue

            growth = self._calculate_growth_rate(numeric_grades)
            last_grade = numeric_grades[-1]
            
            ethnicity = getattr(self.student, 'ethnicity', 'White British')
            current_max = max(numeric_grades)
            base_max = GradeLimiter.get_base_max_grade(current_max, ethnicity)

            proj = {}
            years_left = 11 - self.student.current_year
            terms_per_year = 4
            total_terms = years_left * terms_per_year
            
            if self.student.current_year >= 11:
                continue
                
            start_year = self.student.current_year + 1
            
            for year_offset in range(start_year, 12):
                target_year_max = GradeLimiter.get_age_appropriate_max(year_offset, ethnicity, base_max)
                
                for term in range(1, terms_per_year + 1):
                    if years_left > 0:
                        current_term = (year_offset - self.student.current_year) * terms_per_year + (term - 1)
                        
                        projected = self._generate_term_projection(
                            year_offset, term, last_grade, growth, total_terms,
                            current_term, target_year_max, ethnicity
                        )
                        
                        proj[f"Year {year_offset} Term {term}"] = projected
                        last_grade = projected

            self.projections[subject] = proj

    def get_predicted_grades(self):
        return {subj: grades.get("Year 11 Term 4", "N/A") for subj, grades in self.projections.items()}

    def plot_projections(self):
        current_year = self.student.current_year
        future_projections = {}
        
        for subject, year_data in self.projections.items():
            future_data = {}
            for term_name, grade in year_data.items():
                year = int(term_name.split()[1])
                if year > current_year:
                    future_data[term_name] = grade
            
            if future_data:
                future_projections[subject] = future_data

        for subject, year_data in future_projections.items():
            years = list(year_data.keys())
            grades = list(year_data.values())
            plt.plot(years, grades, marker='o', label=subject)

        student_name = f"{self.student.first_name} {self.student.last_name}"
        class_name = getattr(self.student, 'class_code', 'Unknown Class')
        plt.title(f"Grade Projection for {student_name} ({class_name})")
        
        plt.ylabel("Predicted Grade")
        plt.xlabel("Academic Year and Term")
        plt.ylim(0, 10)
        plt.xticks(rotation=45, fontsize=8)
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("website/static/assets/graph.png")
        plt.close()