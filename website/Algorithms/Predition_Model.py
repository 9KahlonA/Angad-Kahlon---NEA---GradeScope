# Import plotting & numerical tools
import matplotlib.pyplot as plt
import numpy as np

# ----------------- STUDENT FEATURE MODEL -------------------
class Student:
    def __init__(self, student_id, reading_age, is_efl, ethnicity, current_year):
        self.student_id = student_id  # Unique student ID
        self.reading_age = reading_age  # Float reading age (e.g., 11.5)
        self.is_efl = is_efl  # 1 if English not first language, 0 if fluent/native
        self.ethnicity = ethnicity  # Ethnic background (if used for modifiers)
        self.current_year = current_year  # Integer school year (e.g. 9)
        self.subjects = {}  # Dictionary: {subject_name: {year: grade}}

    def add_grades(self, subject, grades_by_term):
        self.subjects[subject] = grades_by_term  # Add subject progress history

# ----------------- PREDICTION ENGINE -------------------
class GradePredictor:
    def __init__(self, student: Student):
        self.student = student  # Attach student model
        self.projections = {}  # Store all future projections by subject

    # Modifies growth rate based on EFL, reading age, and student age
    def apply_feature_modifiers(self, growth_rate):
        if self.student.is_efl:
            growth_rate *= 0.90  # Slightly less penalty for EFL learners
        if self.student.reading_age < 11.0:
            growth_rate *= 0.98  # Slightly less penalty for lower reading age
        elif self.student.reading_age > 12.0:
            growth_rate *= 1.10  # Slightly higher boost for strong readers

        # Dynamic adjustment based on how young the student is
        years_left = 11 - self.student.current_year  # Years left until Year 11
        if years_left > 0:
            growth_rate *= 1 + (years_left * 0.05)  # Increase growth rate for younger students

        return growth_rate

    def predict(self):
        # Loop through each subject the student has
        for subject, grades in self.student.subjects.items():
            years = sorted(grades.keys())  # Sort year keys
            values = [float(grades[yr]) for yr in years if grades[yr] != "N/A"]

            if not values:
                self.projections[subject] = {"Year 11": "N/A"}
                continue

            # Apply simple linear regression on years vs grades
            x = np.arange(len(values))
            y = np.array(values)
            if len(x) > 1:
                coef = np.polyfit(x, y, 1)  # Fit a trend line: slope and intercept
                base_growth = coef[0]  # Use slope for growth rate
            else:
                base_growth = 0.30  # Slightly higher assumed growth when not enough data

            # Adjust the trend using reading age, EFL status, and student age
            growth = self.apply_feature_modifiers(base_growth)
            last_grade = values[-1]  # Starting point for future projection

            # Introduce variability to ensure not all students reach grade 9
            max_grade = np.random.randint(7, 10)  # Randomly set max grade between 7 and 9

            proj = {}
            years_left = 11 - self.student.current_year  # Years left until Year 11
            terms_per_year = 4  # Represent 4 terms per year

            for year_offset in range(self.student.current_year, 12):  # Project to Year 11
                for term in range(1, terms_per_year + 1):  # Loop through 4 terms per year
                    if years_left > 0:
                        # Distribute growth gradually across terms and years
                        term_growth = growth / terms_per_year
                        variability = np.random.uniform(-0.3, 0.3)  # Add variability for dips and rises
                        projected = last_grade + ((year_offset - self.student.current_year) * growth) + (term * term_growth) + variability
                    else:
                        projected = last_grade  # No growth if already in Year 11

                    # Add a small boost for Year 10 and Year 11 to represent revision time
                    if year_offset >= 10:
                        projected += 0.1  # Small boost for revision time

                    projected = max(2, min(max_grade, round(projected)))  # Clamp between grade 2 and max_grade
                    proj[f"Year {year_offset} Term {term}"] = projected
                    last_grade = projected  # Update last grade for the next term

            self.projections[subject] = proj  # Save subject projections

    # Final predicted grade = projected Year 11 grade per subject
    def get_predicted_grades(self):
        return {subj: grades.get("Year 11 Term 4", "N/A") for subj, grades in self.projections.items()}  # Use final term of Year 11

    # Plot predictions and save graph as static image
    def plot_projections(self):
        for subject, year_data in self.projections.items():
            years = list(year_data.keys())
            grades = list(year_data.values())
            plt.plot(years, grades, marker='o', label=subject)

        plt.title(f"Grade Projection for Student {self.student.student_id}")
        plt.ylabel("Predicted Grade")
        plt.xlabel("Academic Year and Term")
        plt.ylim(0, 10)
        plt.xticks(rotation=45, fontsize=8)  # Rotate x-axis labels for better readability
        plt.legend()
        plt.grid(True)
        plt.tight_layout()  # Adjust layout to prevent label overlap
        plt.savefig("website/static/assets/graph.png")  # Save to static folder
        plt.close()
