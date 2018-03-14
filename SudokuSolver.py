from itertools import combinations

__author__ = 'cablome'
__project__ = 'SudokuSolver'

class CellNeighbors:
    """Aggregation of row, column, and grid cells related to a cell"""

    def __init__(self, index):
        # List cells in the same row
        row_start = index - index % 9
        self.row = [x for x in range(row_start, row_start + 9)
                    if x != index]
        self.column = [x for x in range(index % 9, 81, 9)
                       if x != index]
        self.grid = [x for x in range(81)
                     if x != index
                     and self.grid_index(x) == self.grid_index(index)]

    @staticmethod
    def grid_index(index):
        return 3 * (index // 27) + (index % 9) // 3

    def aggregate(self):
        return self.row + self.column + [x for x in self.grid
                                         if x not in self.row
                                         and x not in self.column]

    def info(self):
        print(self.row)
        print(self.column)
        print(self.grid)


class GridCell:
    """Fundamental cell data element"""

    def __init__(self, index):
        # When 9x9 grid cell array is row major, divmod() yields cell row and column
        x = divmod(index, 9)
        self.row_index = x[0]
        self.column_index = x[1]
        # Additional fu computes the 3x3 grid index starting from upper left
        self.grid = 3 * (self.row_index // 3) + self.column_index // 3
        # List of possible cell values, colloquially "pencil marks"
        # When cell value is determined, list length is 1
        self.PencilMarks = list(range(1, 10))
        # If cell array is considered as graph, each cell has 20 adjacent cells:
        # 8 in same row
        # 8 in same column
        # 4 in same 3x3 grid but _not_ in same row or column
        self.neighbors = CellNeighbors(index)
        # Flag indicates which cells to include in heuristic solver steps
        self.solved = False

    def info(self):
        print(self.row_index)
        print(self.column_index)
        print(self.grid)
        self.neighbors.info()

    def solve(self, value):
        self.PencilMarks = [value]
        self.solved = True

    def get_value(self):
        # convenience function for console printing
        if self.solved:
            return self.PencilMarks[0]
        else:
            return "X"

    def remove_mark(self, value):
        if value in self.PencilMarks:
            self.PencilMarks.remove(value)


class Puzzle:
    """encapsulates puzzle solving code"""

    def __init__(self, seed):
        self.cells = []
        for i in range(81):
            self.cells.append(GridCell(i))
            # cells[i].info()
        print("Cell Grid Initialized")
        for i in seed:
            # print(i)
            cell_index = 9 * i[0] + i[1]
            self.cells[cell_index].solve(i[2])
            for j in self.cells[cell_index].neighbors.aggregate():
                # print(j, cells[j].PencilMarks)
                self.cells[j].remove_mark(i[2])
                # print(j, cells[j].PencilMarks)

    def info(self):
        return [[x.get_value() for x in self.cells[9 * i:9 * (i + 1)]] for i in range(9)]

    def dump_marks(self):
        # dump pencil marks
        for i in range(81):
            if self.cells[i].solved:
                print(i, self.cells[i].PencilMarks[0])
            else:
                print(i, self.cells[i].PencilMarks)

    def solve(self):
        puzzle_solved = False
        working_set = [x for x in self.cells if not x.solved]
        unsolved_before = len(working_set)

        while not puzzle_solved:
            # deal with hidden and naked singles until none are found
            new_singles_set = self.process_singles(working_set)
            if len(new_singles_set) > 0:
                continue

            working_set = [x for x in self.cells if not x.solved]
            # check for hidden pairs
            self.process_hidden_pairs(working_set)

            # check for naked pairs
            self.process_naked_pairs(working_set)

            # keep rolling if new singles resulted from pairs checks
            new_singles_set = [y for y in [x for x in self.cells if not x.solved] if len(y.PencilMarks) == 1]
            if len(new_singles_set) > 0:
                continue

            # done with this solving iteration -- check progress
            working_set = [x for x in self.cells if not x.solved]
            unsolved_after = len(working_set)

            if unsolved_after == unsolved_before:
                return None
            unsolved_before = unsolved_after
            print("unsolved:" + str(unsolved_after))
            puzzle_solved = (unsolved_after == 0)
        return [self.cells[i].get_value() for i in range(81)]

    def process_naked_pairs(self, working_set):
        pair_candidate_set = [x for x in working_set if len(x.PencilMarks) == 2]
        for pair in combinations(pair_candidate_set, 2):
            if pair[0].PencilMarks == pair[1].PencilMarks:
                # may be a naked pair -- check for same section and process
                if pair[0].row_index == pair[1].row_index:
                    # same row -- remove pencil marks from others in row
                    for c in [self.cells[i] for i in pair[0].neighbors.row
                              if self.cells[i].column_index != pair[1].column_index]:
                        c.remove_mark(pair[0].PencilMarks[0])
                        c.remove_mark(pair[0].PencilMarks[1])
                if pair[0].column_index == pair[1].column_index:
                    # same column -- remove pencil marks from others in column
                    for c in [self.cells[i] for i in pair[0].neighbors.column
                              if self.cells[i].row_index != pair[1].row_index]:
                        c.remove_mark(pair[0].PencilMarks[0])
                        c.remove_mark(pair[0].PencilMarks[1])
                if pair[0].grid == pair[1].grid:
                    # same grid -- remove pencil marks from others in grid
                    for c in [self.cells[i] for i in pair[0].neighbors.grid
                              if self.cells[i].row_index != pair[1].row_index
                                 or self.cells[i].column_index != pair[1].column_index]:
                        c.remove_mark(pair[0].PencilMarks[0])
                        c.remove_mark(pair[0].PencilMarks[1])

    def process_hidden_pairs(self, working_set):
        neighbor_pairs = [p for p in combinations(working_set, 2)
                          if (len(set(p[0].PencilMarks)) > 2 or len(set(p[1].PencilMarks)) > 2)
                          and (p[0].row_index == p[1].row_index
                               or p[0].column_index == p[1].column_index
                               or p[0].grid == p[1].grid)]
        for pair in neighbor_pairs:
            hidden_pair = False
            shared_marks = set(pair[0].PencilMarks) | set(pair[1].PencilMarks)
            if pair[0].row_index == pair[1].row_index:
                mutual_neighbors = set(pair[0].neighbors.row) & set(pair[1].neighbors.row)
                mn_marks = [set(self.cells[i].PencilMarks) for i in mutual_neighbors]
                exclusive_marks = shared_marks - set.union(*mn_marks)
                hidden_pair = len(exclusive_marks) == 2
            elif pair[0].column_index == pair[1].column_index:
                mutual_neighbors = set(pair[0].neighbors.column) & set(pair[1].neighbors.column)
                mn_marks = [set(self.cells[i].PencilMarks) for i in mutual_neighbors]
                exclusive_marks = shared_marks - set.union(*mn_marks)
                hidden_pair = len(exclusive_marks) == 2
            elif not hidden_pair and pair[0].grid == pair[1].grid:
                mutual_neighbors = set(pair[0].neighbors.grid) & set(pair[1].neighbors.grid)
                mn_marks = [set(self.cells[i].PencilMarks) for i in mutual_neighbors]
                exclusive_marks = shared_marks - set.union(*mn_marks)
                hidden_pair = len(exclusive_marks) == 2

            if hidden_pair:
                # remove other pencil marks
                for mark in [x for x in pair[0].PencilMarks if x not in exclusive_marks]:
                    pair[0].remove_mark(mark)
                for mark in [x for x in pair[1].PencilMarks if x not in exclusive_marks]:
                    pair[1].remove_mark(mark)

    def process_singles(self, working_set):
        # seek out and process hidden singles
        multiple_mark_set = [k for k in working_set if len(k.PencilMarks) > 1]
        for i in multiple_mark_set:
            hidden_single = None
            for j in i.PencilMarks:
                # is pencil mark j unique in the row, column, or grid?
                if all(j not in self.cells[k].PencilMarks for k in i.neighbors.row) \
                        or all(j not in self.cells[k].PencilMarks for k in i.neighbors.column) \
                        or all(j not in self.cells[k].PencilMarks for k in i.neighbors.grid):
                    hidden_single = j
                    break

            if hidden_single is not None:
                i.PencilMarks = [hidden_single]
        # seek out and process naked singles
        naked_single_set = [y for y in working_set if len(y.PencilMarks) == 1]
        # print([x.PencilMarks for x in naked_single_set])
        for i in naked_single_set:
            i.solve(i.PencilMarks[0])
            # print(i.GetValue())
            for j in i.neighbors.aggregate():
                # print(j, self.cells[j].PencilMarks)
                self.cells[j].remove_mark(i.get_value())
                # print(j, self.cells[j].PencilMarks)
        new_singles_set = [y for y in [x for x in self.cells if not x.solved] if len(y.PencilMarks) == 1]
        return new_singles_set


if __name__ == "__main__":
    print("Hello World")
    # cells = []
    # for i in range(81):
    #     cells.append(GridCell(i))
    #     # cells[i].info()
    # print("Cell Grid Initialized")

    # Initial grid values as row/column/value tuples
    InitValues = [(0, 1, 8), (0, 4, 9), (0, 6, 3),
                  (1, 0, 3), (1, 3, 5), (1, 6, 1), (1, 8, 8),
                  (2, 2, 6), (2, 3, 3), (2, 4, 4),
                  (3, 0, 5), (3, 7, 7), (3, 8, 4),
                  (5, 0, 7), (5, 1, 1), (5, 8, 9),
                  (6, 4, 5), (6, 5, 6), (6, 6, 8),
                  (7, 0, 6), (7, 2, 1), (7, 5, 2), (7, 8, 7),
                  (8, 2, 5), (8, 4, 7), (8, 7, 3)]

    # for i in InitValues:
    #     # print(i)
    #     cellIndex = 9 * i[0] + i[1]
    #     cells[cellIndex].solve(i[2])
    #     for j in cells[cellIndex].neighbors.aggregate():
    #         # print(j, cells[j].PencilMarks)
    #         cells[j].RemoveMark(i[2])
    #         # print(j, cells[j].PencilMarks)

    myPuzzle = Puzzle(InitValues)

    # now print the initial puzzle
    # for i in range(9):
    #     print([x.GetValue() for x in cells[9 * i:9 * (i + 1)]])
    print(myPuzzle.info())

    print("Entering solving loop\n")

    answer = myPuzzle.solve()
    print(answer)

    # PuzzleSolved = False
    #
    # while not PuzzleSolved:
    #     workingSet = [x for x in cells if not x.solved]
    #     unsolvedBefore = len(workingSet)
    #     unsolvedAfter = unsolvedBefore
    #     # seek out and process hidden singles
    #     multipleMarkSet = [k for k in workingSet if len(k.PencilMarks) > 1]
    #     for i in multipleMarkSet:
    #         hiddenSingle = None
    #         for j in i.PencilMarks:
    #             # is pencil mark j unique in the row, column, or grid?
    #             if all(j not in cells[k].PencilMarks for k in i.neighbors.row) \
    #             or all(j not in cells[k].PencilMarks for k in i.neighbors.column) \
    #             or all(j not in cells[k].PencilMarks for k in i.neighbors.grid):
    #                 hiddenSingle = j
    #
    #         if hiddenSingle != None:
    #             i.PencilMarks = [hiddenSingle]
    #     # seek out and process naked singles
    #     nakedSingleSet = [y for y in workingSet if len(y.PencilMarks) == 1]
    #     # print([x.PencilMarks for x in nakedSingleSet])
    #     for i in nakedSingleSet:
    #         i.solve(i.PencilMarks[0])
    #         # print(i.GetValue())
    #         for j in i.neighbors.aggregate():
    #             # print(j, cells[j].PencilMarks)
    #             cells[j].RemoveMark(i.GetValue())
    #             # print(j, cells[j].PencilMarks)
    #         unsolvedAfter = unsolvedAfter - 1
    #     if (unsolvedAfter == unsolvedBefore):
    #         break
    #     PuzzleSolved = (unsolvedAfter == 0)

    # dump pencil marks
    myPuzzle.dump_marks()
    # for i in range(81):
    #     if cells[i].solved:
    #         print(i, cells[i].PencilMarks[0])
    #     else:
    #         print(i, cells[i].PencilMarks)
