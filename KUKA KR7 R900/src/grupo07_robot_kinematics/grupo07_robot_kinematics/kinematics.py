import numpy as np


L1 = -0.34200
L2 =  0.05000
L3 =  0.41000
L4 =  0.00000
L5 =  0.04500
L6 = -0.44000
L7 = -0.07700


TB = np.array([
    [1.0,  0.0,  0.0,  0.0],
    [0.0, -1.0,  0.0,  0.0],
    [0.0,  0.0, -1.0,  0.0],
    [0.0,  0.0,  0.0,  1.0]
], dtype=float)


def get_dh_matrices(q):

    q = np.asarray(
        q,
        dtype=float
    )

    if q.shape != (6,):

        raise ValueError(
            "q debe contener 6 articulaciones"
        )


    q1 = q[0]
    q2 = q[1]
    q3 = q[2]
    q4 = q[3]
    q5 = q[4]
    q6 = q[5]


    c1 = np.cos(q1)
    s1 = np.sin(q1)

    c2 = np.cos(q2)
    s2 = np.sin(q2)

    c3 = np.cos(q3)
    s3 = np.sin(q3)

    c4 = np.cos(q4)
    s4 = np.sin(q4)

    c5 = np.cos(q5)
    s5 = np.sin(q5)

    c6 = np.cos(q6)
    s6 = np.sin(q6)


    A1 = np.array([
        [ c1,  0.0,  s1, L2*c1],
        [ s1,  0.0, -c1, L2*s1],
        [0.0,  1.0,  0.0, L1],
        [0.0,  0.0,  0.0, 1.0]
    ], dtype=float)


    A2 = np.array([
        [ c2, -s2, 0.0, L3*c2],
        [ s2,  c2, 0.0, L3*s2],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ], dtype=float)


    A3 = np.array([
        [ s3, 0.0, -c3,  L5*s3],
        [-c3, 0.0, -s3, -L5*c3],
        [0.0, 1.0, 0.0, L4],
        [0.0, 0.0, 0.0, 1.0]
    ], dtype=float)


    A4 = np.array([
        [ c4,  0.0, -s4, 0.0],
        [ s4,  0.0,  c4, 0.0],
        [0.0, -1.0,  0.0, L6],
        [0.0,  0.0,  0.0, 1.0]
    ], dtype=float)


    A5 = np.array([
        [ c5, 0.0,  s5, 0.0],
        [ s5, 0.0, -c5, 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ], dtype=float)


    A6 = np.array([
        [ c6, -s6, 0.0, 0.0],
        [ s6,  c6, 0.0, 0.0],
        [0.0, 0.0, 1.0, L7],
        [0.0, 0.0, 0.0, 1.0]
    ], dtype=float)


    return (
        A1,
        A2,
        A3,
        A4,
        A5,
        A6
    )


def forward_kinematics(q):

    (
        A1,
        A2,
        A3,
        A4,
        A5,
        A6

    ) = get_dh_matrices(q)


    T01 = TB @ A1

    T02 = T01 @ A2

    T03 = T02 @ A3

    T04 = T03 @ A4

    T05 = T04 @ A5

    T06 = T05 @ A6


    return T06


def tcp_position(q):

    T06 = forward_kinematics(q)

    x = T06[0, 3]
    y = T06[1, 3]
    z = T06[2, 3]

    return np.array([
        x,
        y,
        z
    ])