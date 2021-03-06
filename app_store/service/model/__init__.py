import pymysql as sql
import pickle
from xgboost import XGBClassifier
import numpy as np

def insertBbsData( data ):
    db_session   = None
    affected_row = 0 # 영향을 받은 로의 수
    try:    
        db_session = sql.connect( host='localhost',
                                user='root',
                                password='12341234',
                                db='local_db',
                                charset='utf8',
                                cursorclass=sql.cursors.DictCursor)
        
        with db_session.cursor() as cursor:
            sql_str = '''
                insert into tbl_contact
                (name, `email`, phone, message)
                values
                (%s,%s,%s,%s);
            '''
            cursor.execute( sql_str,
              (
                  data.get('name'),
                  data.get('email'),
                  data.get('phone'),
                  data.get('message')
              ) )
        # 실제 반영 => commit()
        db_session.commit()
        affected_row = db_session.affected_rows()
    except Exception as e:
        print( e )
    finally:    
        if db_session:
            db_session.close()            
    # 영향을 받은 로의 수를 반환
    return affected_row
def searchInPlaystore(info):
    db_session   = None
    rows = None # 영향을 받은 로의 수
    try:    
        db_session = sql.connect( host='localhost',
                                user='root',
                                password='12341234',
                                db='local_db',
                                charset='utf8',
                                cursorclass=sql.cursors.DictCursor)
        
        with db_session.cursor() as cursor:
            sql_str = '''
                select Rating, App, `Type`, Category, `Content Rating`
                from tbl_playstore
                where Rating >= %s and `Type` = %s and `Category` = %s and `Content Rating` = %s;
            '''
            cursor.execute( sql_str, (info.get('points'), info.get('type'), info.get('category'), info.get('rating')))
            rows = cursor.fetchall()
            
    except Exception as e:
        print( e )
    finally:
        if db_session:
            db_session.close()
            print('디비접속해제성공')
        return rows

def RatingPredictionModel(data):
    with open('service/model/model7.dat', 'rb') as fp:
        model = pickle.load(fp)
    
    y2_pred = model.predict(data)

    for r in y2_pred:
        print(r)
    return y2_pred

def searchInAppstore(info):
    db_session   = None
    rows = None # 영향을 받은 로의 수
    try:    
        db_session = sql.connect( host='localhost',
                                user='root',
                                password='12341234',
                                db='local_db',
                                charset='utf8',
                                cursorclass=sql.cursors.DictCursor)
        
        with db_session.cursor() as cursor:
            sql_str = '''
                select track_name, price, user_rating, prime_genre, cont_rating
                from tbl_appstore
                where price <= %s and user_rating >= %s and prime_genre = %s and cont_rating = %s;
            '''
            cursor.execute( sql_str, (info.get('type'), info.get('points'), info.get('category'),info.get('rating')))
            rows = cursor.fetchall()
            
    except Exception as e:
        print( e )
    finally:
        if db_session:
            db_session.close()
            print('디비접속해제성공')
        return rows

