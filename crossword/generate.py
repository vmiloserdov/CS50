import sys
from pprint import pprint
from collections import deque
from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # self.domains is a dictionary mapping of variables to the set of the possible values that they can take on
        # Variable() : set() of possible worlds
        for var in self.domains:
            self.domains[var] = set([word for word in self.domains[var] if len(word) == var.length])

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        overlaps = self.crossword.overlaps[(x, y)]

        if overlaps is None:
            return revised
        
        x_index = overlaps[0]
        y_index = overlaps[1]
        
        for x_option in self.domains[x].copy():
            
            # Let's say that we have chosen x_option as the value of x
            # x_option is a string that represents a possible word that variable x can take on
            y_exists_option = False
            for y_option in self.domains[y]:
                if y_option == x_option:
                    continue
                if x_option[x_index] == y_option[y_index]:
                    y_exists_option = True
                    break
            
            if not y_exists_option:
                self.domains[x].remove(x_option)
                revised = True
        
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None:
            # Only add the variables that actually have some intersections
            q = deque(
                var_pair 
                for var_pair, value in self.crossword.overlaps.items() 
                if value is not None
            )

        else:
            q = deque(arcs)

        while q:
            x, y = q.popleft()
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                
                for nbr in self.crossword.neighbors(x):
                    if nbr == y:
                        continue
                    q.append((nbr, x))

        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        return len(assignment) == len(self.crossword.variables)
    
    def unique(self, assignment):
        seen = set()
        for value in assignment.values():
            if value is None:
                continue
            
            if value in seen:
                return False
            
            seen.add(value)

        return True
    
    def length(self, assignment):
        for var, value in assignment.items():
            if value == None:
                continue

            if var.length != len(value):
                return False
            
        return True
    
    def conflict(self, assignment):             
        for key, value in self.crossword.overlaps.items():
            if value is None:
                continue

            (x, y), (x_index, y_index) = key, value
            if (assignment.get(x, None) is None) or (assignment.get(y, None) is None):
                continue

            if assignment[x][x_index] != assignment[y][y_index]:
                return True
            
        return False

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        return self.unique(assignment) and self.length(assignment) and (not self.conflict(assignment))

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        res = []
        nbrs = self.crossword.neighbors(var)

        for word in self.domains[var]:
            # See how many neighbors this assignment eliminates
            total_eliminated = 0
            for nbr in nbrs:
                var_index, nbr_index = self.crossword.overlaps[(var, nbr)]
                for nbr_word in self.domains[nbr]:
                    if word[var_index] != nbr_word[nbr_index]:
                        total_eliminated += 1
            
            res.append((word, total_eliminated))

        res.sort(key=lambda x: x[1])
        return [x[0] for x in res]

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned = [var for var in self.crossword.variables if var not in assignment]
        min_var = None
        min_var_domain = float('inf')

        for var in unassigned:
            domain_len = len(self.domains[var])
            if domain_len < min_var_domain:
                min_var = var
                min_var_domain = domain_len

        return min_var

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        
        var = self.select_unassigned_variable(assignment)
        for value in self.domains[var]:
            cpy = assignment.copy()
            cpy[var] = value

            if self.consistent(cpy):
                assignment[var] = value
                result = self.backtrack(assignment)

                if self.assignment_complete(result):
                    return result
                
            assignment[var] = None

        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
