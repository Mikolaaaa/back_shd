import psycopg2
import pandas as pd
import matplotlib
from main_script_dir.filter import filter_shd
from main_script_dir.prognoz import prediction_linear_regression_shd
from main_script_dir.visual import vis_overload_realtime
from new_data_to_df_log import new_data_to_df_log
matplotlib.use('Agg')
from flask import Flask, jsonify, request
import json


app = Flask(__name__)

# Параметры подключения к PostgreSQL
db_params = {
    'host': '172.16.20.236',
    'port': '5432',
    'database': 'shd',
    'user': 'postgres',
    'password': 'example',
    'connect_timeout': 5
}

# Функция для выполнения SQL-запроса к PostgreSQL
def execute_query(query):
    while True:
        try:
            connection = psycopg2.connect(**db_params)
            cursor = connection.cursor()

            cursor.execute(query)

            # Получение метаданных о столбцах
            column_names = [desc[0] for desc in cursor.description]

            # Если запрос начинается с SELECT, получаем результат
            if query.strip().lower().startswith('select'):
                result = cursor.fetchall()
            else:
                result = None

            connection.commit()

            cursor.close()
            connection.close()

            # Возвращаем результат и названия столбцов
            return result, column_names


        except psycopg2.OperationalError as e:
            print(f"Ошибка при выполнении запроса: {e}")
            print("Повторная попытка подключения через 5 секунд...")

        except Exception as e:
            print(f"Произошла ошибка: {e}")
            return None


result_shd, column_names_shd = execute_query('select * from shd_from_csv')

if result_shd is not None:
    df_shd = pd.DataFrame(result_shd, columns=column_names_shd)

result_level, column_names_level = execute_query('select * from level')
if result_level is not None:
    df_levels = pd.DataFrame(result_level, columns=column_names_level)


vars_dict_real = {
    'features_columns': ['time'],  # Список колонок признаков, включая время sigh
    'targets_columns': ['Capacity usage(%)'],  # Список колонок целевых признаков target
}
"""
print(11111)
print(df_shd)

print(22222)
print(df_levels)

df_filter_shd, df_filter_level, error1 = filter_shd(df_shd, df_levels, 'System') #param

print(33333)
print(df_filter_shd)
print(44444)
print(df_filter_level)

df_filter_shd_log, gui_dict1, error4 = new_data_to_df_log(df_filter_shd)

print(66666)
print(df_filter_shd_log)

predict_model, df_predict, error2 = prediction_linear_regression_shd(df_filter_shd, df_filter_level, vars_dict_real, False, 'auto_interval', {'find_global': False}, 'LEVEL0', )
                                                                                                                    # sp_flag, select_window_type, dropdown_block{}, levels_list, use_cloud

print(55555)
print(predict_model)
print(df_predict)

df_predict_log, gui_dict2, error5 = new_data_to_df_log(df_predict)

print(77777)
print(df_predict_log)

result, error3 = vis_overload_realtime(df_filter_shd_log, df_predict_log, df_filter_level)

print(result)"""


@app.route('/api/data')
def get_data():
    data = {'message': 'Hello from Flask API!'}
    return jsonify(data)

"""@app.route('/api/get_graph', methods=['POST'])
def get_graph():
    try:
        # Получаем данные из запроса
        data = request.json
        print(data)

        # Ваши данные из запроса
        param = data.get('param')
        sigh = data.get('sigh')
        sigh_param = data.get('target')
        storage_pool_flag = data.get('sp_flag')
        window_type = data.get('select_window_type')
        dropdown_block = data.get('dropdown_block', {})
        find_global = dropdown_block.get('find_global')
        interval = dropdown_block.get('interval')
        interval_num = dropdown_block.get('interval_num')
        levels_list = data.get('levels_list')
        use_cloud = data.get('use_cloud')

        # Здесь обрабатывайте данные и выполняйте необходимые действия

        # Пример ответа
        response_data = {
            'message': 'Success',
            # Данные, которые вы хотите вернуть
            # Например, какие-то данные для клиента
        }

        return jsonify(response_data), 200

    except Exception as e:
        # Если возникает ошибка, возвращаем ошибку сервера
        return jsonify({'error': str(e)}), 500"""


@app.route('/api/get_graph', methods=['POST'])
def get_shd_data():
    try:
        # Получаем данные из запроса
        data = request.json
        print(data)

        # Извлекаем необходимые параметры из данных
        param_val = data.get('param')
        param = param_val[0].get('key')
        param = str(param)
        sigh = data.get('sigh')
        sigh = str(sigh)
        target = data.get('target')
        target = str(target)
        sp_flag = data.get('sp_flag')
        select_window_type = data.get('select_window_type')
        select_window_type = str(select_window_type)
        if select_window_type == 'advanced_interval':
            dropdown_block = {'find_global': data.get('dropdown_block', {}).get('find_global'), 'interval': data.get('dropdown_block', {}).get('interval'), 'interval_num': data.get('dropdown_block', {}).get('interval_num')}
        else:
            dropdown_block = {'find_global': data.get('dropdown_block', {}).get('find_global')}

        print(dropdown_block)
        levels_list_val = data.get('levels_list')
        levels_list = levels_list_val[0].get('key')
        levels_list = levels_list.upper()
        levels_list = str(levels_list)
        use_cloud = data.get('use_cloud')

        vars_dict_real = {
            'features_columns': [sigh],  # Список колонок признаков, включая время sigh
            'targets_columns': [target],  # Список колонок целевых признаков target
        }

        df_filter_shd, df_filter_level, error1 = filter_shd(df_shd, df_levels, param)

        print(1)

        df_filter_shd_log, gui_dict1, error4 = new_data_to_df_log(df_filter_shd)

        print(2)

        predict_model, df_predict, error2 = prediction_linear_regression_shd(df_filter_shd, df_filter_level, vars_dict_real,
                                                                             sp_flag, select_window_type, dropdown_block,
                                                                             levels_list, use_cloud)

        print(3)

        df_predict_log, gui_dict2, error5 = new_data_to_df_log(df_predict)

        print(4)

        result, error3 = vis_overload_realtime(df_filter_shd_log, df_predict_log, df_filter_level)

        print(5)

        print(json.dumps(result))

        # Возвращаем отфильтрованные данные в формате JSON
        return json.dumps(result)
    except Exception as e:
        # Если возникает ошибка, возвращаем ошибку сервера
        print(Exception)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)