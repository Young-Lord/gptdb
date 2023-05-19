#!/usr/bin/python3
import openai
from time import sleep
aa=1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111;aa=1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111;openai.api_key = "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"
aa=1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111;aa=1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111;openai.api_base = "https://chatgpt.nextweb.fun/api/openai/v1"

SYSTEM_CONTENT = '''You are a SQLite 3 API. You are operating a initialized empty database. Every user input should be processed as a SQLite command. If any error happened, return "raise OperationalError" (without quotes). If the command is a query and no error happened, return result as a Python tuple, which is the result of c.fetchall().__repr__() in Python. If no error happened and the command is not a query, return a single char "0". I want you to only reply with the result and nothing else. do not write explanations. do not type commands unless I instruct you to do so. do not explain anything even if the result is empty.
Examples:
Input: SELECT ,,
Output: raise OperationalError
Input: CREATE TABLE COMPANY( ID INT PRIMARY KEY     NOT NULL, NAME           TEXT );
Output: 0 
Input: SELECT * FROM COMPANY
Output: ()
'''

class OperationalError(Exception):
    pass

# code from https://zhuanlan.zhihu.com/p/610907785
class GPTDB:
    def __init__(self) -> None:
        self.conversation_list = [{'role':'system','content':SYSTEM_CONTENT}]
    
    def show_conversation(self,msg_list):
        for msg in msg_list:
            if msg['role'] == 'user':
                print(f"\U0001f47b: {msg['content']}\n")
            else:
                print(f"\U0001f47D: {msg['content']}\n")

    def ask(self, prompt) -> str:
        self.conversation_list.append({"role":"user","content":prompt})
        try:
            response = openai.ChatCompletion.create(temperature=0, model="gpt-3.5-turbo", messages=self.conversation_list)
        except openai.error.RateLimitError:
            print("! rate limit detected. retry in 21 seconds...")
            sleep(21)
            response = openai.ChatCompletion.create(temperature=0, model="gpt-3.5-turbo", messages=self.conversation_list)
        answer = response.choices[0].message['content']
        # print('*total token:', response['usage'])
        self.conversation_list.append({"role":"assistant","content":answer})
        return answer
    
    def execute(self, command) -> list:
        try:
            answer = self.ask(command)
        except Exception as e:
            print("*ask failed.")
            print("*conversation_list:", self.conversation_list)
            raise e
        if answer.startswith("raise "):
            print("*db exception.")
            print("*answer:", answer)
            print("*conversation_list:", self.conversation_list)
            raise eval(answer[6:])
        try:
            print("successfully returned. answer: "+answer)
            return eval(answer)
        except Exception as e:
            print("*eval failed.")
            print("*answer:", answer)
            print("*conversation_list:", self.conversation_list)
            raise e

    def close() -> None:
        pass

gptdb = GPTDB()
while 1:
    input_str = ""
    while 1:
        current = input()
        if current.strip() == "":
            break
        input_str += "\n"
        input_str += current
    print(gptdb.execute(input_str))


"""
CREATE TABLE COMPANY(
   ID INT PRIMARY KEY     NOT NULL,
   NAME           TEXT    NOT NULL,
   AGE            INT     NOT NULL,
   ADDRESS        CHAR(50),
   SALARY         REAL
);

INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY)
VALUES (1, 'Paul', 32, 'California', 20000.00 );

SELECT * FROM COMPANY;

SELECT ID,SALARY,AGE,AGE FROM COMPANY;

INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY)
VALUES (2, 'Allen', 25, 'Texas', 15000.00 );

INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY)
VALUES (3, 'Teddy', 23, 'Norway', 20000.00 );

INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY)
VALUES (4, 'Mark', 25, 'Rich-Mond ', 65000.00 );

INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY)
VALUES (5, 'David', 27, 'Texas', 85000.00 );

INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY)
VALUES (6, 'Kim', 22, 'South-Hall', 45000.00 );

SELECT sql FROM sqlite_master WHERE type = 'table' AND tbl_name = 'COMPANY';

"""
