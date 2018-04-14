import itertools
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import cascaded_union, unary_union

def merge_cluster(pattern, p, visited_polygons):
    common_color = p.color_index
    cluster = []
    candidates = list(p.list_neighbours)
    while len(candidates) > 0:
        candidate_idx = candidates.pop()
        candidate = pattern.list_polygons[candidate_idx]
        if candidate not in visited_polygons and candidate.color_index == common_color:
            cluster.append(candidate)
            visited_polygons.add(candidate_idx)
            for neighbouring_candidate in candidate.list_neighbours:
                if neighbouring_candidate not in visited_polygons:
                    candidates.append(neighbouring_candidate)
    return cluster


def merge_polygons_to_sets(pattern):
    resulting_clusters = []
    visited_polygons = set()
    for idx, p in enumerate(pattern.list_polygons):
        if idx not in visited_polygons:
            cluster = merge_cluster(pattern, p, visited_polygons)
            if len(cluster) > 0:
                resulting_clusters.append(cluster)
    return resulting_clusters


def clusterize(pattern):
    print("Before polygonization: {}", len(pattern.list_polygons))
    clusters = merge_polygons_to_sets(pattern)
    print("After polygonize {}", len(clusters))
    return clusters
