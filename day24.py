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
    l,r = row.split(' @ ')
    p.append(eval('('+l+')'))
    v.append(eval('('+r+')')) 


def intersection_point_x_y(p_1, v_1, p_2, v_2):
    # print(p_1, v_1, p_2, v_2)
    x_1, y_1 = p_1[0], p_1[1]
    x_2, y_2 = p_2[0], p_2[1]
    vx_1, vy_1 = v_1[0], v_1[1]
    vx_2, vy_2 = v_2[0], v_2[1]
    if vx_1 - vx_2 != 0:
        t = (x_1 - x_2) / (vx_2 - vx_1)
    elif vy_1 - vy_2 != 0:
        t = (y_1 - y_2) / (vy_2 - vy_1)
    p_1 = (x_1 + t * vx_1, y_1 + t * vy_1)
    p_2 = (x_2 + t * vx_2, y_2 + t * vy_2)
    if p_1 == p_2:
        return t, p_1
    else:
        print(p_1, p_2)
        return None, None

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


def line_at_time(p, v, t):
    return tuple(p[i] + t * v[i] for i in range(len(p)))


def path_intersection_point(p_1, v_1, p_2, v_2):
    t_2 = (p_2[0] - p_1[0]) / (v_1[0] * (v_2[1] / v_1[1]) - 1)
    t_1 = (v_2[0] * t_2 - p_1[0] + p_2[0]) / v_1[0]
    print(p_1, p_2)
    print((v_1[0] * (v_2[1] / v_1[1]) - 1))
    print(t_1, t_2, line_at_time(p_1, v_1, t_1), line_at_time(p_2, v_2, t_2))


def test_path_function(p, v):
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            path_intersection_point(p[i], v[i], p[j], v[j])


def count_hailstone_collisions_in_test_area(p, v, min_val, max_val):
    result = 0
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            x, y, t_1, t_2 = path_intersection_point_x_y(p[i], v[i], p[j], v[j])
            print(p[i], p[j])
            print(x, y, t_1, t_2)

            if (x is not None) and (
                min(t_1, t_2) > 0
                ) and (
                min_val < min(x,y) < max(x,y) < max_val
            ):
                print('yer')
                result += 1
    return result


# print(count_hailstone_collisions_in_test_area(
#     p, v, 200000000000000, 400000000000000))

'''

279089400341912, 304994228698111, 304643844096319 @ 34, -53, -20
195198618527037, 395317981506666, 264675278567659 @ 34, -197, -134
'''


# for i in range(len(p)):
#     for j in range(i + 1, len(p)):
#         for k in range(3):
#             if v[i][k] == v[j][k]:
#                 print('t_{} == t_{} (mod {})'.format(
#                     i, j, max(p[i][k], p[j][k]) - min(p[i][k], p[j][k])
#                 ))


# 163165394977794, 345482543054781, 306898575876926 @ 190, 55, -357
# 171178400007298, 165283791547432, 246565404194007 @ 190, 186, 60

# for k_p in range(1000):
#     for f in [-1, 1]:
#         k = f * k_p
#         print('k:', k)
#         for c in range(3):
#             M = helpers.lcm([vel[c] - k for vel in v])
#             print(c, M)
#             for m in range(M+1):
#                 if all (
#                     (k == v[i][c] 
#                     # and p[i][0] % M == 0
#                     ) or (
#                         k != v[i][c] and
#                     (p[i][c] - m) % (k - v[i][c]) == 0) for i in range(len(v))
            
#                 ):
#                     print('a good one.', c, k, m)


def projects_to_integer_vector(n, v):
    if all(x == 0 for x in n):
        return False
    k = len(n)
    return sum(v[i]*n[i] for i in range(k)) % sum(n[i]*n[i] for i in range(k))


def projection_integer(v, n):
    k = len(v)
    n_part = sum(v[i]*n[i] for i in range(k)) // sum(n[i]*n[i] for i in range(k))
    return tuple(
        v[i] - n_part * n[i] for i in range(k)
    )


def projection_to_normal_plane(v, n):
    k = len(v)
    # print(v,n)
    # print(sum(v[i]*n[i] for i in range(k)))
    # print(sum(n[i]*n[i]
    #           for i in range(k)))
    n_part = sum(v[i]*n[i] for i in range(k)) / sum(n[i]*n[i]
                                                     for i in range(k))
    # print(n_part)
    return tuple(
        v[i] - n_part * n[i] for i in range(k)
    )


def dot(u, v):
    return sum(u[i] * v[i] for i in range(len(u)))

def line_and_plane_intersection_point(p, v, n):
    k = len(p)
    t = - sum(n[i] * p[i] for i in range(k)) / sum(n[i] * v[i] for i in range(k))
    #proj = projection_to_normal_plane(v, n)
    return tuple(p[i] + t * v[i] for i in range(k))


# for n_x in range(1000):
#     for n_y in range(n_x+1):
#         for n_z in range(n_x+1):
#             for coeff in itertools.product([-1, 1], repeat=2):
#                 n = (coeff[0]*n_x, coeff[1]*n_y, n_z)
#                 if n not in v and all(dot(n,vec) != 0 for vec in v):
#                 #and all(projects_to_integer_vector(n, u) for u in v):
#                     q = [line_and_plane_intersection_point(p[i], v[i], n) for i in range(0, 50, 10)]
#                     u = [projection_to_normal_plane(v[i], n) for i in range(10)]
#                     seen_points = set()
#                     for i in range(len(q)):
#                         for j in range(i+1, len(q)):
#                             if all(u[i][k] != 0 and u[j][k] != 0 for k in range(3)):
#                                 x, y, t_1, t_2 = path_intersection_point_x_y(
#                                     q[i], u[i], q[j], u[j])
#                                 if x:
#                                     z_1 = q[i][2] + t_1 * u[i][2]
#                                     z_2 = q[j][2] + t_2 * u[j][2]
#                                 else:
#                                     z_1, z_2 = None, None
#                                 for z in [z_2, z_2]:
#                                     seen_points.add((x,y, z))
#                     rounded = {
#                         tuple(round(r[i], 6) for i in range(3)) for r in seen_points if r[0]
#                     }
#                     # if n == (-3,1,2):
#                     #     print('it', rounded)

#                     if len(rounded) == 1:
#                         print(n, rounded)


# test_path_function(p, v)

# print(projection_to_normal_plane((-2, 1, -2), (-3, 1, 2)))
from time import time
start_time = time()


def diameter(pointset):
    return max(
        sum(
            (p[i] - q[i])**2 for i in range(len(p))
        ) for p, q in itertools.combinations(pointset, 2)
    )


n = (209, -180, 112)
for i in range(len(p)):
    for j in range(i + 1, len(p)):
        # print(i,j)
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
        print(i, j)
        t_1 = round(t_1_start + t_1)
        t_2 = round(t_2_start + t_2)
        # print(p[i], v[i], t_1_start + t_1)
        # print(p[j], v[j], t_2_start + t_2)
        p_1 = tuple(p[i][k] + t_1 * (v[i][k] - n[k]) for k in range(3))
        p_2 = tuple(p[j][k] + t_2 * (v[j][k] - n[k]) for k in range(3))
        print(p_1)
        print(p_2)
        print(sum(p_1))

a, b, c = 209, -180, 112
best = float('inf')
for n_x in range(a,300):
    if n_x % 25 == 0:
        print(n_x)
    for n_y in range(  (n_x * b) // a - abs(a) // 100, (n_x * b) // a + abs(a) // 100):
        for n_z in range(  (n_x * c) // a - abs(a) // 100, (n_x * c) // a + abs(a) // 100):
            # if n_x == n_y == n_z:
            #     print(n_x, time() - start_time)
            if True:
            # for coeff in itertools.product([-1, 1], repeat=2):
            #    n = (coeff[0]*n_x, coeff[1]*n_y, n_z)
                n = (n_x, n_y, n_z)
                if n not in v and all(dot(n,vec) != 0 for vec in v[10:14]):
                    seen_points = set()
                    it = itertools.combinations(range(5,9), 2)
                    it_t = itertools.combinations(range(5,9), 2)
                    while len(seen_points) < 5 and any(it_t): 
                        i,j = next(it)
                        # print(i,j)
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
                            print('new best:', n, d, len(seen_points))
                            best = d
                    if not any(it_t) and len(seen_points) == 1:
                        print('done at last:', n, seen_points)


