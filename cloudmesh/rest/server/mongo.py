# TODO: complete
# for executing shell commands please do not reinvent the whele but use

# https://github.com/cloudmesh/client/blob/master/cloudmesh_client/common/Shell.py
# if commands are missing or are not working we can fix that in cloudmesh_client

from __future__ import print_function

import os

from cloudmesh.common.Shell import Shell
from cloudmesh.common.util import grep
import shutil
import errno
from pymongo import MongoClient
import psutil

def log_print(msg):
    # temporarily used till we switch to real logger
    print('mongod: ' + msg)

def create_dir(path):
    os.system("mkdir -p " + path)

class Mongo(object):
    """
    Manage mongod service.
    """

    def __init__(self, port=27017):
        """
        sets up a mongo d service
        :param port: the prort number. default set to 5000
        """
        self.parameters = {}
        self.parameters['port'] = port
        self.parameters['dbpath'] = "~/.cloudmesh/data/db"
        self.parameters['bind_ip'] = "127.0.0.1"
        self.parameters['logpath'] = "~/.cloudmesh/data/mongo.log"
        create_dir(self.parameters['dbpath'])
        print(self.parameters)


    def clean(self):
        """
        Removes the database and the log files
        :return:
        """
        shutil.rmtree(self.parameters['dbpath'])
        shutil.rmtree(self.parameters['logpath'])
        create_dir(self.parameters['dbpath'])


    def kill(self):
        """
        killall mongod
        :return:
        """
        os.system("killall mongod")
        self.clean()


    def start(self):
        """starts the mongo service."""
        command = 'mongod --port {port} -dbpath {dbpath} -bind_ip {bind_ip} --fork --logpath {logpath}' \
            .format(**self.parameters)
        command_list = command.split(' ')
        create_dir(self.parameters['dbpath'])
        print(command)
        os.system("ulimit -n 1024")
        os.system(command)

        # print (command_list)
        # r = Shell.execute(command)

        # print(r)
        log_print('started')
        self.status()

    def stop(self):
        """stops the mongo service."""
        process_id = self.pid()
        if process_id is not None:

            p = psutil.Process(int(process_id))
            p.terminate()  # or p.kill()

        log_print('stopped')
        # waite a bit
        self.status()        

    def pid(self):
        process_id = None
        output = Shell.ps('-ax')
        for line in output.split("\n"):

            if 'mongod' in line and "--port" in line:
                log_print(line)
                process_id = line.split(" ")[0]
                return process_id

        return process_id


    def status(self, format=None):
        """returns the status of the service. if no parameter. if format
        is specified its returned in that fomat. txt, json, XML,
        allowed
        """
        process_id = self.pid()
        if process_id is not None:
            log_print('running')
            log_print("Mongod process id: " + str(process_id))
        else:
            log_print('stopped')

    def reset(self):
        """stops the service and deletes the database, restarts the service."""
        r = Shell.execute('mongod stop'.split(' '))
        print (r)
        log_print('stopped')
        # client.drop_database(databasename); how is this differentfrom deleting the collection?

        # print("not yet implemented")


    def delete(self):
        """deletes all data in the database."""
        try:
            log_print("NOT YET IMPLEMENTED")
            # client = MongoClient(host='localhost', port=self.parameters['port'] )
            # TODO: bug database is not defined


			#db=client.get_database(database)
            #collectionsnames = db.collection_names()

            #for singlecollectionname in collectionsnames:
            #    log_print("deleting: " + singlecollectionname)
            #    db.get_collection(singlecollectionname).remove({})

        except Exception as e:
            log_print("problem deleting" +  str(e))


    def log(self, path):
        """sets the log file to the given path"""
        self.parameters['logpath'] = path  # TODO: define test programs with nosetest

if __name__ == "__main__":
    m = Mongo()
    m.start()
