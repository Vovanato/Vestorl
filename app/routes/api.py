from flask import Blueprint, jsonify,request,session
from werkzeug.security import generate_password_hash,check_password_hash
from app.database import get_db_connection
from app.storage import upload_file,delete_file
vbp = Blueprint('api', __name__, url_prefix = '/vbp')

@vbp.route('/hello', methods = ['GET'])
def hello_vbp ():
    return jsonify({"status": "ok", "message": "Привіт,це API"})
@vbp.route('/register', methods=['POST'])

def upe():

    input_data = request.get_json()

    user_email = input_data.get('email')
    user_name =  input_data.get('username')
    user_pass = input_data.get('password')


    if not user_email or not user_name or not user_pass:
        return jsonify({"eror": "Всі поля обов'язкові"}),400

    hashed_pass = generate_password_hash(user_pass)
    
    try:
        conn=get_db_connection()
        cursor=conn.cursor()
        query="INSERT INTO users(email,username,password_hash) VALUES (%s, %s, %s)"
        cursor.execute(query,(user_email,user_name,hashed_pass))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message":"Користувач створений"}), 201
    except Exception as e:
        return jsonify({"error":str(e)}),500
@vbp.route('/login',methods=['POST'])    
def user_login():
    input_data=request.get_json()
    user_email = input_data.get('email')
    user_pass = input_data.get('password')
    if not user_email or not user_pass:
        return jsonify({"eror":"Всі поля обов'язкові"}), 400
    try:
        conn=get_db_connection()
        cursor=conn.cursor()
        query="SELECT id, password_hash FROM users Where email = %s"
        cursor.execute(query,(user_email,))
        user_data=cursor.fetchone()
        cursor.close()
        conn.close()
        if user_data is None:
            return jsonify({"error":"Користувача не знайдено"}),401
        if check_password_hash(user_data[1],user_pass) is True:
            session['user_id'] = user_data[0]
            return jsonify({"message": "Вхід успішний!"}), 200
        else:
            return jsonify({"error":"Пароль невірний"}),401
    except Exception as e:
        return jsonify({"error":str(e)}),500

@vbp.route('/upload',methods=['POST'])
@vbp.route('/upload', methods=['POST'])
def upload_users_files():
    if 'user_id' not in session:
        return jsonify({'error': 'Ви не увійшли в систему'}), 401
    
    user_id = session['user_id']

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
        
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'drop filename'}), 400

    file_url, new_name = upload_file(file, file.filename)
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "INSERT INTO files (user_id,filename,storage_name,file_url) VALUES (%s,%s,%s,%s)"
        cursor.execute(query, (user_id, file.filename, new_name, file_url))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'filename': 'Файли завантажені в хмару'}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@vbp.route('/files',methods=['GET'])
def get_user_files():
    if 'user_id' not in session:
        return jsonify({'error': 'Ви не увійшли в систему'}), 401
    user_id = session['user_id']
    conn=get_db_connection()
    cursor=conn.cursor(dictionary=True)
    query="SELECT * FROM files WHERE user_id= %s"
    cursor.execute(query,(user_id,))
    files_list=cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(files_list)
@vbp.route('/files', methods=['DELETE'])
@vbp.route('/files', methods=['DELETE'])
def delete_user_file():
    if 'user_id' not in session:
        return jsonify({'error': 'Ви не увійшли в систему'}), 401
    user_id = session['user_id']

    file_id = request.args.get('file_id')

    if not file_id:
        return jsonify({'error': 'Не вказано ID файлу'}), 400
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT * FROM files WHERE id = %s AND user_id = %s"
        cursor.execute(query, (file_id, user_id))
        result = cursor.fetchone()
        
        if result is None:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Файл не знайдено або у вас немає прав'}), 404

        filename_in_cloud = result['storage_name']
        delete_file(filename_in_cloud)  
        
        query1 = "DELETE FROM files WHERE id = %s"
        cursor.execute(query1, (file_id,))
        conn.commit()
        
        cursor.close()
        conn.close()
        return jsonify({'message': 'Файл успішно видалено'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
@vbp.route('/logout', methods=['POST']) 
def logout():
    session.clear()
    return jsonify({"message": "Ви успішно вийшли"})


    
