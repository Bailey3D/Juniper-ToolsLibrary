import hou

import juniper.utilities.math

import hou.juniper.utilities.maths as maths


class _SCAttractionPoint(object):
    """Class for an individual attraction point in the space colonisation algorithm"""
    def __init__(self, generator, position):
        self.generator = generator
        self.position = position
        self.nearest_end_point = None  # previous nearest end point - for caching purposes
        self.active = True  # is the attraction point active? Saves removing from "active_end_points" arrays


class _SCNode(object):
    """Class for a node in the space colonisation algorithm"""
    def __init__(self, generator, position=None, parent=None):
        self.generator = generator

        self.position = position
        self.children = []
        self.parent = parent
        self.branch_level = 0

        if(self.parent):
            self.parent.add_child(self)
            if(self.parent.num_children > 0):
                self.branch_level = self.parent.branch_level + 1
            else:
                self.branch_level = self.parent.branch_level

    def add_child(self, child):
        self.children.append(child)

    @property
    def num_children(self):
        return len(self.children)

    @property
    def can_add_child(self):
        if(self.num_children > 0 and self.branch_level >= self.generator.max_branch_levels):
            return False
        if(self.num_children >= self.generator.max_branchlets):
            return False
        return True


class RootsGenerator(object):
    def __init__(self, node_points, node_attraction_points, attraction_radius=100.0, attraction_deadzone=5.0, max_branch_levels=4, max_branchlets=4, num_cycles=4, max_cycles=16, render_attraction_points=False):
        """Generates roots from various input data
        :param <hou.node:node_points> Houdini node containing points to begin calculations at
        :param <hou.node:node_attraction_points> Houdini node containing points to act as attraction points
        :param [<float:attraction_radius>] Attraction radius for each attraction point
        :param [<float:attraction_deadzone>] Minimum distance a point can be from a node before it is considered occupied
        :param [<int:max_branch_levels>] Maximum branch levels allowed
        :param [<int:max_branchlets>] Maximum branchlets allowed at each node split
        :param [<bool:render_attraction_points>] Debug - should attraction points be rendered?
        """

        self.node_points = node_points
        self.node_attraction_points = node_attraction_points
        self.attraction_radius = attraction_radius
        self.attraction_deadzone = attraction_deadzone
        self.max_branch_levels = max_branch_levels
        self.max_branchlets = max_branchlets
        self.max_cycles = max_cycles
        self.num_cycles = min(num_cycles, self.max_cycles)

        self.render_attraction_points = render_attraction_points

        self.available_attraction_points = self.attraction_positions

        self.points = []
        self.newest_points = []

        self.run()

    # ------------------------------------------------------------------

    @property
    def geo_points(self):
        return self.node_points.geometry()

    @property
    def geo_attraction_points(self):
        return self.node_attraction_points.geometry()

    # ------------------------------------------------------------------

    @property
    def start_positions(self):
        """"""
        return [i.position() for i in self.geo_points.points()]

    @property
    def attraction_positions(self):
        """"""
        output = []
        for i in self.geo_attraction_points.points():
            output.append(_SCAttractionPoint(self, i.position()))
        return output

    # ------------------------------------------------------------------

    def run(self):

        for i in self.start_positions:
            base_point = _SCNode(
                self,
                position=i,
                parent=None
            )
            self.points.append(base_point)
            self.newest_points.append(base_point)

        def __get_nearest_end(position):
            """Closest end point to a given position"""
            closest_point = None
            closest_distance_squared = None

            target_arrays = [self.newest_points]
            if(position.nearest_end_point):
                target_arrays.append((position.nearest_end_point,))

            for i in target_arrays:
                for ep in i:
                    d = abs((ep.position - position.position).lengthSquared())
                    if((closest_distance_squared is None) or (d < closest_distance_squared)):
                        if(ep.can_add_child):
                            closest_distance_squared = d
                            closest_point = ep

            position.nearest_end_point = closest_point
            return closest_point

        def __cycle():
            num_added = 0

            ends_children = {}

            for ap in self.available_attraction_points[::-1]:
                if(ap.active):
                    # closest point to the current attractor
                    closest_point = __get_nearest_end(ap)

                    if(closest_point.position.distanceTo(ap.position) < self.attraction_radius):
                        if(closest_point not in ends_children):
                            ends_children[closest_point] = [ap.position]
                        else:
                            ends_children[closest_point].append(ap.position)

            for ep in ends_children:
                end_point_attractor_average_position = maths.average_vector3(ends_children[ep])
                new_point = _SCNode(
                    self,
                    position=end_point_attractor_average_position,
                    parent=ep
                )

                self.points.append(new_point)
                self.newest_points.append(new_point)
                num_added += 1

            for ap in self.available_attraction_points[::-1]:
                if(ap.active):
                    closest_point = __get_nearest_end(ap)
                    d = closest_point.position.distanceTo(ap.position)
                    if(d < self.attraction_deadzone):
                        ap.active = False

            self.newest_points = []
            return num_added

        num_cycles = 0
        while(self.available_attraction_points and num_cycles < self.num_cycles):
            num_added = __cycle()
            if(num_added == 0):
                num_cycles = self.num_cycles
            num_cycles += 1

        self.geo_points.deletePoints(self.geo_points.points())

        if(self.render_attraction_points):
            for i in self.available_attraction_points:
                if(i.active):
                    p = self.geo_points.createPoint()
                    p.setPosition(i.position)

        else:
            for i in self.points:
                if(i.parent):
                    p = self.geo_points.createPoint()
                    p.setPosition(i.position)
                    p.setAttribValue("branch_level", i.branch_level)

                    pp = self.geo_points.createPoint()
                    pp.setPosition(i.parent.position)
                    pp.setAttribValue("branch_level", i.branch_level)

                    poly = self.geo_points.createPolygon()
                    poly.addVertex(p)
                    poly.addVertex(pp)
