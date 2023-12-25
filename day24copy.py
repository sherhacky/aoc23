from time import time
import helpers
import itertools
from collections import defaultdict
import copy
import sys
import networkx as nx

input = helpers.get_input('input24.txt')
# input = helpers.get_input('input24test.txt')


p = []
v = []
for row in input:
    l, r = row.split(' @ ')
    p.append(eval('('+l+')'))
    v.append(eval('('+r+')'))


def path_intersection_point_x_y(p_1, v_1, p_2, v_2):
    m_1 = v_1[1] / v_1[0]
    m_2 = v_2[1] / v_2[0]
    b_1 = -m_1 * p_1[0] + p_1[1]
    b_2 = -m_2 * p_2[0] + p_2[1]
    if m_1 == m_2:
        return None, None, None, None
    x = (b_2 - b_1) / (m_1 - m_2)
    y = m_1 * (x - p_1[0]) + p_1[1]
    t_1 = (x - p_1[0]) / v_1[0]
    t_2 = (x - p_2[0]) / v_2[0]
    return x, y, t_1, t_2


def count_hailstone_collisions_in_test_area(p, v, min_val, max_val):
    result = 0
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            x, y, t_1, t_2 = path_intersection_point_x_y(
                p[i], v[i], p[j], v[j])

            if (x is not None) and (
                min(t_1, t_2) > 0
            ) and (
                min_val < min(x, y) < max(x, y) < max_val
            ):
                result += 1
    return result


# Part 1
print(count_hailstone_collisions_in_test_area(
    p, v, 200000000000000, 400000000000000))


# Part 2
def projection_to_normal_plane(v, n):
    k = len(v)
    n_part = sum(v[i]*n[i] for i in range(k)) / sum(n[i]*n[i]
                                                    for i in range(k))
    return tuple(
        v[i] - n_part * n[i] for i in range(k)
    )


def dot(u, v):
    return sum(u[i] * v[i] for i in range(len(u)))


def line_and_plane_intersection_point(p, v, n):
    k = len(p)
    t = - sum(n[i] * p[i] for i in range(k)) / sum(n[i] * v[i]
                                                   for i in range(k))
    return tuple(p[i] + t * v[i] for i in range(k))


# The idea here was to do a brute force search for the velocity vector of the
# thrown rock, i.e. find the vector parallel to the line intersecting all paths.
# Based on the input file it seemed reasonable to guess the max abs value of
# each coordinate in the desired velocity vector would be < 1000.
#
#   So, trying all such vectors, we took pairs of paths, given by p[i] + tv[i],
# p[j] + tv[j], projected both onto the plane with normal vector n, and used
# the same method as in Part 1 to determine an intersection point; from
# googling / intuition, 4 skew lines should be sufficient to determine the
# vector n.  So we restrict to a set of 4 paths and do the above procedure
# pairwise, saving the found intersection points to a set seen_points.  We know
# we've found the n we're looking for if the resulting
#
#   Besides being very inefficient, this had a crucial flaw in that the
# position values were large enough to introduce floating point errors.  Thus
# even when the function checked the actual desired vector n, it found a
# set seen_points with multiple intersection points, all within ~0.04 of
# eachother.
def search_for_vector_of_line_intersecting_all_paths(p, v, max_runtime=float('inf')):
    start_time = time()
    for n_x in range(1000):
        print('Searching with max(abs(n)) < {}, {}s elapsed'.format(
            n_x, round(time() - start_time, 2)
        ))
        if start_time - time() > max_runtime:
            print('Specified max runtime {}s exceeded'.format(max_runtime))
            return
        for n_y in range(n_x+1):
            for n_z in range(n_x+1):
                for coeff in itertools.product([-1, 1], repeat=2):
                    n = (coeff[0]*n_x, coeff[1]*n_y, n_z)
                    if n not in v and all(dot(n, vec) != 0 for vec in v):
                        q = [line_and_plane_intersection_point(
                            p[i], v[i], n
                        ) for i in range(0, 50, 10)]
                        u = [projection_to_normal_plane(
                            v[i], n) for i in range(10)]
                        seen_points = set()
                        for i in range(len(q)):
                            for j in range(i+1, len(q)):
                                if all(
                                    u[i][k] != 0 and u[j][k] != 0 for k in range(3)
                                ):
                                    x, y, t_1, t_2 = path_intersection_point_x_y(
                                        q[i], u[i], q[j], u[j]
                                    )
                                    if x:
                                        z_1 = q[i][2] + t_1 * u[i][2]
                                        z_2 = q[j][2] + t_2 * u[j][2]
                                        for z in [z_1, z_2]:
                                            seen_points.add((x, y, z))

                        # Drat. Rounding to the nearest integer might have worked..
                        rounded = {
                            tuple(
                                round(r[i], 6) for i in range(3)
                            ) for r in seen_points if r[0]
                        }

                        if len(rounded) == 1:
                            print(n, rounded)


start_time = time()


def diameter(pointset):
    return max(
        sum(
            (p[i] - q[i])**2 for i in range(len(p))
        ) for p, q in itertools.combinations(pointset, 2)
    )


# A modified version of the above function, but correcting the main issue
# by tracking the "best" set of intersection points seen thus far, ie, the
# set with minimum diameter.
def search_for_normal_vector_minimum_diameter(p, v, max_search=1000):
    best = float('inf')
    for n_x in range(1, max_search + 1):
        for n_y in range(1, n_x + 1):
            for n_z in range(1, n_x + 1):
                for coeff in itertools.product([-1, 1], repeat=2):
                    n = (coeff[0]*n_x, coeff[1]*n_y, n_z)
                    # Another arbitrary choice of 5 (because why not) lines to examine
                    if n not in v and all(dot(n, vec) != 0 for vec in v):
                        seen_points = set()
                        it = itertools.combinations(range(5, 9), 2)
                        it_t = itertools.combinations(range(5, 9), 2)
                        while len(seen_points) < 5 and any(it_t):
                            i, j = next(it)
                            q_0 = line_and_plane_intersection_point(
                                p[i], v[i], n)
                            q_1 = line_and_plane_intersection_point(
                                p[j], v[j], n)
                            u_0 = projection_to_normal_plane(v[i], n)
                            u_1 = projection_to_normal_plane(v[j], n)
                            if all(u_0[k] != 0 and u_1[k] != 0 for k in range(3)):
                                x, y, t_1, t_2 = path_intersection_point_x_y(
                                    q_0, u_0, q_1, u_1)
                                if x:
                                    z_1 = q_0[2] + t_1 * u_0[2]
                                    z_2 = q_1[2] + t_2 * u_1[2]
                                    for z in [z_1, z_2]:
                                        seen_points.add(
                                            tuple(round(r, 4)
                                                  for r in (x, y, z))
                                        )
                        if len(seen_points) > 1:
                            d = diameter(seen_points)
                            if d < best:
                                print('new best: n = {}, diameter = {}, {} points in intersection'.format(
                                    n, d, len(seen_points))
                                )
                                best = d
                        if not any(it_t) and len(seen_points) == 1:
                            print('done at last:', n, seen_points)


search_for_normal_vector_minimum_diameter(p, v, max_search=16)


# A souped up version.  This one speeds things up by focusing on just
# a window (1 / scale_factor_nbhd times (abs(a)) in size) around some 'good'
# candidate vector (a,b,c).
def search_for_normal_vector_minimum_diameter_target_and_nbhd(
    p, v, a, b, c, scale_factor_nbhd, max_search=1000
):
    best = float('inf')
    for n_x in range(a, max_search):
        for n_y in range(
            (n_x * b) // a - abs(a) // scale_factor_nbhd,
            (n_x * b) // a + abs(a) // scale_factor_nbhd
        ):
            for n_z in range(
                (n_x * c) // a - abs(a) // scale_factor_nbhd,
                (n_x * c) // a + abs(a) // scale_factor_nbhd
            ):
                n = (n_x, n_y, n_z)
                # Another arbitrary choice of 5 (because why not) lines to examine
                if n not in v and all(dot(n, vec) != 0 for vec in v[10:14]):
                    seen_points = set()
                    it = itertools.combinations(range(5, 9), 2)
                    it_t = itertools.combinations(range(5, 9), 2)
                    while len(seen_points) < 5 and any(it_t):
                        i, j = next(it)
                        q_0 = line_and_plane_intersection_point(p[i], v[i], n)
                        q_1 = line_and_plane_intersection_point(p[j], v[j], n)
                        u_0 = projection_to_normal_plane(v[i], n)
                        u_1 = projection_to_normal_plane(v[j], n)
                        if all(u_0[k] != 0 and u_1[k] != 0 for k in range(3)):
                            x, y, t_1, t_2 = path_intersection_point_x_y(
                                q_0, u_0, q_1, u_1)
                            if x:
                                z_1 = q_0[2] + t_1 * u_0[2]
                                z_2 = q_1[2] + t_2 * u_1[2]
                                for z in [z_1, z_2]:
                                    seen_points.add(
                                        tuple(round(r, 4) for r in (x, y, z))
                                    )
                    if len(seen_points) > 1:
                        d = diameter(seen_points)
                        if d < best:
                            print('new best: n = {}, diameter = {}, {} points in intersection'.format(
                                n, d, len(seen_points))
                            )
                            best = d
                    if not any(it_t) and len(seen_points) == 1:
                        print('done at last:', n, seen_points)


# Plugging one result of the above, n = (15, -13, 8), into this function:
print('Focus search near n=(15, -13, 8)')
search_for_normal_vector_minimum_diameter_target_and_nbhd(
    p, v, 15, -13, 8, scale_factor_nbhd=5, max_search=300
)


# Using the above eventually helped find the normal vector n:
n = (209, -180, 112)

# To find the starting point of our throw, translate by appropriate time t.
# Print any candidates not seen so far (but we always get the same point p,
# so we know it's right)
good_points = set()
for i in range(len(p)):
    for j in range(i + 1, len(p)):
        q_0 = line_and_plane_intersection_point(p[i], v[i], n)
        q_1 = line_and_plane_intersection_point(p[j], v[j], n)
        u_0 = projection_to_normal_plane(v[i], n)
        u_1 = projection_to_normal_plane(v[j], n)
        t_1_start = t = - sum(n[k] * p[i][k] for k in range(3)) / \
            sum(n[k] * v[i][k] for k in range(3))
        t_2_start = t = - sum(n[k] * p[j][k] for k in range(3)) / \
            sum(n[k] * v[j][k] for k in range(3))
        if all(u_0[k] != 0 and u_1[k] != 0 for k in range(3)):
            x, y, t_1, t_2 = path_intersection_point_x_y(
                q_0, u_0, q_1, u_1)

            t_1 = round(t_1_start + t_1)
            t_2 = round(t_2_start + t_2)

            p_1 = tuple(p[i][k] + t_1 * (v[i][k] - n[k]) for k in range(3))
            p_2 = tuple(p[j][k] + t_2 * (v[j][k] - n[k]) for k in range(3))
            for p_i in [p_1, p_2]:
                if p_i not in good_points:
                    print('Candidate point {}, final answer {}'.format(
                        p_i, sum(p_i)
                    ))
                    good_points.add(p_i)
