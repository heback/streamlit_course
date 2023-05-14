# 사용할 패키지 가져오기
import sqlite3


# TodoDB 클래스 정의
class TodoDB:

    # con 클래스변수, 클래스변수는 클래스 이름으로 접근
    # TodoDB.con
    con = None

    # 클래스 메서드
    @staticmethod # 클래스 메서드임을 알리는 decorator
    def connectToDatabase():
        try: # try ~ except
            # 데이터베이스 연결, todo.db가 없으면 새로 생성해서 연결
            # check_same_thread=False : 다중 접속을 허용
            TodoDB.con = sqlite3.connect('todo.db', check_same_thread=False)

            # 데이터베이스에 명령(SQL)을 전달하기 위한 커서 얻기
            c = TodoDB.con.cursor()

            # 명령 실행
            c.execute(f'CREATE TABLE IF NOT EXISTS tasks ' # 테이블 생성(없다면), 있으면 패스
                      f'(id INTEGER PRIMARY KEY AUTOINCREMENT,' # 속성 PK
                      f'todo_content TEXT NOT NULL,'            # 속성
                      f'todo_date TEXT NOT NULL,'               # 속성
                      f'todo_time TEXT,'                        # 속성
                      f'completed NUMERIC NOT NULL,'            # 속성
                      f'reg_date TEXT NOT NULL)')               # 속성
            c.execute(f'CREATE TABLE IF NOT EXISTS users ' # 테이블 생성(없다면), 있으면 패스
                      f'(id INTEGER PRIMARY KEY AUTOINCREMENT,' # 속성 PK
                      f'user_name TEXT NOT NULL,'               # 속성
                      f'user_gender TEXT NOT NULL,'             # 속성
                      f'user_id TEXT NOT NULL,'                 # 속성
                      f'user_pw TEXT NOT NULL,'                 # 속성
                      f'user_email TEXT NOT NULL,'              # 속성
                      f'user_mobile TEXT NOT NULL,'             # 속성    
                      f'reg_date TEXT NOT NULL)')               # 속성
            # DDL(CREATE), DML(INSERT, UPDATE, DELETE) 명령 실행 후 데이터베이스 파일에 반영
            TodoDB.con.commit()
        except Exception as e:
            print(e)

    # 멤버 메서드, self는 객체 자신을 가리킨다.
    def readTodos(self):
        c = TodoDB.con.cursor()
        # SELECT 속성1, 속성2, ...
        # SELECT * : 모든 속성
        # FROM 테이블 이름
        c.execute('SELECT * FROM tasks')
        # SELECT 문을 실행한 다음에는 결과를 받아서 반환한다.
        # 결과가 하나 뿐일 때는 fetchone()
        res = c.fetchall()
        return res

    # 할일 검색
    def findTodos(self, task, date):
        c = TodoDB.con.cursor()
        # WHERE 조건절, 조건에 포함될 속성에 대한 조건을 지정함
        # LIKE 는 포함 연산자
        # %str% : str을 포함
        # str% : str로 시작
        # %str : str로 끝남
        c.execute(f"SELECT * FROM tasks WHERE todo_content LIKE '%{task}%' AND todo_date LIKE '{date}%'")
        res = c.fetchall()
        return res

    def insertTodo(self, values):
        c = TodoDB.con.cursor()
        # INSERT INTO 테이블 이름
        # (속성1, 속성2, ... )
        # VALUES (값1, 값2, ... )
        # 속성 개수와 값 개수가 반드시 같아야 함
        c.execute('INSERT INTO tasks (todo_content, todo_date, todo_time, completed, reg_date)'
                  ' VALUES (?, ?, ?, ?, ?)', values)
        TodoDB.con.commit()
        return c.lastrowid

    def deleteTodo(self, id):
        c = TodoDB.con.cursor()
        # 테이블에서 레코드 삭제
        # DELETE FROM 테이블 이름
        # WHERE 조건절
        c.execute(f'DELETE FROM tasks WHERE id={id}')
        TodoDB.con.commit()

    def updateTodo(db, values):
        c = TodoDB.con.cursor()
        # 테이블에서 레코드 수정
        # UPDATE 테이블 이름
        # SET 속성1=값1, ...
        # WHERE 조건절
        c.execute('UPDATE tasks SET todo_content=?, todo_date=?, todo_time=?,'
                  ' completed=? WHERE id=?', values)
        TodoDB.con.commit()

    def updateTaskState(self, args):
        c = TodoDB.con.cursor()
        c.execute('UPDATE tasks SET completed=? WHERE id=?', (args[1], args[0]))
        TodoDB.con.commit()

    def updateTodoContent(self, args):
        c = TodoDB.con.cursor()
        c.execute('UPDATE tasks SET todo_content=? WHERE id=?', (args[1], args[0]))
        TodoDB.con.commit()

    def updateTodoDate(self, args):
        c = TodoDB.con.cursor()
        c.execute('UPDATE tasks SET todo_date=? WHERE id=?', (args[1], args[0]))
        TodoDB.con.commit()

    def updateTodoTime(self, args):
        c = TodoDB.con.cursor()
        c.execute('UPDATE tasks SET todo_time=? WHERE id=?', (args[1], args[0]))
        TodoDB.con.commit()

    def readUsers(self):
        c = TodoDB.con.cursor()
        c.execute('SELECT * FROM users')
        res = c.fetchall()
        return res

    # 회원 검색
    def findUserByName(self, name):
        c = TodoDB.con.cursor()
        c.execute(f"SELECT * FROM users WHERE user_name LIKE '%{name}%'")
        res = c.fetchall()
        return res

    def insertUser(self, values):
        c = TodoDB.con.cursor()
        c.execute('INSERT INTO users (user_name, user_gender, '
                  'user_id, user_pw, '
                  'user_email, user_mobile, reg_date)'
                  ' VALUES (?, ?, ?, ?, ?, ?, ?)', values)
        TodoDB.con.commit()
        return c.lastrowid

    def deleteUser(self, id):
        c = TodoDB.con.cursor()
        c.execute(f'DELETE FROM users WHERE id={id}')
        TodoDB.con.commit()

    def updateUser(db, values):
        c = TodoDB.con.cursor()
        c.execute('UPDATE users SET user_name=?, user_gender=?, user_pw=?,'
                  'user_email=?, user_mobile=? WHERE id=?', values)
        TodoDB.con.commit()