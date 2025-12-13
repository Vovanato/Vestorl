import inquirer
import requests
import json
import sys
import time

# Імпорт усіх моделей (переконайтеся, що models_ar.py та models_dao.py оновлені!)
try:
    from models_ar import ClientAR, DilerAR, AvtoAR, CitiesAR, DogovoryAR
    from models_dao import ClientDAO, ClientDTO, DilerDAO, DilerDTO, AvtoDAO, AvtoDTO, CitiesDAO, CitiesDTO, DogovoryDAO, DogovoryDTO
except ImportError:
    print("!! ПОМИЛКА: Не знайдено файли 'models_ar.py' або 'models_dao.py'.")
    sys.exit()

API_URL_BASE = "http://127.0.0.1:5000"

CURRENT_DB_CONFIG = {
    'user': 'root',
    'password': 'MyNewP@ssw0rd2025!',
    'host': 'localhost',
    'port': 3306,
    'database': 'Комісійний автомагазин',
    'raise_on_warnings': True,
    'charset': 'utf8mb4'
}

# --- ДОПОМІЖНІ ФУНКЦІЇ ВВОДУ ---

def set_server_db_mode(mode):
    try:
        requests.post(f"{API_URL_BASE}/switch_db", json={'mode': mode})
    except:
        print("\n[Error] Сервер app.py не відповідає.")

def get_person_input(entity_name="Клієнта"):
    print(f"--- Введення даних {entity_name} ---")
    return {
        'first_name': input("Ім'я: "),
        'last_name': input("Прізвище: "),
        'city_id': input("ID міста (число): "),
        'address': input("Адреса: "),
        'phone': input("Телефон: ")
    }

def get_avto_input():
    print("--- Введення даних Авто ---")
    return {
        'marka_avto': input("Марка: "),
        'data_vypusku': input("Дата випуску (РРРР-ММ-ДД): "),
        'probih': input("Пробіг: ")
    }

def get_city_input():
    return {'city_name': input("Назва міста: ")}

# --- 1. РЕЖИМ REST API (Твій готовий код) ---
def run_rest_api_mode():
    print("\n=== РЕЖИМ REST API (SQL ЗАПИТИ) ===")
    while True:
        q = [inquirer.List('act', message="REST API Дія:", choices=['SELECT', 'INSERT', 'UPDATE', 'DELETE', '< НАЗАД'])]
        ans = inquirer.prompt(q)
        if not ans or ans['act'] == '< НАЗАД': break
        
        # ... (Весь твій код REST API з попередньої версії залишається тут) ...
        # ... (Для економії місця в цьому повідомленні я його скорочую, 
        # ...  але ти маєш залишити ту версію, де є цикл редагування UPDATE) ...
        
        # Для прикладу - спрощена версія, щоб файл був робочим:
        if ans['act'] == 'SELECT':
            tbl = input("Таблиця: ")
            try:
                resp = requests.post(f"{API_URL_BASE}/query", json={'query': f"SELECT * FROM {tbl}"})
                print(json.dumps(resp.json(), indent=2, ensure_ascii=False))
            except Exception as e: print(e)
        
        elif ans['act'] == 'INSERT':
            print("Використовуй меню AR/DAO для зручного додавання, або пиши SQL вручну тут.")
            tbl = input("Таблиця: ")
            col = input("Колонки: ")
            val = input("Значення: ")
            try: requests.post(f"{API_URL_BASE}/query", json={'query': f"INSERT INTO {tbl} ({col}) VALUES ({val})"})
            except: pass

        elif ans['act'] == 'UPDATE':
             # Встав сюди свій крутий код з циклом while True
             print("Запустіть повну версію для Editor Mode")

# --- 2. РЕЖИМ ACTIVE RECORD (ОНОВЛЕНИЙ) ---
def run_ar_mode():
    print("\n=== РЕЖИМ ACTIVE RECORD ===")
    
    # Вибір таблиці
    while True:
        tbl_q = [inquirer.List('table', message="З якою таблицею працюємо?", 
                               choices=['Klient', 'Diler', 'Avto', 'Cities', '< НАЗАД'])]
        tbl_ans = inquirer.prompt(tbl_q)
        if not tbl_ans or tbl_ans['table'] == '< НАЗАД': break
        
        entity_class = None
        if tbl_ans['table'] == 'Klient': entity_class = ClientAR
        elif tbl_ans['table'] == 'Diler': entity_class = DilerAR
        elif tbl_ans['table'] == 'Avto': entity_class = AvtoAR
        elif tbl_ans['table'] == 'Cities': entity_class = CitiesAR

        # Меню дій для вибраної таблиці
        while True:
            act_q = [inquirer.List('act', message=f"AR [{tbl_ans['table']}] Дія:", 
                                   choices=['Всі (All)', 'Знайти (Find)', 'Створити (Save)', 'Оновити (Update)', 'Видалити (Delete)', '< НАЗАД'])]
            act = inquirer.prompt(act_q)
            if not act or act['act'] == '< НАЗАД': break

            try:
                if act['act'] == 'Всі (All)':
                    items = entity_class.get_all(CURRENT_DB_CONFIG)
                    for i in items: print(i)

                elif act['act'] == 'Знайти (Find)':
                    uid = input("ID: ")
                    item = entity_class.find_by_id(CURRENT_DB_CONFIG, uid)
                    print(f"Знайдено: {item}" if item else "Не знайдено")

                elif act['act'] == 'Створити (Save)':
                    # Вибираємо правильний input залежно від таблиці
                    if entity_class == ClientAR: data = get_person_input("Клієнта")
                    elif entity_class == DilerAR: data = get_person_input("Дилера")
                    elif entity_class == AvtoAR: data = get_avto_input()
                    elif entity_class == CitiesAR: data = get_city_input()
                    
                    # Створюємо об'єкт (розпаковуємо словник data через **)
                    obj = entity_class(CURRENT_DB_CONFIG, **data)
                    obj.save()
                    print("✅ Збережено!")

                elif act['act'] == 'Оновити (Update)':
                    uid = input("ID для оновлення: ")
                    item = entity_class.find_by_id(CURRENT_DB_CONFIG, uid)
                    if item:
                        print(f"Поточні дані: {item}")
                        print("Введіть нові дані (натисніть Enter, щоб залишити старі):")
                        
                        # Проста логіка оновлення полів
                        for attr, val in item.__dict__.items():
                            if attr in ['id', 'db_config']: continue # Службові поля не чіпаємо
                            new_val = input(f"{attr} [{val}]: ")
                            if new_val:
                                setattr(item, attr, new_val) # Оновлюємо атрибут об'єкта
                        
                        item.save() # Зберігаємо зміни
                        print("✅ Оновлено!")
                    else:
                        print("❌ Не знайдено")

                elif act['act'] == 'Видалити (Delete)':
                    uid = input("ID для видалення: ")
                    item = entity_class.find_by_id(CURRENT_DB_CONFIG, uid)
                    if item:
                        item.delete()
                        print("✅ Видалено!")
                    else:
                        print("❌ Не знайдено")

            except Exception as e:
                print(f"Помилка AR: {e}")

# --- 3. РЕЖИМ DAO (ОНОВЛЕНИЙ) ---
def run_dao_mode():
    print("\n=== РЕЖИМ DAO ===")
    
    while True:
        tbl_q = [inquirer.List('table', message="З якою таблицею працюємо?", 
                               choices=['Klient', 'Diler', 'Avto', 'Cities', '< НАЗАД'])]
        tbl_ans = inquirer.prompt(tbl_q)
        if not tbl_ans or tbl_ans['table'] == '< НАЗАД': break
        
        # Ініціалізуємо відповідний DAO і клас DTO
        dao = None
        dto_class = None
        
        if tbl_ans['table'] == 'Klient': 
            dao = ClientDAO(CURRENT_DB_CONFIG)
            dto_class = ClientDTO
        elif tbl_ans['table'] == 'Diler':
            dao = DilerDAO(CURRENT_DB_CONFIG)
            dto_class = DilerDTO
        elif tbl_ans['table'] == 'Avto':
            dao = AvtoDAO(CURRENT_DB_CONFIG)
            dto_class = AvtoDTO
        elif tbl_ans['table'] == 'Cities':
            dao = CitiesDAO(CURRENT_DB_CONFIG)
            dto_class = CitiesDTO

        while True:
            act_q = [inquirer.List('act', message=f"DAO [{tbl_ans['table']}] Дія:", 
                                   choices=['Всі', 'Знайти', 'Створити', 'Оновити', 'Видалити', '< НАЗАД'])]
            act = inquirer.prompt(act_q)
            if not act or act['act'] == '< НАЗАД': break

            try:
                if act['act'] == 'Всі':
                    items = dao.read_all()
                    for i in items: print(i)

                elif act['act'] == 'Знайти':
                    uid = input("ID: ")
                    item = dao.read_by_id(uid)
                    print(f"Знайдено: {item}" if item else "Не знайдено")

                elif act['act'] == 'Створити':
                    if dto_class == ClientDTO: data = get_person_input("Клієнта")
                    elif dto_class == DilerDTO: data = get_person_input("Дилера")
                    elif dto_class == AvtoDTO: data = get_avto_input()
                    elif dto_class == CitiesDTO: data = get_city_input()
                    
                    dto = dto_class(**data)
                    dao.create(dto)
                    print("✅ Створено!")

                elif act['act'] == 'Оновити':
                    uid = input("ID для оновлення: ")
                    dto = dao.read_by_id(uid)
                    if dto:
                        print(f"Поточні дані: {dto}")
                        # Цикл по атрибутах DTO
                        for attr, val in dto.__dict__.items():
                            if attr == 'id': continue
                            new_val = input(f"{attr} [{val}]: ")
                            if new_val:
                                setattr(dto, attr, new_val)
                        dao.update(dto)
                        print("✅ Оновлено!")
                    else:
                        print("❌ Не знайдено")

                elif act['act'] == 'Видалити':
                    uid = input("ID для видалення: ")
                    dao.delete(uid)
                    print("✅ Видалено!")

            except Exception as e:
                print(f"Помилка DAO: {e}")

# --- ГОЛОВНЕ МЕНЮ ---
def main():
    global CURRENT_DB_CONFIG
    print("--- СИСТЕМА КЕРУВАННЯ БАЗОЮ ДАНИХ (Lab 8-9 Ultimate) ---")

    # Вибір бази
    q_db = [inquirer.List('db', message="База Даних:", choices=['Local (3306)', 'Docker (3307)', 'Exit'])]
    ans_db = inquirer.prompt(q_db)
    
    if not ans_db or ans_db['db'] == 'Exit': sys.exit()
    
    if ans_db['db'] == 'Docker (3307)':
        CURRENT_DB_CONFIG['port'] = 3307
        CURRENT_DB_CONFIG['database'] = 'car_shop'
        set_server_db_mode('docker')
    else:
        CURRENT_DB_CONFIG['port'] = 3306
        CURRENT_DB_CONFIG['database'] = 'Комісійний автомагазин'
        set_server_db_mode('local')

    # Вибір методу
    while True:
        q_method = [inquirer.List('method', message="Метод доступу:", 
                                  choices=['REST API (Lab 8)', 'Active Record (Lab 9)', 'DAO (Lab 9)', 'Exit'])]
        ans_method = inquirer.prompt(q_method)

        if not ans_method or ans_method['method'] == 'Exit': break
        
        if ans_method['method'].startswith('REST API'):
            run_rest_api_mode()
        elif ans_method['method'].startswith('Active Record'):
            run_ar_mode()
        elif ans_method['method'].startswith('DAO'):
            run_dao_mode()

if __name__ == "__main__":
    main()  