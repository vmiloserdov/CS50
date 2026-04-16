from minesweeper import MinesweeperAI, Sentence

def simple_tests():
    ai1 = MinesweeperAI(3, 3)
    ai1.add_knowledge((0, 2), 1)
    ai1.knowledge.append(Sentence({(1, 0), (1, 1)}, 2))
    ai1.add_knowledge((2, 2), 0)
    
    print(f"Test 1 (Infer Multiple Mines):")
    if {(1, 0), (1, 1)}.issubset(ai1.mines):
        print("PASSED")
    else:
        print("FAILED")


    ai2 = MinesweeperAI(3, 3)
    ai2.knowledge.append(Sentence({(0, 0), (0, 1), (0, 2)}, 1))
    ai2.knowledge.append(Sentence({(0, 1), (0, 2)}, 1))
    ai2.add_knowledge((2, 2), 0)

    print(f"Test 2 (Subset Rule Safe Cell): ")
    if (0, 0) in ai2.safes:
        print("PASSED")
    else:
        print("FAILED")


def test_recursive_logic():
    ai = MinesweeperAI(3, 3)
    ai.knowledge.append(Sentence({(0, 0), (0, 1)}, 1))
    ai.knowledge.append(Sentence({(0, 1), (0, 2)}, 2))

    # Dummy move to trigger processing
    ai.add_knowledge((2, 2), 0)
    
    print("Test 3 (Recursive Logic):")
    
    if (0, 2) in ai.mines and (0, 0) in ai.safes:
        print("PASSED")
    else:
        print("FAILED")


def test_cleaning_new_knowledge():
    ai = MinesweeperAI(3, 3)
    ai.mark_mine((1, 1))
    ai.add_knowledge((0, 0), 1)
    
    print("Test 4 (Cleaning New Knowledge):")

    if (0, 1) in ai.safes:
        print("PASSED")
    else:
        print("FAILED")

if __name__ == "__main__":
    simple_tests()
    test_recursive_logic()
    test_cleaning_new_knowledge()