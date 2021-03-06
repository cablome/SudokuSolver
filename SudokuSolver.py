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
            # print(self.info())
            # deal with hidden and naked singles until none are found
            new_singles_set = self.process_singles(working_set)
            if len(new_singles_set) > 0:
                continue

            working_set = [x for x in self.cells if not x.solved]

            # check for pairs
            # keep rolling if new singles resulted from pairs checks
            new_singles_set = self.reduce_r(working_set, 2)
            if len(new_singles_set) > 0:
                continue

            # check for triples
            # keep rolling if new singles resulted from triples checks
            new_singles_set = self.reduce_r(working_set, 3)
            if len(new_singles_set) > 0:
                continue

            # done with this solving iteration -- check progress
            working_set = [x for x in self.cells if not x.solved]
            unsolved_after = len(working_set)

            if unsolved_after == unsolved_before:
                return None
            unsolved_before = unsolved_after
            print("unsolved:" + str(unsolved_after))
            # print(self.info())
            puzzle_solved = (unsolved_after == 0)
        return [self.cells[i].get_value() for i in range(81)]

    def process_pointing_pairs(self, working_set):
        neighbor_pairs = [p for p in combinations(working_set, 2)
                          if (p[0].row_index == p[1].row_index
                              or p[0].column_index == p[1].column_index)
                          and p[0].grid == p[1].grid]
        for pair in neighbor_pairs:
            mutual_neighbors = set.intersection(*[set(p.neighbors.grid) for p in pair])
            shared_marks = set.union(*[set(p.PencilMarks) for p in pair])
            mn_marks = [set(self.cells[i].PencilMarks) for i in mutual_neighbors]
            exclusive_marks = shared_marks - set.union(*mn_marks)
            pointing_candidate = len(exclusive_marks) == 1
            if pointing_candidate and pair[0].row_index == pair[1].row_index:
                # remove the pointing pair symbol from other cells in the row
                mark = exclusive_marks.pop()
                for j in set(pair[0].neighbors.row) & set(pair[1].neighbors.row):
                    self.cells[j].remove_mark(mark)

            elif pointing_candidate and pair[0].column_index == pair[1].column_index:
                # remove the pointing pair symbol from other cells in the column
                mark = exclusive_marks.pop()
                for j in set(pair[0].neighbors.column) & set(pair[1].neighbors.column):
                    self.cells[j].remove_mark(mark)

    def reduce_r(self, working_set, r):
        # consider one section (row, column, grid) at a time
        for i in range(9):
            working_row = [x for x in working_set if x.row_index == i and len(x.PencilMarks) > 1]
            for cell_tuple in combinations(working_row, r):
                shared_marks = set.union(*[set(p.PencilMarks) for p in cell_tuple])
                mutual_neighbors = set.intersection(*[set(p.neighbors.row) for p in cell_tuple])
                mn_marks = [set(self.cells[i].PencilMarks) for i in mutual_neighbors]
                exclusive_marks = shared_marks - set.union(*mn_marks)

                if len(exclusive_marks) == r:
                    if len(shared_marks) > len(exclusive_marks):
                        for cell in cell_tuple:
                            for mark in shared_marks - exclusive_marks:
                                cell.remove_mark(mark)
                    else:
                        for neighbor in mutual_neighbors:
                            for mark in shared_marks:
                                self.cells[neighbor].remove_mark(mark)

            working_column = [x for x in working_set if x.column_index == i and len(x.PencilMarks) > 1]
            for cell_tuple in combinations(working_column, r):
                shared_marks = set.union(*[set(p.PencilMarks) for p in cell_tuple])
                mutual_neighbors = set.intersection(*[set(p.neighbors.column) for p in cell_tuple])
                mn_marks = [set(self.cells[i].PencilMarks) for i in mutual_neighbors]
                exclusive_marks = shared_marks - set.union(*mn_marks)

                if len(exclusive_marks) == r:
                    if len(shared_marks) > len(exclusive_marks):
                        for cell in cell_tuple:
                            for mark in shared_marks - exclusive_marks:
                                cell.remove_mark(mark)
                    else:
                        for neighbor in mutual_neighbors:
                            for mark in shared_marks:
                                self.cells[neighbor].remove_mark(mark)

            working_grid = [x for x in working_set if x.grid == i and len(x.PencilMarks) > 1]
            for cell_tuple in combinations(working_grid, r):
                shared_marks = set.union(*[set(p.PencilMarks) for p in cell_tuple])
                mutual_neighbors = set.intersection(*[set(p.neighbors.grid) for p in cell_tuple])
                mn_marks = [set(self.cells[i].PencilMarks) for i in mutual_neighbors]
                exclusive_marks = shared_marks - set.union(*mn_marks)

                if len(exclusive_marks) == r:
                    if len(shared_marks) > len(exclusive_marks):
                        for cell in cell_tuple:
                            for mark in shared_marks - exclusive_marks:
                                cell.remove_mark(mark)
                    else:
                        for neighbor in mutual_neighbors:
                            for mark in shared_marks:
                                self.cells[neighbor].remove_mark(mark)
        self.process_pointing_pairs(working_set)
        return [y for y in [x for x in self.cells if not x.solved] if len(y.PencilMarks) == 1]

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

    # dump pencil marks
    myPuzzle.dump_marks()
