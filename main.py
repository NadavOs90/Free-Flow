from Flow import Board as Board_Flow

if __name__ == '__main__':
    '''Size = 5 pairs as vortexes'''
    # pairs = [(4, 11), (5, 9), (19, 25), (20, 16), (17, 8)]
    # pairs = [(1, 15), (7, 9), (6, 14), (20, 21), (16, 19)]
    pairs = [(1, 22), (3, 17), (5, 19), (8, 23), (10, 24)]
    flow = Board_Flow(pairs=pairs)

    '''Size = 6 pairs as vortexes'''
    # pairs_6 = [(1, 25), (2, 31), (3, 15), (5, 21), (6, 33), (11, 27)]
    # flow = Board_Flow(size=6, pairs=pairs_6)

    '''Size = 7 pairs as coordinates'''
    # pairs_7 = [((1, 0), (3, 6)), ((6, 0), (4, 6)), ((1, 1), (5, 1)), ((3, 1), (5, 2)), ((3, 2), (5, 3)), ((3, 3), (2, 4)), ((5, 4), (4, 5))]
    # flow = Board_Flow(size=7, pairs=pairs_7)

    '''Random Generate a board'''
    # flow = Board_Flow()
    # flow = Board_Flow(size=8)

    '''Print the Board and the Solution Visually'''
    flow.print_board()
    print '\nSolution:'
    flow.print_board_with_solution()

    '''Print the Solution without the visualization'''
    # flow.solve()
