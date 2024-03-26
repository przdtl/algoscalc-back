INSERT INTO calculations (title, name, description)
VALUES ('N-е число Фибоначчи', 'fibonacci', 'Числа Фибоначчи - последовательность чисел, каждый член которой равен сумме двух предыдущих.
Введите порядковый номер числа Фибоначчи и калькулятор выдаст вам соответствующее значение.'),
       ('Числа Фибоначчи', 'fibonacci_list', 'Числа Фибоначчи - последовательность чисел, каждый член которой равен сумме двух предыдущих.
Введите n-ый член, для которого надо сформировать ряд Фибоначчи, и калькулятор выдаст вам последовательность до n-го члена.'),
       ('Расход топлива для поездки на заданное расстояние', 'fuel_consumption',
        'Калькулятор расхода топлива поможет рассчитать количество и стоимость топлива для поездки на заданное расстояние'),
       ('Вычитание матриц', 'matrix_sub', 'Вычитание матриц'),
       ('Проверка ряда чисел на совершенность', 'perfect_numbers', 'Совершенное число - число, равное сумме своих собственных делителей (то есть всех своих положительных делителей, отличных от самого числа).
Введите ряд чисел через запятую для проверки наличия совершенных чисел.
Пример: 4,5,28,496,6789,5235906'),
       ('Корни квадратного уравнения', 'quadratic_equation', 'Нахождение корней квадратного уравнения'),
       ('Количество подстрок в строке', 'substring_in_a_string', 'Вывод количества подстрок в одной строке');


INSERT INTO parameters (calculation_id, name, title, description, data_type, data_shape)
VALUES ((SELECT id FROM calculations WHERE name = 'fibonacci'),
        'n', 'Номер числа Фибоначчи', 'Введите целое положительное число', 'INT', 'SCALAR'),
       ((SELECT id FROM calculations WHERE name = 'fibonacci_list'),
        'n', 'Длина последовательности', 'Введите целое положительное число', 'INT', 'SCALAR'),
       ((SELECT id FROM calculations WHERE name = 'fuel_consumption'),
        'distance', 'Сколько хотите проехать', 'Введите неотрицательное вещественное число', 'FLOAT', 'SCALAR'),
       ((SELECT id FROM calculations WHERE name = 'fuel_consumption'),
        'mean_consumption', 'Средний расход топлива (л/100км)', 'Введите неотрицательное вещественное число', 'FLOAT',
        'SCALAR'),
       ((SELECT id FROM calculations WHERE name = 'fuel_consumption'),
        'price', 'Стоимость 1 л. топлива (руб)', 'Введите неотрицательное вещественное число', 'FLOAT', 'SCALAR'),
       ((SELECT id FROM calculations WHERE name = 'fuel_consumption'),
        'need_round', 'Округлять результат', 'При проставлении отметки объем и стоимость будут округлены до целого',
        'BOOL', 'SCALAR'),
       ((SELECT id FROM calculations WHERE name = 'matrix_sub'),
        'n', 'Матрица', 'Введите значения в матрицу', 'FLOAT', 'MATRIX'),
       ((SELECT id FROM calculations WHERE name = 'matrix_sub'),
        'm', 'Матрица', 'Введите значения в матрицу', 'FLOAT', 'MATRIX'),
       ((SELECT id FROM calculations WHERE name = 'perfect_numbers'),
        'numbers', 'Ряд чисел для проверки на совершенность', 'Введите ряд целых чисел через запятую', 'INT', 'LIST'),
       ((SELECT id FROM calculations WHERE name = 'quadratic_equation'),
        'a', 'Коэффициент a', 'Введите любое вещественное число кроме 0', 'FLOAT', 'SCALAR'),
       ((SELECT id FROM calculations WHERE name = 'quadratic_equation'),
        'b', 'Коэффициент b', 'Введите любое вещественное число', 'FLOAT', 'SCALAR'),
       ((SELECT id FROM calculations WHERE name = 'quadratic_equation'),
        'c', 'Коэффициент c', 'Введите любое вещественное число', 'FLOAT', 'SCALAR'),
       ((SELECT id FROM calculations WHERE name = 'substring_in_a_string'),
        'text', 'Исходный текст', 'Введите, пожалуйства, исходный текст', 'STRING', 'SCALAR'),
       ((SELECT id FROM calculations WHERE name = 'substring_in_a_string'), 'findtext', 'Строка для поиска',
        'Введите, пожалуйства, строку, которую нужно найти', 'STRING', 'SCALAR');

INSERT INTO outputs (calculation_id, name, title, description, data_type, data_shape)
VALUES ((SELECT id FROM calculations WHERE name = 'fibonacci'),
        'result', 'Число Фибоначчи', 'Число Фибоначчи с номером n', 'INT', 'SCALAR'),
       ((SELECT id FROM calculations WHERE name = 'fibonacci_list'),
        'result', 'Последовательность чисел Фибоначчи', 'Список чисел Фибоначчи от 1-го до n-го', 'INT', 'LIST'),
       ((SELECT id FROM calculations WHERE name = 'fuel_consumption'),
        'volume', 'Потребуется топлива (л)', 'Объем топлива в литрах', 'FLOAT', 'SCALAR'),
       ((SELECT id FROM calculations WHERE name = 'fuel_consumption'),
        'cost', 'Стоимость топлива (руб)', 'Стоимость топлива в рублях', 'FLOAT', 'SCALAR'),
       ((SELECT id FROM calculations WHERE name = 'matrix_sub'),
        'result', 'Матрица', 'Матрица, полученная в процессе вычитания', 'FLOAT', 'MATRIX'),
       ((SELECT id FROM calculations WHERE name = 'perfect_numbers'),
        'has_perfect', 'Проверка наличия совершенных чисел', 'Указывает есть ли в исходном списке совершенные числа',
        'BOOL', 'SCALAR'),
       ((SELECT id FROM calculations WHERE name = 'perfect_numbers'),
        'perfect_numbers', 'Совершенные числа', 'Список совершенных чисел', 'INT', 'LIST'),
       ((SELECT id FROM calculations WHERE name = 'quadratic_equation'),
        'roots', 'Корни уравнения', 'Значения корней или сообщение, что корней нет', 'STRING', 'SCALAR'),
       ((SELECT id FROM calculations WHERE name = 'substring_in_a_string'),
        'num_count', 'Количество подстрок', 'Количество всех подстрок строки', 'INT', 'SCALAR');