########
# Copyright (c) 2014 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.

__author__ = 'idanmo'


class NodeInstance(dict):
    """
    Cloudify node instance.
    """

    def __init__(self, node_instance):
        self.update(node_instance)

    @property
    def id(self):
        """
        :return: The identifier of the node instance.
        """
        return self.get('id')

    @property
    def node_id(self):
        """
        :return: The identifier of the node whom this is in instance of.
        """
        return self.get('node_id')

    @property
    def relationships(self):
        """
        :return: The node instance relationships.
        """
        return self.get('relationships')

    @property
    def host_id(self):
        """
        :return: The node instance host_id.
        """
        return self.get('host_id')

    @property
    def deployment_id(self):
        """
        :return: The deployment id the node instance belongs to.
        """
        return self.get('deployment_id')

    @property
    def runtime_properties(self):
        """
        :return: The runtime properties of the node instance.
        """
        return self.get('runtime_properties')

    @property
    def state(self):
        """
        :return: The current state of the node instance.
        """
        return self.get('state')

    @property
    def version(self):
        """
        :return: The current version of the node instance
         (used for optimistic locking on update)
        """
        return self.get('version')


class NodeInstancesClient(object):

    def __init__(self, api):
        self.api = api

    @staticmethod
    def _get_node_instance_uri(node_instance_id):
        return '/node-instances/{0}'.format(node_instance_id)

    def get(self, node_instance_id, _include=None):
        """
        Returns the node instance for the provided node instance id.

        :param node_instance_id: The identifier of the node instance to get.
        :param _include: List of fields to include in response.
        :return: The retrieved node instance.
        """
        assert node_instance_id
        uri = self._get_node_instance_uri(node_instance_id)
        response = self.api.get(uri, _include=_include)
        return NodeInstance(response)

    def update(self,
               node_instance_id,
               state=None,
               runtime_properties=None,
               version=0):
        """
        Update node instance with the provided state & runtime_properties.

        :param node_instance_id: The identifier of the node instance to update.
        :param state: The updated state.
        :param runtime_properties: The updated runtime properties.
        :param version: Current version value of this node instance in
         Cloudify's storage (used for optimistic locking).
        :return: The updated node instance.
        """
        assert node_instance_id
        uri = self._get_node_instance_uri(node_instance_id)
        data = {'version': version}
        if runtime_properties is not None:
            data['runtime_properties'] = runtime_properties
        if state is not None:
            data['state'] = state
        response = self.api.patch(uri, data=data)
        return NodeInstance(response)

    def list(self, deployment_id=None, _include=None):
        """
        Returns a list of node instances which belong to the deployment
        identified by the provided deployment id.

        :param deployment_id: The deployment's id to list node instances for.
        :param _include: List of fields to include in response.
        :return: Node instances.
        :rtype: list
        """
        params = {'deployment_id': deployment_id} if deployment_id else None
        response = self.api.get('/node-instances',
                                params=params,
                                _include=_include)
        return [NodeInstance(item) for item in response]
