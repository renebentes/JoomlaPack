# coding: utf-8
class Project:

    def __init__(self, path, json):
        self.path = path
        self.name = json["name"]
        self.project_type = json["project_type"]
        self.description = json["description"]
        self.default_project_name = json["default_project_name"]
        self.prefix_project_name = json["prefix_project_name"]
        self.folders = json["folders"]
        self.settings = json["settings"]
        self.build_systems = json["build_systems"]

    def to_quickpanel(self):
        return [self.name, self.description]

    def __str__(self):
        return self.name
