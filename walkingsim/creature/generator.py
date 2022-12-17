import os
import json

import networkx as nx

import pychrono as chrono


class ChronoCreature:
    _collision_family = 2

    def __init__(self, __creature: str, __graph: nx.Graph, pos: tuple) -> None:
        self.__creature = __creature
        self.__graph = __graph
        self.__pos = chrono.ChVectorD(pos[0], pos[1], pos[2])

        self.__joints = []
        self.__bodies = []

        self._create_morphology()

    def _create_bone(self, size: tuple):
        bone_material = chrono.ChMaterialSurfaceNSC()
        bone_material.SetFriction(0.5)
        bone_material.SetDampingF(0.2)
        #  bone_material.SetCompliance(0.0005)
        #  bone_material.SetComplianceT(0.0005)

        bone = chrono.ChBodyEasyBox(size[0], size[1], size[2], 1000, True, True, bone_material)
        bone.SetBodyFixed(False)
        bone.GetVisualShape(0).SetColor(chrono.ChColor(0.5, 0.7, 0.5))

        return bone

    def _create_body(self, index: int, pos: chrono.ChVectorD):
        meta = self.__graph.nodes[index]
        body_part = self._create_bone(meta['dimensions'])
        body_part.GetCollisionModel().SetFamily(self._collision_family)
        body_part.GetCollisionModel().SetFamilyMaskNoCollisionWithFamily(self._collision_family)
        body_part.SetPos(pos)
        self.__bodies.append(body_part)
        
        # FIXME: For debug purposes
        if index == 0:
            body_part.SetBodyFixed(True)

        print('Node {}, Pos: {}, Edges: {}'.format(index, pos, self.__graph.edges(nbunch=index)))
        for (edge_node1, edge_node2, edge_meta) in self.__graph.edges(nbunch=index, data=True):
            # TODO different types of joints?
            joint = chrono.ChLinkMotorRotationTorque()
            joint_pos = edge_meta['position']
            joint_frame = chrono.ChFrameD(chrono.ChVectorD(*joint_pos))

            # TODO how to find position of new part based on parent's pos?
            node2_dim = self.__graph.nodes[edge_node2]['dimensions']
            node2_body_part_pos = (joint_pos[0], joint_pos[1] - node2_dim[1] / 2, joint_pos[2])
            node2_body_part = self._create_body(edge_node2, chrono.ChVectorD(*node2_body_part_pos), body_part)

            joint.Initialize(body_part, node2_body_part, joint_frame)
            self.__joints.append(joint)

        return body_part

    def _create_morphology(self):
        # TODO how to choose automatically position of spawned creature wrt
        # the position of the ground?
        # TODO establish rules for joint placement
        # and collision box reductions in procedural generation
        self._create_body(0, self.__pos)

        # XXX torque function test
        for i, joint in enumerate(self.__joints):
            mod = 1 if i % 2 == 0 else -1
            sin_torque = chrono.ChFunction_Sine(
                0, 1, mod * 90  # phase [rad]  # frequency [Hz]
            )  # amplitude [Nm]
            joint.SetTorqueFunction(sin_torque)

    def add(self, __env):
        for body in self.__bodies:
            __env.Add(body)

        for joint in self.__joints:
            __env.Add(joint)


class CreatureGenerator:
    def __init__(self, __datapath: str, __engine: str) -> None:
        self.__datapath = __datapath
        self.__engine = __engine

        self.__creature = {
            'chrono': ChronoCreature
        }

    def generate_creature(self, __creature: str):
        filename = os.path.join(self.__datapath, f'{__creature}.json')
        with open(filename, 'r') as fp:
            creature_spec = json.load(fp)

        nodes = [
            (node['id'], node['meta']) for node in creature_spec['nodes']
        ]

        edges = [
            (*edge['nodes'], edge['meta']) for edge in creature_spec['edges']
        ]

        creature_graph = nx.MultiDiGraph()
        creature_graph.add_nodes_from(nodes)
        creature_graph.add_edges_from(edges)

        return self.__creature[self.__engine](__creature, creature_graph, (0, 1.9, 0))
