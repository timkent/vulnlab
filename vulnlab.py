#!/usr/bin/env python3

# vulnlab.py
# https://github.com/timkent/vulnlab

# depends on: python3-flask python3-pyvmomi

from flask import Flask
from pyVim import connect
from pyVmomi import vmodl
from pyVmomi import vim

# details for your ESX host:
host = "x.x.x.x"
user = "vulnlab"
password = "sethere"
port = 443

# name of (this) machine to be excluded
control_vm = "vulnlab"

def main():

    # ignore invalid cert on ESX box
    import ssl
    _create_unverified_https_context = ssl._create_unverified_context
    ssl._create_default_https_context = _create_unverified_https_context

    vm_list = get_vm_list()

    app = Flask(__name__)

    @app.route("/")
    def index():
        result = '''<!DOCTYPE html>
<html>
  <head>
    <title>VulnLab</title>
  <body>
    <h1>Reset</h1>
'''
        for name, uuid in sorted(vm_list.items()):
            result += '    <a href="/reset/' + name + '">' + name + '</a><br>\n'

        result += '''  </body>
</html>
'''
        return result, 200

    @app.route("/reset/<string:vm_name>")
    def reset(vm_name):
        reset_vm(vm_list, vm_name)
        return 'OK\n', 200

    # start the web server
    app.run(host="0.0.0.0", port=5000)

def get_vm_list():

    # make connection
    service_instance = connect.SmartConnect(host=host, user=user, pwd=password, port=int(port))

    # create list of machines
    content = service_instance.RetrieveContent()
    containerView = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    children = containerView.view
    vm_list = {}
    for child in children:
        summary = child.summary
        if not summary.config.name == control_vm:
            vm_list[summary.config.name] = summary.config.uuid

    connect.Disconnect(service_instance)
    return vm_list

def reset_vm(vm_list, target_name):

    # make sure target is in list
    target_uuid = vm_list[target_name]

    if target_uuid:
        # make connection
        service_instance = connect.SmartConnect(host=host, user=user, pwd=password, port=int(port))
        target_vm = service_instance.content.searchIndex.FindByUuid(None, target_uuid, True)

        if target_vm:
#            print(target_vm.runtime.powerState)
            target_vm.ResetVM_Task()

        connect.Disconnect(service_instance)

if __name__ == "__main__":
    main()
