import pymongo

import SudokuSolver
import time



def check_new_entry():
    new = input("New entry of Sudoku question board? (y/n)")
    if new == "y":
        return True
    else:
        return False

def check_data_exist(collection, query):
    found = collection.find(query)
    clone_found = found.clone()
    if len(list(clone_found)) != 0:
        return (True, found)
    return (False, found)

def check_replace():
    replace = input("Replace existing question with new question? (y/n)")
    if replace.lower() == "y":
        print("false")
        return False
    return True

def remove_entry(collection, query):
    collection.delete_one(query)

def new_entry(collection, query):
    collection.insert_one(query)

def solve_trigger(question_board, collection, query, solution):
    '''for i in question_board:
        question = i["question"]'''
    SudokuSolver.Solution().solveSudoku(solution)
    qsDoc = {"question": question_board}
    solDoc = {"solution": solution}
    collection.update_many(
        query,
        {
            "$set":qsDoc
            })
    collection.update_many(
        query,
        {
            "$set":solDoc
            })
    print("Solution updated.")

def set_question():
    # manual question boards
    # ex0 - easy
    question_board = (
        [["2",".","1","8",".",".",".",".","4"],
        ["8","9",".","3",".",".","2","6","1"],
        [".","6","7","1",".","9",".",".","5"],
        [".",".","8",".",".","6",".",".","."],
        [".",".","3","5",".",".","6",".","."],
        [".",".","2","7","4","3",".","9","8"],
        [".",".",".",".",".",".",".","1","9"],
        ["5",".","9",".","3","2",".",".","6"],
        [".",".",".",".","1","7","4","5","2"]]
    ) 

    # ex1 - hard
    ''' question_board = (
        [[".",".",".",".",".","8","2","6","."],
        [".",".",".",".","5","1",".",".","3"],
        [".","6",".",".","4",".",".",".","1"],
        ["3",".",".",".",".","5","8",".","."],
        [".",".",".",".","8",".","6","9","."],
        ["2",".","4",".","1",".",".",".","."],
        ["5","4","9",".",".",".",".",".","8"],
        [".",".","2",".",".",".",".","3","."],
        ["8",".",".",".",".",".",".",".","."]]
    )  '''

    # # ex2 - hard
    # question_board = (
    #     [["9",".","3",".",".","5",".","8","."],
    #     [".","2",".","8",".",".",".",".","5"],
    #     [".",".",".",".","9","4",".",".","."],
    #     ["6","7","2","3",".",".",".",".","."],
    #     [".","5",".",".",".",".",".","1","."],
    #     [".",".",".",".",".","8","2","6","7"],
    #     [".",".",".","5","4",".",".",".","."],
    #     ["5",".",".",".",".","3",".","7","."],
    #     [".","6",".","7",".",".","5",".","9"]]
    # ) 
    # # ex3 - hard
    # question_board = (
    #     [[".",".","1",".","2","9",".",".","7"],
    #     [".",".","5",".","6",".",".","3","8"],
    #     [".",".",".","5",".","8","1",".","."],
    #     [".",".","8",".",".",".",".","1","2"],
    #     [".",".",".",".",".",".",".",".",".",],
    #     ["4","3",".",".",".",".","8",".","."],
    #     [".",".","9","7",".","6",".",".","."],
    #     ["7","5",".",".","1",".","2",".","."],
    #     ["6",".",".","9","5",".","4",".","."]]
    # )

    # ex4 - evil
    # question_board = (
    #     [[".",".",".",".",".",".",".",".","."],
    #     ["7","3",".","9",".",".",".",".","1"],
    #     [".","4",".",".","3","1",".","6","."],
    #     [".","7",".","2","5",".",".",".","4"],
    #     ["5",".",".",".",".",".",".",".","8"],
    #     ["2",".",".",".","8","9",".","3","."],
    #     [".","5",".","6","9",".",".","7","."],
    #     ["3",".",".",".",".","4",".","2","9"],
    #     [".",".",".",".",".",".",".",".","."]]
    # ) 

    # ex5 - master
    question_board = (
        [[".",".","1",".",".","4","8",".","."],
        [".",".","3","2","8",".",".",".","5"],
        [".","2",".",".",".","6",".",".","."],
        [".",".","5",".",".",".",".","7",".","."],
        [".","3",".","9","1",".","6",".","."],
        [".",".",".",".",".","2",".",".","."],
        [".","9",".","8","3",".","1",".","."],
        ["1",".",".",".",".",".",".",".","6"],
        [".",".",".",".","4",".",".",".","."]]
    )
    return question_board

    # temp
    ''' question_board = (
        [[".",],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        []]
    ) 
    '''

def main(DatabaseMode, ReadMode, OverwriteMode, client_address, collection_name, db_name, question_num, question_board, solution):
    # timer starts
    st = time.time()

    #client = pymongo.MongoClient("mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.1.5")
    # define variables
    client = pymongo.MongoClient(client_address)
    #collection_name = "example"
    #db_name = "sudoku"
    #question_num = input("Question number: ")
    question_name = "Q" + question_num
    query = {"name": question_name}
    db = client[db_name]
    collection = db[collection_name]
    #question_board = set_question()

    # Choose interaction with database
    if DatabaseMode:
        (exist, document) = check_data_exist(collection, query)
        if ReadMode:
            # Read from database
            if exist:
                for j in document:
                    question_board, solution = j["question"], j["solution"]
                return (question_board, solution)
            else:
                print("Entry not found.")
        else:
            # Write to database
            if exist:
                if OverwriteMode:
                    # code for exist + overwrite
                    remove_entry(collection, query)
                    new_entry(collection, query)
                    solve_trigger(question_board, collection, query, solution)
                else:
                    # code for exist + NOT overwrite
                    print("Entry exist and Overwrite mode is not activated.")
            else:
                # code for NOT exist
                new_entry(collection, query)
                solve_trigger(question_board, collection, query, solution)
    else:
        # Not saving solution
        # Generating solution only
        SudokuSolver.Solution().solveSudoku(solution)
        return (solution)

    # timer ends
    et = time.time()
    elapsed_time = et-st
    print("Execution time:", elapsed_time, "seconds")