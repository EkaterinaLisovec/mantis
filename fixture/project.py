from model.project import Project

class ProjectHelper:

    def __init__(self, app):
        self.app = app

    def open_project_page(self):
        wd = self.app.wd
        if not (wd.current_url.endswith("manage_proj_page.php") and
                len(wd.find_elements_by_name("manage_proj_create_page_token")) > 0):
            wd.find_element_by_link_text("Manage").click()
            wd.find_element_by_link_text("Manage Projects").click()

    def create(self, project):
        wd = self.app.wd
        self.open_project_page()
        # init project creation
        wd.find_element_by_xpath("//input[@value='Create New Project']").click()
        self.fill_project_form(project)
        # submit project creation
        wd.find_element_by_xpath("//input[@value='Add Project']").click()
        self.open_project_page()
        self.project_cache = None

    def change_field_value(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(text)

    def fill_project_form(self, project):
        wd = self.app.wd
        self.change_field_value("name", project.name)
        self.change_field_value("status", project.status)
        self.change_field_value("view_state", project.view_state)
        self.change_field_value("description", project.description)

    project_cache = None

    # def return_to_home_page(self):
    #     wd = self.app.wd
    #     if not (wd.current_url.endswith("/addressbook/") and len(wd.find_elements_by_name("Send e-Mail")) > 0):
    #         wd.find_element_by_link_text("home").click()

    # def select_first_group(self):
    #     wd = self.app.wd
    #     wd.find_element_by_name("selected[]").click()
    #
    # def select_group_by_index(self, index):
    #     wd = self.app.wd
    #     wd.find_elements_by_name("selected[]")[index].click()
    #
    def select_project_by_name(self, name):
         wd = self.app.wd
         wd.find_element_by_link_text(name).click()
    #
    # def delete_first_group(self):
    #     self.delete_group_by_index(0)
    #
    # def delete_group_by_index(self, index):
    #     wd = self.app.wd
    #     self.open_groups_page()
    #     self.select_group_by_index(index)
    #     # submit deletion
    #     wd.find_element_by_name("delete").click()
    #     self.return_to_home_page()
    #     self.group_cache = None
    #
    def delete_project_by_name(self, name):
        wd = self.app.wd
        self.open_project_page()
        self.select_project_by_name(name)
        # submit deletion
        wd.find_element_by_xpath("//input[@value='Delete Project']").click()
        wd.find_element_by_xpath("//input[@value='Delete Project']").click()
        self.open_project_page()
        self.project_cache = None
    #
    # def modify_first_group(self):
    #     self.modify_group_by_index(0)
    #
    # def modify_group_by_index(self, index, new_group_data):
    #     wd = self.app.wd
    #     self.open_groups_page()
    #     self.select_group_by_index(index)
    #     # open modification form
    #     wd.find_element_by_name("edit").click()
    #     # fill group form
    #     self.fill_group_form(new_group_data)
    #     # submit modification
    #     wd.find_element_by_name("update").click()
    #     self.return_to_home_page()
    #     self.group_cache = None
    #
    # def count(self):
    #     wd = self.app.wd
    #     self.open_groups_page()
    #     return len(wd.find_elements_by_name("selected[]"))
    #
    # group_cache = None
    #
    # def get_group_list(self):
    #     if self.group_cache is None:
    #         wd = self.app.wd
    #         self.open_groups_page()
    #         self.group_cache = []
    #         for element in wd.find_elements_by_css_selector("span.group"):
    #             text = element.text
    #             id = element.find_element_by_name("selected[]").get_attribute("value")
    #             self.group_cache.append(Group(name=text, id=id))
    #     return list(self.group_cache)