from cloudmesh.mongo.DataBaseDecorator import DatabaseUpdate
from cloudmesh.common.Shell import Shell
from cloudmesh.mongo.CmDatabase import CmDatabase
from cloudmesh.common.Printer import Printer
import yaml

class Registry:
    kind = "register"

    collection = "local-registry"

    output = {
        "register": {
            "sort_keys": ["cm.name"],
            "order": ["cm.name",
                      "status",
                      "url",
                      "pid"],
            "header": ["Name",
                       "Status",
                       "Url",
                       "Pid"]
        }
    }

    # noinspection PyPep8Naming
    def Print(self, data, output=None):

        if output == "table":

            order = self.output[Registry.kind]['order']  # not pretty
            header = self.output[Registry.kind]['header']  # not pretty
            # humanize = self.output[kind]['humanize']  # not pretty

            print(Printer.flatwrite(data,
                                    sort_keys=["name"],
                                    order=order,
                                    header=header,
                                    output=output,
                                    # humanize=humanize
                                    )
                  )
        else:
            print(Printer.write(data, output=output))

    def __init__(self):
        pass

    @DatabaseUpdate()
    def add(self, name=None, **kwargs):
        entry = {
            "cm": {
                "cloud": "local",
                "kind": "registry",
                "name": name,
                "driver": None
            },
            "name": name,
            "status": "defined"
        }

        for key in kwargs:
            entry[key] = kwargs[key]

        return entry

    def add_form_file(self, filename, **kwargs):
        """

        :param filename:
        :return:
        """

        spec = filename

        title = spec["info"]["title"]

        registry = Registry()
        entry = registry.add(name=title, **kwargs)

        return entry

    def delete(self, name=None):
        """

        :param name:
        :return:
        """
        cm = CmDatabase()

        collection = cm.collection(self.collection)
        if name is None:
            query = {}
        else:
            query = {'name': name}
        entries = cm.delete(collection=self.collection, **query)
        return entries


    def list(self, name=None):
        """

        :param name:  if none all
        :return:
        """

        cm = CmDatabase()
        if name == None:
            entries = cm.find(cloud="local", kind="registry")
        else:
            entries = cm.find_name(name=name, kind="registry")

        return entries

    def start(self):
        """
        start the registry

        possibly not needed as we have cms start

        :return:
        """
        r = Shell.cms("start")

    def stop(self):
        """
        stop the registry

        possibly not needed as we have cms start
        this will not just sto the registry but mongo

        :return:
        """
        r = Shell.cms("stop")
