import logging

import pymel.core as pm

logger = logging.getLogger(__name__)

def get_edit_context():
    return Edit_Context()

class Edit_Context(object):

    def __init__(self):
        self._created_nodes=[]
        self._attr_values={}
        self._connected_attrs={}# stores old connection before disconnect
        self._old_attr_values={}#stores old values before applying new attribute connections
        logger.debug("created edit context..")

    def __enter__(self):
        logger.debug("entering edit context..")
        return self

    def __exit__(self, *args):
        logger.debug("exit edit context..")

        #delete creates nodes
        logger.debug("deleting created nodes... %s", self._created_nodes)
        pm.delete(self._created_nodes)

        #restore attribute values
        logger.debug("restoring attribute values..")
        for attribute, value in self._attr_values.iteritems():
            logger.debug("restore attribute %s to value %s", attribute, value)
            attribute.set(value)

        # disconnect newly connected attrs
        logger.debug("restoring old attrs values")
        for attribute, value in self._old_attr_values.iteritems():
            logger.debug("restore attribute %s with value %s", attribute, value)
            attribute.disconnect()
            try:
                attribute.set(value)
            except:
                pass

        #reconnect attributes
        logger.debug("restoring disconnected attrs")
        for attribute, inputs in self._connected_attrs.iteritems():
            logger.debug("restore attribute %s to value %s", attribute, inputs)
            inputs[0].connect(attribute)




    def createNode(self, type):
        """
        Creates the node of given type
        """
        node=pm.createNode(type)
        self._created_nodes.append(node)
        logger.debug("created node %s", node)
        return node

    def setAttr(self, attribute, value):
        old_value=attribute.get()
        if attribute not in self._attr_values.keys():
            self._attr_values[attribute] = old_value
        attribute.set(value)
        logger.debug("set attribute %s with old value %s to new value %s", attribute, old_value, value)

    def connectAttr(self, attribute1, attribute2):
        """
        Connects attribute1 into attribute2
        """
        old_value=attribute2.get()
        self._old_attr_values[attribute2]=old_value
        logger.debug("Connecting attribute %s into attribute %s", attribute1, attribute2)
        attribute1.connect(attribute2)

    def disconnectAttr(self, attribute):
        self._connected_attrs[attribute]=attribute.inputs(p=True)
        logger.debug('disconnecting attribute %s', attribute)
        attribute.disconnect()


