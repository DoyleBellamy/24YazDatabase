# TODO İki tane olan get_data kodu teke düsürülebilir

import streamlit as st
import mysql.connector
import pandas as pd
import re
import config as c
from mysql.connector import Error

#Giriş bilgileri
'''db_config = {
    'user': 'root',
    'password': 'umut',
    'host': '127.0.0.1',
    'database': 'bil372_project',
}'''

def format_time(time_str):
    """Saat formatını düzenler (09.00 -> 9, 17.00 -> 17)."""
    try:
        return int(time_str.split('.')[0])  # Saat kısmını integer'a çevir
    except ValueError:
        return time_str  # Eğer format doğru değilse orijinal değeri döndür


# MySQL bağlantısı oluştur
def create_connection():
    return mysql.connector.connect(**c.Config.db_config)

# MySQL veritabanından veri almak için fonksiyon
# TODO Bu get_data versiyonu silinecek 
def get_data(query):
    conn = create_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def update_data(query, params):
    """
    Veri tabanında güncelleme yapar.
    
    Args:
        query (str): Güncelleme sorgusu. Sorguda %s yer tutucuları kullanılabilir.
        params (tuple): Sorguda yer tutucular için değerler.
    """
    conn = create_connection()
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()  # Değişiklikleri kaydeder
        print(f"{cursor.rowcount} kayıt güncellendi.")
    except Error as e:
        print(f"Bir hata oluştu: {e}")
        conn.rollback()  # Hata durumunda geri alır
    finally:
        cursor.close()
        conn.close()


def insert_data(query, params):
    """
    Veri tabanına yeni bir satır ekler.
    
    Args:
        query (str): Ekleme sorgusu. Sorguda %s yer tutucuları kullanılabilir.
        params (tuple): Sorguda yer tutucular için değerler.
    """
    conn = create_connection()
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()  # Değişiklikleri kaydeder
        print(f"Yeni satır eklendi, ID: {cursor.lastrowid}")
    except Error as e:
        print(f"Bir hata oluştu: {e}")
        conn.rollback()  # Hata durumunda geri alır
    finally:
        cursor.close()
        conn.close()


def get_highest_id(table_name, id_ismi):
    """
    Belirtilen tabloda en yüksek ID değerini getirir.
    
    Args:
        table_name (str): Üzerinde sorgulama yapılacak tablo adı.
    
    Returns:
        int: En yüksek ID değeri. Eğer hata oluşursa veya tablo boşsa None döner.
    """
    conn = create_connection()
    if conn is None:
        return None

    try:
        cursor = conn.cursor()
        query = f"SELECT MAX({id_ismi}) FROM {table_name}"
        cursor.execute(query)
        result = cursor.fetchone()
        highest_id = result[0] if result[0] is not None else None
        return highest_id
    except Error as e:
        print(f"Bir hata oluştu: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

# Veritabanından veri çekme fonksiyonu
def get_data(query, params=None):
    conn = create_connection()
    if conn is None:
        return None
    try:
        df = pd.read_sql(query, conn, params=params)
        return df
    except Error as e:
        st.error(f"Bir hata oluştu: {e}")
        return None
    finally:
        conn.close()