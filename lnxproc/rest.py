"""
REST setup using Flask
"""
from logging import getLogger

from flask import Flask, jsonify, Response
from flask_restful import Resource, Api

from .resources import Resources, get_keys, json_streamer

LOGGER = getLogger(__name__)

ROOT = [None, ]


class Keys(Resource):
    """
    Return list of available keys
    """
    def get(self):  # pylint: disable=no-self-use
        """
        Return list of available keys
        """
        keys = list(get_keys())
        LOGGER.debug("Keys are %s", keys)

        return jsonify(keys)


class Proc(Resource):
    """
    Return status of host resource
    """
    def get(self, resource_key):  # pylint: disable=no-self-use
        """
        Return json representation
        """
        LOGGER.debug("Proc route for %s", resource_key)
        res = Resources(
            keys=(resource_key, ),
            root=ROOT[0],
        )
        res.read()
        data = res.normalize()

        return jsonify(data)


class ProcAll(Resource):
    """
    Return statuses of all host resources
    """
    def get(self):  # pylint: disable=no-self-use
        """
        Return json representation
        """
        LOGGER.debug("ProcAll route")
        res = Resources(
            root=ROOT[0],
        )
        res.read()
        data = res.normalize()

        return Response(json_streamer(data))


class Pid(Resource):
    """
    Return status of process
    """
    def get(self, pid, resource_key):  # pylint: disable=no-self-use
        """
        Return json representation
        """
        res = Resources(
            keys=(resource_key, ),
            pids=(pid, ),
            root=ROOT[0],
        )
        res.read()
        data = res.normalize()

        return jsonify(data)


def entry(port=None, root=None):
    """
    Create and start REST API
    """
    LOGGER.debug("Start REST API on port %s for root %s", port, root)
    ROOT[0] = root

    app = Flask(__name__)
    api = Api(app)
    api.add_resource(Keys, '/keys')
    api.add_resource(ProcAll, '/resource')
    api.add_resource(Proc, '/resource/<resource_key>')
    api.add_resource(Pid, '/pid/<pid>/<resource_key>')
    app.run(port=port, host='0.0.0.0')
