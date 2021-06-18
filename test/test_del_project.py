from model.project import Project
import random

def test_delete_some_project(app, db):
    if len(db.get_project_list()) == 0:
        app.project.create(Project(name='test'))
    old_projects = db.get_project_list()
    project = random.choice(old_projects)
    app.project.delete_project_by_name(project.name)
    assert len(old_projects) - 1 == len(db.get_project_list())
    new_projects = db.get_project_list()
    #удаление элементов списка с индексом 0
    old_projects.remove(project)
    assert old_projects == new_projects