# coding: utf-8
import sublime
import sublime_plugin
import os
import json
from shutil import rmtree

st_version = int(sublime.version())

if st_version > 3000:
    from JoomlaPack.commands import *
    from JoomlaPack.lib.helpers import *
    from JoomlaPack.lib.project import Project
else:
    from commands import *
    from lib.hepers import *
    from lib.project import Project


class NewProjectCommand(sublime_plugin.WindowCommand):

    def run(self, template=None):
        templates = get_templates()
        self.projects = []
        self.quickpanel = []
        for item in templates:
            f = item + ".json"
            if not os.path.exists(os.path.join(templates[item], f)):
                show_message("error", "[Error] %s is invalid!" % item)
                return
            content = json.load(open(os.path.join(templates[item], f)))
            self.projects.append(Project(templates[item], content))

        for project in self.projects:
            self.quickpanel.append(project.to_quickpanel())

        if template is None:
            sublime.active_window().show_quick_panel(
                self.quickpanel, self.on_pincked_template)
        else:
            index = -1
            for x in range(0, len(self.quickpanel)):
                if template in self.quickpanel[x][0].lower():
                    index = x
                    break
            self.on_pincked_template(index)

    def on_pincked_template(self, index):
        if index < 0:
            self.on_cancel()
            return
        self.pincked_project = self.projects[index]
        show_input_panel("Type %s name: " % self.pincked_project.project_type,
                         self.pincked_project.default_project_name,
                         self.on_done, None, self.on_cancel)

    def on_cancel(self):
        show_message("", "Operation Canceled!")

    def on_done(self, project_name):
        if self.pincked_project.prefix_project_name not in project_name:
            project_name = self.pincked_project.prefix_project_name + \
                project_name
        destination = os.path.join(get_project_root(), project_name)

        if os.path.exists(destination):
            if not show_message("confirm",
                                "[Confirm] Project %s already exists!"
                                % project_name):
                return
            else:
                rmtree(destination)
        try:
            args = {
                "args": {
                    "name": project_name,
                    "source": self.pincked_project.path,
                    "destination": destination
                }
            }
            sublime.active_window().run_command(
                "new_%s" % self.pincked_project.project_type, args)
        except Exception as e:
            rmtree(destination)
            show_message("error",
                         "[Error] Project %s could not be created! %s"
                         % (project_name, e))
        else:
            self.save_project_file(project_name, destination)

    def save_project_file(self, project_name, destination):
        content = {}
        indent = self.pincked_project.settings[0]["tab_size"]
        self.pincked_project.folders[0]["path"] = destination
        try:
            f = open(os.path.join(destination, "%s.sublime-project" %
                                  project_name.replace("_", "-")), "w+")

            content["build_systems"] = self.pincked_project.build_systems
            content["settings"] = self.pincked_project.settings
            content["folders"] = self.pincked_project.folders
            f.write(json.dumps(content, indent=indent))
            f.close()
        except (Exception, IOError) as e:
            show_message("error",
                         "[Error] %s.sublime-project could not be created! %s"
                         % (project_name, e))
        else:
            sublime.active_window().set_project_data(content)
