from settings import settings
import mariadb

conn_params = {
  "user" : settings.mariadb_user,
  "password" : settings.mariadb_password,
  "host" : settings.mariadb_host,
  "database" : settings.mariadb_database,
  "port" : settings.mariadb_port
}



def getConn():
  try:
    conn = mariadb.connect(**conn_params)
    if conn == None:
      return None
    return conn
  except mariadb.Error as e:
    print(f"접속 오류 : {e}")
    return None

def findOne(sql, params=None): # ← params 인자를 추가해서 2개를 받을 수 있게 합니다.
    result = None
    conn = None
    try:
        conn = getConn()
        if conn:
            cur = conn.cursor()
            # 파라미터가 있으면 함께 실행, 없으면 쿼리만 실행
            if params:
                cur.execute(sql, params)
            else:
                cur.execute(sql)
            
            row = cur.fetchone()
            
            if row:
                # 결과 컬럼명 매핑
                columns = [desc[0] for desc in cur.description]
                result = dict(zip(columns, row))
            
            cur.close()
    except mariadb.Error as e:
        print(f"MariaDB Error : {e}")
    finally:
        if conn:
            conn.close()
    return result

def findAll(sql, params=None):
  result = []
  try:
    conn = getConn()
    if conn:
      cur = conn.cursor()
      cur.execute(sql, params or ())
      rows = cur.fetchall()
      columns = [desc[0] for desc in cur.description]
      cur.close()
      conn.close()
      result = [dict(zip(columns, row)) for row in rows]
  except mariadb.Error as e:
    print(f"MariaDB Error : {e}")
  return result

def save(sql, params=None):
  result = False
  try:
    conn = getConn()
    if conn:
      cur = conn.cursor()
      cur.execute(sql, params or ())
      conn.commit()
      cur.close()
      conn.close()
      result = True
  except mariadb.Error as e:
    print(f"MariaDB Error : {e}")
  return result

def add_key(sql):
  result = [False, 0]
  try:
    conn = getConn()
    if conn:
      cur = conn.cursor()
      cur.execute(sql)
      sql2 = "SELECT LAST_INSERT_ID() as no"
      cur.execute(sql2)
      row = cur.fetchone()
      columns = [desc[0] for desc in cur.description]
      data = dict(zip(columns, row)) if row else None      
      conn.commit()
      cur.close()
      conn.close()
      result[0] = True
      if data:
        result[1] = data["no"]
  except mariadb.Error as e:
    print(f"MariaDB Error : {e}")
  return result