# -*- coding: utf-8 -*-
from model.project import Project
#если хотим загружать данные из data.groups.py, то указать переменную на вход: data_groups
#это описано в conftest


def test_add_project(app, db, json_projects):
    project = json_projects
    #old_projects = db.get_project_list()
    old_projects = app.soap.get_projects()
    app.project.create(project)
    #assert len(old_groups) + 1 == app.group.count()
    #new_projects = db.get_project_list()
    new_projects = app.soap.get_projects()
    #добавление новой группы в список
    old_projects.append(project)
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)