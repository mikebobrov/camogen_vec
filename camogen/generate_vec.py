from shapely.geometry import box, Polygon, MultiPolygon, GeometryCollection, Point, LineString
from shapely.ops import split
from shapely.affinity import scale
from shapely.ops import cascaded_union
import svgwrite

import numpy as np

from camogen.vec_pattern import VecPattern
from camogen.vec_polygon import VecPolygon


def edge_split(v1, v2, frac):
    if v1[0] < v2[0]:
        new_x = v1[0] + np.abs(v2[0] - v1[0]) * frac
    else:
        new_x = v1[0] - np.abs(v2[0] - v1[0]) * frac

    if v1[1] < v2[1]:
        new_y = v1[1] + np.abs(v2[1] - v1[1]) * frac
    else:
        new_y = v1[1] - np.abs(v2[1] - v1[1]) * frac

    return new_x, new_y


def new_edge(va1, va2, vb1, vb2):
    frac_a = 0.4 + np.random.randint(3) / 10
    frac_b = 0.4 + np.random.randint(3) / 10

    # frac_a = np.random.random()
    # frac_b = np.random.random()

    # Split Edge A
    new_vert_a = edge_split(va1, va2, frac_a)

    # Split Edge B
    new_vert_b = edge_split(vb1, vb2, frac_b)

    return scale(LineString([new_vert_a, new_vert_b]), 1.3, 1.3)


def distance_vertices(c1, c2):
    return Point(c1).distance(Point(c2))


def generate_polygons(pattern, polygon, depth):
    # Check if the circumference of the Polygon is small enough. If it's the case, we stop the recursion
    # We also check if we did enough recursive call. If it's the case, we also stop the recursion
    if polygon.length < pattern.polygon_size or depth <= 0:
        # print('{} {} {}'.format(polygon.length, depth, polygon.wkt))
        pattern.add_polygon(VecPolygon(polygon))
        pass
    else:

        # If none of these two conditions is fulfilled, we continue the recursive call
        # Compute the number of edges for this Polygon
        polygon_coords = polygon.boundary.coords
        nbr_edges = len(polygon.boundary.coords)

        # Make a list of all the edges length
        edge_lengths = []

        for i in range(nbr_edges):
            edge_lengths.append(
                distance_vertices(polygon_coords[i], polygon_coords[(i + 1) % nbr_edges]))

        # We sort the edges in function of their lengths. We are interested in the indices
        idx_edge_sorted = np.argsort(edge_lengths)[::-1]

        # Let's take the two biggest edges
        # WARNING: We need to have them in order for the polygon splitting to work properly.
        # Therefore, a is the edge with the smallest index
        idx_edge_a = min(idx_edge_sorted[0], idx_edge_sorted[1])
        idx_edge_b = max(idx_edge_sorted[0], idx_edge_sorted[1])

        # We need to get the vertices of these edges
        va1 = polygon_coords[int(idx_edge_a)]
        va2 = polygon_coords[int((idx_edge_a + 1) % nbr_edges)]

        vb1 = polygon_coords[int(idx_edge_b)]
        vb2 = polygon_coords[int((idx_edge_b + 1) % nbr_edges)]

        edge_c = new_edge(va1, va2, vb1, vb2)

        n_polygons = split(polygon, edge_c)

        for n_polygon in n_polygons:
            generate_polygons(pattern, n_polygon, depth - 1)


def find_neighbours(pattern):
    for polygon in pattern.list_polygons:
        for candidate in pattern.list_polygons:
            if polygon == candidate:
                pass
            else:
                if polygon.geom.touches(candidate.geom):
                    polygon.add_neighbour(candidate)


def touches_cluster(cluster, polygon):
    if len(cluster) > 0:
        return cascaded_union([p.geom for p in cluster]).touches(polygon.geom)
    else:
        return True


def merge_cluster(polygon, visited_polygons, bleed):
    cluster = []
    candidates = [polygon]
    candidates.extend(list(polygon.list_neighbours))
    current_bleed = bleed
    while len(candidates) > 0 and current_bleed >= 0:
        candidate = candidates.pop()
        if candidate not in visited_polygons:
            if touches_cluster(cluster, candidate):
                cluster.append(candidate)
                visited_polygons.add(candidate)
                current_bleed = current_bleed - 1
                current_cluster_polygon = cascaded_union([p.geom for p in cluster])
                for neighbouring_candidate in candidate.list_neighbours:
                    if neighbouring_candidate not in visited_polygons and current_cluster_polygon.touches(neighbouring_candidate.geom):
                        candidates.append(neighbouring_candidate)
    return cluster


def merge_polygons_to_clusters(pattern):
    resulting_clusters = []
    visited_polygons = set()
    for idx, p in enumerate(pattern.list_polygons):
        if idx not in visited_polygons:
            cluster = merge_cluster(p, visited_polygons, pattern.color_bleed)
            if len(cluster) > 0:
                resulting_clusters.append(cluster)
    return resulting_clusters


# def write_svg(polygons, file_name):
#     with open(file_name, 'w') as f:
#         f.write('''<?xml version="1.0" encoding="utf-8" ?>
# <svg baseProfile="full" height="812" version="1.1" width="735" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink">''')
#         for p in polygons:
#             f.write(p.svg())
#         f.write('</svg>')


def polygon_path_vec(draw_svg, points, color):
    path_string = ''
    for idx, point in enumerate(points):
        if idx == 0:
            path_string = 'M{},{}'.format(point[0], point[1])
        else:
            path_string = path_string + ' L{},{}'.format(point[0], point[1])

    path_string = path_string + ' Z'
    draw_svg.add(draw_svg.path(d=path_string, fill=color, stroke='none'))

def polygon_path_vec_bezier(draw_svg, points, color):
    path_string = ''
    for idx, point in enumerate(points):
        if idx == 0:
            path_string = 'M{},{}'.format(point[0], point[1])
        else:
            path_string = path_string + ' T{},{}'.format(point[0], point[1])

    path_string = path_string + ' T{},{}'.format(points[0][0], points[0][1])

    path_string = path_string + ' Z'
    draw_svg.add(draw_svg.path(d=path_string, fill=color, stroke='none'))


def draw_polygons(result, polygons, pattern):
    for polygon in polygons:
        color = pattern.colors[np.random.randint(len(pattern.colors))]
        # polygon_path_vec(result, polygon.boundary.coords, color)
        polygon_path_vec_bezier(result, polygon.boundary.coords, color)


def generate(parameters, file_name):
    """
     Generate the Camouflage pattern given the parameters

     :param parameters: Dictionnary of parameters
     :return: Image with the camouflage pattern
     """

    pattern = VecPattern(parameters)

    starting_polygon = Polygon(
        [
            (pattern.width, 0),
            (0, 0),
            (0, pattern.height),
            (pattern.width, pattern.height),
        ]
    )

    # Generate a rough sketch of the pattern
    generate_polygons(pattern, starting_polygon, pattern.max_depth)
    find_neighbours(pattern)
    pattern.shuffle_polygons()
    clusters = merge_polygons_to_clusters(pattern)
    clusterized_polygons = []
    for cluster in clusters:
        geometries = [scale(p.geom,1.5,1.5) for p in cluster]
        union = cascaded_union(geometries)
        clusterized_polygons.append(union)

    result = svgwrite.Drawing('1.svg', size=(pattern.width.item(), pattern.height.item()))

    # draw_polygons_vec(result, pattern)
    # pixelize_vec(pattern, image, result)
    draw_polygons(result, clusterized_polygons, pattern)
    result.save()

    # Shuffle the polygons
    # pattern.suffle_polygons()

    # for p in pattern.list_polygons:
    #     for p1 in pattern.list_polygons:
    #         if p != p1 and p.intersects(p1):
    #             print('---')
    #             print(p1.svg())
    #             print(p.svg())
    #             print('---')

    # Generate the image
    # generate_image(pattern, file_name)
