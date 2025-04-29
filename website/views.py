from flask import Blueprint, render_template, request
from .models import YearGroup, Class  # Assuming these models exist

views = Blueprint('views', __name__)

@views.route('/language')
def language():
    year_groups = YearGroup.query.all()  # Fetch all year groups
    return render_template('language.html', year_groups=year_groups)

@views.route('/literature')
def literature():
    year_groups = YearGroup.query.all()  # Fetch all year groups
    return render_template('literature.html', year_groups=year_groups)

@views.route('/language/<int:year_group_id>')
def language_classes(year_group_id):
    classes = Class.query.filter_by(yeargroup_id=year_group_id).all()  # Fetch classes for the selected year group
    return render_template('language_classes.html', classes=classes, year_group_id=year_group_id)

@views.route('/literature/<int:year_group_id>')
def literature_classes(year_group_id):
    classes = Class.query.filter_by(yeargroup_id=year_group_id).all()  # Fetch classes for the selected year group
    return render_template('literature_classes.html', classes=classes, year_group_id=year_group_id)