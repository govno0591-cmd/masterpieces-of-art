# Импортируем все необходимые библиотеки
import tkinter as tk
from tkinter import messagebox, ttk
import random
from PIL import Image, ImageTk, ImageDraw
import os
import time
import json
from datetime import datetime

# --- 1. ГЛОБАЛЬНЫЕ НАСТРОЙКИ И ПЕРЕМЕННЫЕ ИГРЫ ---

# 1.1. Инициализация главного окна
root = tk.Tk()
root.title("🎨 ШЕДЕВРЫ РУССКОГО ИСКУССТВА 🏛️")

# Центрирование и базовый размер
WIDTH = 1000
HEIGHT = 700
x = (root.winfo_screenwidth() // 2) - (WIDTH // 2)
y = (root.winfo_screenheight() // 2) - (HEIGHT // 2)
root.geometry(f'{WIDTH}x{HEIGHT}+{x}+{y}')

# 1.2. Переменные состояния игры
current_user = "Игрок"
difficulty = "легкий"
score = 0
question_number = 0
correct_answers = 0
start_time = 0
all_records = [] # Для хранения рекордов из records.txt
current_game_questions = [] # Список вопросов для текущей игры (перемешивается)
# Временная переменная для хранения выбранной темы до сохранения
temp_theme_setting = "classic" 

# 1.3. Настройки темы
settings = {"theme": "classic"}

themes = {
    "classic": {"bg": "#2C3E50", "header_bg": "#34495E", "card_bg": "#16A085", "text_color": "#ECF0F1", "accent": "#E74C3C", "button_bg": "#3498DB", "combo_bg": "#ECF0F1"},
    "dark": {"bg": "#1A1A1A", "header_bg": "#2D2D2D", "card_bg": "#404040", "text_color": "#FFFFFF", "accent": "#BB86FC", "button_bg": "#BB86FC", "combo_bg": "#FFFFFF"},
    "light": {"bg": "#F5F5F5", "header_bg": "#E0E0E0", "card_bg": "#FFFFFF", "text_color": "#212121", "accent": "#2196F3", "button_bg": "#2196F3", "combo_bg": "#FFFFFF"}
}

# --- 2. БАЗА ВОПРОСОВ (ВАША ОБЪЕДИНЕННАЯ) ---

questions_db = {
    "легкий": [
        {"image": "rublev_troitsa.jpg", "question": "Кто автор знаменитой иконы 'Троица'?", "options": ["Андрей Рублёв", "Феофан Грек", "Дионисий", "Симон Ушаков"], "correct": 0, "fact": "Андрей Рублёв - великий русский иконописец XV века"},
        {"image": "vasiliy_blajenniy.jpg", "question": "Как называется этот собор на Красной площади?", "options": ["Храм Василия Блаженного", "Успенский собор", "Архангельский собор", "Храм Христа Спасителя"], "correct": 0, "fact": "Построен в честь взятия Казани Иваном Грозным в XVI веке"},
        {"image": "uspensky_sobor.jpg", "question": "Главный собор Московского Кремля?", "options": ["Успенский собор", "Благовещенский собор", "Архангельский собор", "Колокольня Ивана Великого"], "correct": 0, "fact": "Успенский собор - место венчания на царство"},
        {"image": "sofia_novgorod.jpg", "question": "Самый древний сохранившийся каменный храм России?", "options": ["Софийский собор в Новгороде", "Софийский собор в Киеве", "Успенский собор во Владимире", "Дмитриевский собор"], "correct": 0, "fact": "Новгородский собор построен в 1045–1050 годах"},
        {"image": "andrey_icon.jpg", "question": "Кто написал 'Спас Нерукотворный' (традиционная икона)?", "options": ["Андрей Рублёв", "Феофан Грек", "Неизвестный мастер", "Дионисий"], "correct": 2, "fact": "Авторство многих древних икон неизвестно"},
        {"image": "novgorod_icon.jpg", "question": "К какому веку относится эта икона (по стилю)?", "options": ["XII век", "XIV век", "XVI век", "XVIII век"], "correct": 1, "fact": "XIV век - расцвет новгородской иконописи"},
        {"image": "golden_gates.jpg", "question": "Что изображено на картинке?", "options": ["Золотые ворота в Киеве", "Золотые ворота во Владимире", "Спасские ворота", "Троицкие ворота"], "correct": 0, "fact": "Золотые ворота в Киеве - памятник XI века"},
        {"image": "bogomater.jpg", "question": "Как называется этот тип иконы Богоматери?", "options": ["Одигитрия", "Умиление", "Оранта", "Знамение"], "correct": 0, "fact": "Одигитрия - один из основных типов икон Богородицы ('Путеводительница')"},
        {"image": "kremlin.jpg", "question": "Из какого города этот Кремль?", "options": ["Новгородский Кремль", "Московский Кремль", "Псковский Кремль", "Казанский Кремль"], "correct": 0, "fact": "Новгородский кремль - один из древнейших в России"},
        {"image": "", "question": "Что такое фреска?", "options": ["Роспись по сырой штукатурке", "Роспись по сухой штукатурке", "Роспись по дереву", "Роспись по металлу"], "correct": 0, "fact": "Фреска (от итал. 'fresco' — свежий) — техника росписи по сырой штукатурке"},
        {"image": "", "question": "Что такое нимб на иконах?", "options": ["Символ святости", "Украшение", "Подпись автора", "Дата создания"], "correct": 0, "fact": "Нимб - символ божественной благодати, света и святости"},
        {"image": "", "question": "Как называется верхняя часть храма в виде полусферы?", "options": ["Купол", "Шпиль", "Крыша", "Башня"], "correct": 0, "fact": "Купол символизирует небесный свод"},
        {"image": "", "question": "Из какого материала традиционно делали иконы?", "options": ["Дерево", "Камень", "Металл", "Стекло"], "correct": 0, "fact": "Иконы писали яичной темперой на деревянных досках (липа, сосна)"},
        {"image": "", "question": "Сколько куполов у храма Василия Блаженного (включая главку над колокольней)?", "options": ["9", "7", "5", "11"], "correct": 0, "fact": "У храма 9 основных куполов над предельными церквями и один над колокольней - всего 10 (часто считают 9 или 10)"},
        {"image": "", "question": "Что такое мозаика?", "options": ["Изображение из кусочков смальты", "Роспись красками", "Резьба по дереву", "Литье из металла"], "correct": 0, "fact": "Мозаика создается из маленьких кусочков смальты или камня"},
    ],
    "средний": [
        {"image": "trinity.jpg", "question": "В каком веке создана 'Троица' Рублёва?", "options": ["XIV век", "XV век", "XVI век", "XVII век"], "correct": 1, "fact": "Создана в XV веке (около 1411 или 1425-1427 годов)"},
        {"image": "", "question": "Характерные черты московской школы иконописи XV века?", "options": ["Утонченность линий", "Яркие контрасты", "Грубоватые формы", "Плоскостность"], "correct": 0, "fact": "Московская школа - гармония, утонченность линий и светлые тона"},
        {"image": "", "question": "Что символизирует красный цвет в иконописи?", "options": ["Мученичество", "Царствие Небесное", "Божественную мудрость", "Человеческую природу"], "correct": 0, "fact": "Красный - цвет мученичества, жертвенности и царской крови"},
        {"image": "fresco_style.jpg", "question": "В каком храме находятся фрески Феофана Грека?", "options": ["Церковь Спаса на Ильине (Новгород)", "Успенский собор", "Архангельский собор", "Благовещенский собор"], "correct": 0, "fact": "Феофан Грек расписал церковь Спаса на Ильине в Новгороде"},
        {"image": "", "question": "Что такое ковчег в иконе?", "options": ["Углубление на доске", "Оклад иконы", "Подпись автора", "Дата создания"], "correct": 0, "fact": "Ковчег - углубленное поле на иконной доске, окруженное плоским бортиком (полем)"},
        {"image": "", "question": "Что такое 'палатное письмо'?", "options": ["Изображение архитектуры", "Портретная живопись", "Пейзаж", "Натюрморт"], "correct": 0, "fact": "Палатное письмо - изображение архитектурных сооружений, часто в иконах или фресках"},
        {"image": "ancient_fresco.jpg", "question": "Где находятся фрески Дионисия?", "options": ["Ферапонтов монастырь", "Троице-Сергиева лавра", "Новодевичий монастырь", "Кирилло-Белозерский монастырь"], "correct": 0, "fact": "Фрески Дионисия в Соборе Рождества Богородицы Ферапонтова монастыря - объект наследия ЮНЕСКО"},
        {"image": "", "question": "Кто такой 'знаменщик'?", "options": ["Художник-рисовальщик", "Золотарь", "Резчик по дереву", "Переплетчик"], "correct": 0, "fact": "Знаменщик - художник, создающий оригинальный рисунок или 'знамя' для иконы"},
        {"image": "", "question": "Что такое 'закомара'?", "options": ["Полукруглое завершение стены", "Колонна", "Окно", "Дверь"], "correct": 0, "fact": "Закомара - полукруглое завершение внешней стены древнерусского храма, прикрывающее свод"},
        {"image": "", "question": "Кто, предположительно, расписывал Благовещенский собор Московского Кремля?", "options": ["Феофан Грек и Андрей Рублёв", "Дионисий", "Симон Ушаков", "Неизвестные мастера"], "correct": 0, "fact": "В росписях Благовещенского собора участвовали известные мастера во главе с Феофаном Греком и Андреем Рублёвым"},
        {"image": "", "question": "Что такое 'ассист'?", "options": ["Золотые линии на иконе", "Краска", "Кисть", "Лак"], "correct": 0, "fact": "Ассист - золотые штрихи и линии, обозначающие Божественный свет и сияние"},
        {"image": "", "question": "В каком веке построен Успенский собор во Владимире?", "options": ["XII век", "XIII век", "XIV век", "XV век"], "correct": 0, "fact": "Успенский собор во Владимире построен в XII веке (1158-1160 годы)"},
        {"image": "", "question": "Что такое 'лицевое шитьё'?", "options": ["Вышивка ликов святых", "Роспись по ткани", "Вязание", "Плетение"], "correct": 0, "fact": "Лицевое шитьё - вид древнерусского искусства, вышивка ликов и фигур святых золотыми и серебряными нитями"},
        {"image": "", "question": "Что такое 'псковский звон'?", "options": ["Особый стиль колокольного звона", "Архитектурный элемент", "Музыкальный инструмент", "Танцевальный ритм"], "correct": 0, "fact": "Псковский звон - особый стиль колокольного звона, отличающийся ритмической сложностью"},
        {"image": "", "question": "Чем отличается 'строгановская школа' иконописи?", "options": ["Миниатюрностью и изяществом", "Крупными формами", "Отсутствием позолоты", "Черно-белой гаммой"], "correct": 0, "fact": "Строгановская школа известна изяществом, миниатюрностью деталей и тонкостью письма (XVI-XVII вв.)"},
    ],
    "сложный": [
        {"image": "unknown_icon.jpg", "question": "Определите школу иконописи (по стилю, гармонии и духовной глубине):", "options": ["Московская", "Новгородская", "Псковская", "Владимирская"], "correct": 0, "fact": "Московская школа (после Рублёва) - гармония цветов и духовная глубина"},
        {"image": "complex_style.jpg", "question": "Чем отличается псковская школа иконописи?", "options": ["Экспрессивностью и напряжением", "Утонченностью", "Яркостью красок", "Строгостью форм"], "correct": 0, "fact": "Псковская школа известна эмоциональной экспрессивностью, контрастами и 'суровым' стилем"},
        {"image": "", "question": "Что такое 'обратная перспектива' в иконописи?", "options": ["Особый способ изображения пространства", "Ошибка художника", "Современная техника", "Фотографический метод"], "correct": 0, "fact": "Обратная перспектива - особенность иконописи, где линии сходятся к зрителю (символическое пространство)"},
        {"image": "", "question": "Что такое 'санкирь'?", "options": ["Подмалевок для ликов", "Золотой фон", "Красная краска", "Защитный лак"], "correct": 0, "fact": "Санкирь - темный зеленовато-коричневый подмалевок, используемый для написания ликов"},
        {"image": "", "question": "Какая школа иконописи известна динамичными 'летящими' фигурами и яркими красками?", "options": ["Новгородская", "Московская", "Псковская", "Ярославская"], "correct": 0, "fact": "Новгородская школа отличается динамичными 'летящими' фигурами, подчеркивая движение и энергию"},
        {"image": "", "question": "В каком историческом периоде возник 'строгановский стиль'?", "options": ["XVI-XVII века", "XIV-XV века", "XII-XIII века", "XVIII-XIX века"], "correct": 0, "fact": "Строгановский стиль сложился в XVI-XVII веках благодаря заказам богатого рода Строгановых"},
        {"image": "", "question": "Что такое 'вохрение'?", "options": ["Моделировка объема", "Золочение", "Покрытие лаком", "Подготовка доски"], "correct": 0, "fact": "Вохрение - техника моделировки объема светлыми охрами поверх санкиря при написании ликов"},
        {"image": "architecture_master.jpg", "question": "Кто построил церковь Покрова на Нерли?", "options": ["Мастера Андрея Боголюбского", "Итальянские зодчие", "Византийские мастера", "Новгородские строители"], "correct": 0, "fact": "Церковь построена мастерами князя Андрея Боголюбского в 1165 году"},
        {"image": "", "question": "Что такое 'Деисусный чин'?", "options": ["Композиция с Христом и предстоящими святыми", "Один тип иконы", "Техника письма", "Размер иконы"], "correct": 0, "fact": "Деисусный чин - центральный ряд иконостаса с Христом Вседержителем и фигурами, молящимися за человечество (Богоматерь, Иоанн Креститель и т.д.)"},
        {"image": "", "question": "Что символизирует голубой цвет в иконописи?", "options": ["Небесную чистоту и истину", "Мученичество", "Царственность", "Земную природу"], "correct": 0, "fact": "Голубой (синий) цвет символизирует небесную чистоту, горний мир и истину"},
        {"image": "", "question": "В каком веке работал великий иконописец Дионисий?", "options": ["XV-XVI века", "XIII-XIV века", "XI-XII века", "XVII-XVIII века"], "correct": 0, "fact": "Дионисий работал в конце XV - начале XVI веков, продолжая традиции Рублёва"},
        {"image": "master_work.jpg", "question": "Какая икона считается эталоном московской школы иконописи?", "options": ["Троица Рублёва", "Богоматерь Владимирская", "Спас Златая влась", "Архангел Гавриил"], "correct": 0, "fact": "'Троица' Андрея Рублёва - вершина и эталон московской школы"},
        {"image": "", "question": "Что такое 'палехская миниатюра'?", "options": ["Лаковая роспись на папье-маше", "Вышивка", "Резьба по кости", "Керамика"], "correct": 0, "fact": "Палехская миниатюра - вид русского народного промысла, лаковая роспись на изделиях из папье-маше"},
        {"image": "", "question": "Что характерно для 'ярославской школы' иконописи (XVII век)?", "options": ["Народная яркость и декоративность", "Аристократизм", "Миниатюрность", "Монохромность"], "correct": 0, "fact": "Ярославская школа отличается живописностью, повествовательностью и народной яркостью"},
        {"image": "historical_masterpiece.jpg", "question": "Где хранится 'Спас Нерукотворный' Симона Ушакова?", "options": ["Третьяковская галерея", "Русский музей", "Эрмитаж", "Кремль"], "correct": 0, "fact": "'Спас Нерукотворный' (1658 г.) хранится в Третьяковской галерее"},
    ],
    "эксперт": [
        {"image": "ikona_symbol.jpg", "question": "Что в иконописи символизирует золотой цвет (фон и нимбы)?", "options": ["Святость и Божественный свет", "Богатство и царская власть", "Мудрость и знания", "Жизнь и природа"], "correct": 0, "fact": "Золотой в иконе - это не металл, а символ Вечности и нетварного (несотворенного) Света."},
        {"image": "larionov_uchitel.jpg", "question": "Михаил Ларионов и Наталья Гончарова основали это направление русского авангарда...", "options": ["Лучизм", "Супрематизм", "Аналитическое искусство", "Оптическое искусство"], "correct": 0, "fact": "Лучизм — это первая русская форма абстракционизма, где живопись изображает лучи, пересекающиеся в пространстве."},
        {"image": "filonov_analitika.jpg", "question": "Павел Филонов — лидер школы...", "options": ["Аналитического искусства", "Абстрактного экспрессионизма", "Ар-Нуво", "Интуитивизма"], "correct": 0, "fact": "Филонов проповедовал 'сделанность' и 'принцип органического роста' произведения, что легло в основу его 'аналитического искусства'."},
        {"image": "rozhdestvo_drevniy.jpg", "question": "Какое архитектурное сооружение является самым старым зданием Москвы?", "options": ["Спасский собор Андроникова монастыря", "Успенский собор Кремля", "Благовещенский собор", "Собор Василия Блаженного"], "correct": 0, "fact": "Собор XIV века пережил пожары и перестройки и до сих пор стоит."},
        {"image": "zhivopis_tempera.jpg", "question": "Какая техника была основной в древнерусской живописи (иконописи) до XVII века?", "options": ["Яичная темпера", "Масляная живопись", "Акварель", "Фреска"], "correct": 0, "fact": "Темпера на яичном желтке была наиболее стойкой и распространенной техникой."},
        {"image": "malevich_chas.jpg", "question": "В каком году Малевич впервые представил 'Чёрный квадрат'?", "options": ["1915", "1913", "1917", "1920"], "correct": 0, "fact": "Картина была впервые выставлена на 'Последней футуристической выставке картин '0,10'' в Петрограде."},
        {"image": "kustodiev_vremya.jpg", "question": "К какому художественному объединению принадлежал Борис Кустодиев?", "options": ["Мир искусства", "Бубновый валет", "Голубая роза", "Ослиный хвост"], "correct": 0, "fact": "Кустодиев присоединился к 'Миру искусства' в начале XX века."},
        {"image": "dionisiy_stil.jpg", "question": "Каким стилем отличается иконопись Дионисия (XV-XVI вв.)?", "options": ["Вытянутые, утонченные фигуры", "Приземистые, массивные фигуры", "Тёмная, драматичная цветовая гамма", "Реалистичность лиц"], "correct": 0, "fact": "Дионисий привнес в икону изящество, удлиненные пропорции и светлые тона."},
        {"image": "golubaya_roza.jpg", "question": "Группа 'Голубая роза' (1907) являлась направлением...", "options": ["Символизма", "Кубизма", "Футуризма", "Примитивизма"], "correct": 0, "fact": "Художники 'Голубой розы' создавали тонкие, меланхоличные произведения, наполненные символами."},
        {"image": "avangard_muzei.jpg", "question": "Какой музей в Москве специализируется на современном искусстве?", "options": ["Музей 'Гараж'", "Государственный исторический музей", "Политехнический музей", "Музей изобразительных искусств им. А.С. Пушкина"], "correct": 0, "fact": "Музей современного искусства 'Гараж' – один из крупнейших в России, посвященный развитию современного искусства."},
        {"image": "fedotov_skandal.jpg", "question": "Сюжет какой картины Федотова является сатирическим изображением жизни чиновничества?", "options": ["Сватовство майора", "Вдовушка", "Завтрак аристократа", "Анкор, ещё анкор!"], "correct": 0, "fact": "Картина 'Сватовство майора' высмеивает браки по расчету и социальное расслоение."},
        {"image": "savrasov_uchitel_kto.jpg", "question": "Кого из художников называли 'певцом русской тоски'?", "options": ["Исаак Левитан", "Алексей Саврасов", "Василий Поленов", "Иван Шишкин"], "correct": 0, "fact": "Левитан известен своими лирическими, часто грустными пейзажами."},
        {"image": "vrubel_demon.jpg", "question": "Какая главная тема прослеживается в творчестве Михаила Врубеля?", "options": ["Демонический цикл", "Царские портреты", "Бытовые сцены", "Средиземноморские пейзажи"], "correct": 0, "fact": "Врубель посвятил много лет 'Демоническому циклу', отражая свои философские и личные переживания."},
        {"image": "malevich_suprematizm.jpg", "question": "Супрематизм переводится как...", "options": ["Превосходство цвета", "Высшее искусство", "Абсолютная форма", "Чистое ощущение"], "correct": 0, "fact": "Название направления от латинского 'supremus' – высший, превосходный."},
        {"image": "repinskaya_shkola.jpg", "question": "Какой знаменитый русский художник был учителем Валентина Серова?", "options": ["Илья Репин", "Василий Перов", "Павел Чистяков", "Иван Крамской"], "correct": 0, "fact": "Серов был не просто учеником, но и членом семьи Репина, его творчество формировалось под влиянием мастера."},
    ]
}

# --- 3. ФУНКЦИИ УПРАВЛЕНИЯ ФАЙЛАМИ И ИЗОБРАЖЕНИЯМИ ---

def setup_ttk_style(theme):
    """Настраивает стили для ttk виджетов (Combobox)"""
    style = ttk.Style()
    style.theme_use('clam') 
    
    style.configure("TCombobox", 
                    fieldbackground=theme["combo_bg"],
                    background=theme["button_bg"],
                    foreground=theme["text_color"],
                    selectbackground=theme["accent"],
                    selectforeground="white")
    style.map('TCombobox', 
              fieldbackground=[('readonly', theme["combo_bg"])],
              background=[('readonly', theme["button_bg"])])


def apply_theme():
    """Применяет выбранную тему и стили ttk"""
    theme_name = settings["theme"]
    theme = themes[theme_name]
    root.configure(bg=theme["bg"])
    setup_ttk_style(theme) 
    
def show_question():
    """Показывает текущий вопрос"""
    # Полная очистка окна перед каждым вопросом
    for widget in root.winfo_children():
        widget.destroy()
        
    theme = themes[settings["theme"]]
    
    # ... дальше твой остальной код ...

def clear_window():
    """Очищает окно от всех виджетов"""
    for widget in root.winfo_children():
        widget.destroy()

# Заглушка для случая, когда картинка есть, но недоступна
def create_unavailable_image_placeholder(theme):
    size = (400, 300)
    try:
        from PIL import ImageFont
    except ImportError:
        ImageFont = None
        
    img = Image.new('RGB', size, theme["card_bg"])
    draw = ImageDraw.Draw(img)
    text = "ИЗОБРАЖЕНИЕ НЕДОСТУПНО"
    
    # Расчет положения текста
    try:
        font = ImageFont.truetype("Arial.ttf", 20) if ImageFont and os.path.exists("Arial.ttf") else ImageFont.load_default()
        bbox = draw.textbbox((0, 0), text, font=font)
        x_center = (size[0] - (bbox[2] - bbox[0])) // 2
        y_center = (size[1] - (bbox[3] - bbox[1])) // 2
        draw.text((x_center, y_center), text, fill=theme["text_color"], font=font)
    except:
        draw.text((100, 140), text, fill=theme["text_color"])
        
    return ImageTk.PhotoImage(img)


def load_image(image_name):
    """
    Загрузка картинки или создание заглушки.
    Если image_name пуст (""), возвращает None, 
    чтобы в show_question отобразилась стильная панель.
    """
    if not image_name:
        return None # Сигнал для show_question: показать стильную панель
        
    size = (400, 300)
    theme = themes[settings["theme"]]
    
    try:
        path = os.path.join("icons", image_name)
        if os.path.exists(path) and os.path.getsize(path) > 0:
            img = Image.open(path).resize(size, Image.LANCZOS)
            return ImageTk.PhotoImage(img)
    except Exception as e:
        pass
        
    # Если загрузка не удалась, создаем заглушку (для вопросов, требующих картинку)
    return create_unavailable_image_placeholder(theme)


# --- 4. ФУНКЦИИ СТАТИСТИКИ (РЕКОРДЫ) - ИСПРАВЛЕНО ДЛЯ БЕЗОПАСНОСТИ ---

def load_records():
    """Загружает рекорды из файла при запуске, максимально защищаясь от ошибок JSON."""
    global all_records
    all_records = [] # Начинаем с пустого списка
    
    if os.path.exists("records.txt"):
        try:
            with open("records.txt", "r", encoding="utf-8") as f:
                # Читаем содержимое, убирая лишние пробелы/переводы строки
                content = f.read().strip()
                
                if content:
                    # Если содержимое не пустое, пытаемся декодировать JSON
                    all_records = json.loads(content) 
                else:
                    # Файл пуст
                    print("Отладка: Файл records.txt пуст.")
                    all_records = []
                    
        except (json.JSONDecodeError, EOFError, Exception) as e:
            # Ловим все возможные ошибки чтения/декодирования
            print(f"Отладка: КРИТИЧЕСКАЯ ОШИБКА при чтении records.txt. Файл поврежден: {e}")
            all_records = []
            
    # Убедимся, что all_records - это список
    if not isinstance(all_records, list):
        print("Отладка: Загруженные данные не являются списком. Сброс.")
        all_records = []


def save_new_record():
    """Сохраняет текущий результат в файл records.txt"""
    global all_records
    
    if not current_game_questions:
        print("Отладка: Игра не была начата, сохранение пропущено.")
        return
        
    total_time = int(time.time() - start_time)
    
    new_record = {
        "user": current_user,
        "difficulty": difficulty.capitalize(),
        "score": score,
        "correct": correct_answers,
        # Нам нужно знать общее число вопросов для статистики
        "total_questions": len(current_game_questions), 
        "time": total_time,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    
    # Убедимся, что загружаем текущие рекорды перед добавлением
    load_records() 
    
    all_records.append(new_record)
    # Сортируем по счету, потом по времени (меньше - лучше)
    all_records.sort(key=lambda x: (x['score'], -x['time']), reverse=True)
    all_records = all_records[:10]
    
    try:
        with open("records.txt", "w", encoding="utf-8") as f:
            json.dump(all_records, f, ensure_ascii=False, indent=4)
        print("Отладка: Новый рекорд успешно сохранен в records.txt.")
    except Exception as e:
        messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить рекорды: {e}")
        print(f"Отладка: КРИТИЧЕСКАЯ ОШИБКА сохранения: {e}")


# --- 5. ФУНКЦИИ ИГРОВОГО ПРОЦЕССА ---

def start_game(lvl_key):
    """Начинает игру с выбранным уровнем"""
    global difficulty, score, question_number, correct_answers, start_time, current_game_questions
    difficulty = lvl_key
    score = 0
    question_number = 0
    correct_answers = 0
    start_time = time.time()
    
    questions_list = questions_db.get(difficulty, []).copy()
    if not questions_list:
           messagebox.showerror("Ошибка", "База вопросов для этого уровня пуста.")
           show_level_selection()
           return
           
    random.shuffle(questions_list)
    current_game_questions = questions_list
    
    show_question()

def show_question():
    """Показывает текущий вопрос — стабильная версия"""
    # 1. ПОЛНАЯ ОЧИСТКА ОКНА (Убирает дублирование картинок)
    for widget in root.winfo_children():
        widget.destroy()
    
    # 2. ПРОВЕРКА ОКОНЧАНИЯ ИГРЫ
    if question_number >= len(current_game_questions):
        show_results()
        return

    # 3. ПОЛУЧЕНИЕ ДАННЫХ
    theme = themes[settings["theme"]]
    data = current_game_questions[question_number]
    
    # --- ВЕРХНЯЯ ПАНЕЛЬ (Имя, Очки, Прогресс) ---
    header = tk.Frame(root, bg=theme["header_bg"])
    header.pack(fill='x', pady=10, padx=20)
    
    tk.Label(header, text=f"👤 {current_user} | 🎯 {difficulty.upper()}", 
             font=("Arial", 12, "bold"), bg=theme["header_bg"], fg=theme["text_color"]).pack(side='left', padx=10)
    
    tk.Label(header, text=f"🏆 ОЧКИ: {score} | 📊 {question_number+1}/{len(current_game_questions)}", 
             font=("Arial", 12, "bold"), bg=theme["header_bg"], fg='#f9b208').pack(side='right', padx=10)

    # --- ЗОНА ИЗОБРАЖЕНИЯ ---
    # Пытаемся загрузить картинку. Если файла нет — блок просто пропустится.
    photo = load_image(data["image"])
    
    if photo:
        img_lbl = tk.Label(root, image=photo, bg=theme["bg"])
        img_lbl.image = photo
        img_lbl.pack(pady=20)
    else:
        # Если картинки нет, просто делаем небольшой отступ
        tk.Frame(root, height=20, bg=theme["bg"]).pack()

    # --- ТЕКСТ ВОПРОСА ---
    tk.Label(root, text=data["question"], font=("Arial", 16, "bold"),
             bg=theme["bg"], fg=theme["text_color"], wraplength=700).pack(pady=15)

    # --- ВАРИАНТЫ ОТВЕТОВ ---
    options_frame = tk.Frame(root, bg=theme["bg"])
    options_frame.pack(pady=10)
    
    # ДАЛЬШЕ ИДЕТ ТВОЙ ЦИКЛ С КНОПКАМИ (ОСТАВЬ ЕГО КАК БЫЛО)
    options_with_indices = [(i, opt) for i, opt in enumerate(data["options"])]
    random.shuffle(options_with_indices)
    
    for original_idx, opt in options_with_indices:
        btn = tk.Button(
            options_frame, 
            text=opt, 
            font=("Arial", 12), 
            bg=theme["button_bg"], 
            fg='white',
            width=50, 
            height=2, 
            wraplength=400,
            command=lambda o_idx=original_idx, f=options_frame: check_answer(o_idx, f)
        )
        btn.pack(pady=5)

def check_answer(selected_idx, options_frame):
    """Проверяет ответ, обновляет счет и показывает результат"""
    global score, question_number, correct_answers
    
    for widget in options_frame.winfo_children():
        if isinstance(widget, tk.Button):
            widget.config(state=tk.DISABLED)

    data = current_game_questions[question_number]
    is_correct = (selected_idx == data["correct"])
    
    if is_correct:
        score += 10
        correct_answers += 1
        title = "✅ ПРАВИЛЬНО!"
        color = "#27ae60" # Зеленый
    else:
        title = "❌ ОШИБКА!"
        color = "#e74c3c" # Красный

    show_answer_result(title, color, data, is_correct)

def show_answer_result(title, color, data, is_correct):
    """Показывает всплывающее окно с фактом и переходом к следующему вопросу"""
    res_win = tk.Toplevel(root)
    res_win.title(title)
    res_win.geometry("500x380")
    res_win.configure(bg=color)
    res_win.transient(root)
    res_win.grab_set() 
    
    tk.Label(res_win, text=title, font=("Arial", 20, "bold"), bg=color, fg='white').pack(pady=20)
    
    if not is_correct:
        correct_text = data["options"][data["correct"]]
        tk.Label(res_win, text=f"Правильный ответ: {correct_text}", font=("Arial", 14), 
                 bg=color, fg='white', wraplength=450).pack(pady=5)

    tk.Label(res_win, text="📚 ФАКТ:", font=("Arial", 12, "bold"), bg=color, fg='white').pack(pady=(15, 5))
    tk.Label(res_win, text=data["fact"], font=("Arial", 11), bg=color, fg='white', wraplength=450, justify='center').pack(pady=10, padx=10)

    def go_next():
        global question_number
        question_number += 1
        res_win.grab_release() 
        res_win.destroy()
        show_question()

    tk.Button(res_win, text="ДАЛЕЕ →", font=("Arial", 12, "bold"), width=15, command=go_next).pack(pady=20)
    res_win.protocol("WM_DELETE_WINDOW", go_next) 

def show_results():
    """Показывает итоговые результаты и сохраняет рекорд"""
    clear_window()
    theme = themes[settings["theme"]]
    total_time = int(time.time() - start_time)
    
    save_new_record()
    
    tk.Label(root, text="🏆 ИГРА ЗАВЕРШЕНА 🏆", font=("Arial", 28, "bold"), 
             bg=theme["bg"], fg=theme["accent"]).pack(pady=30)
    
    res_frame = tk.Frame(root, bg=theme["card_bg"], padx=30, pady=30, bd=5, relief='raised')
    res_frame.pack(pady=20)
    
    data = [
        ("👤 Игрок:", current_user, theme["text_color"]),
        ("🎯 Уровень:", difficulty.capitalize(), theme["accent"]),
        ("💰 Итоговый счет:", str(score), "#f9b208"),
        ("✅ Правильных ответов:", f"{correct_answers}/{len(current_game_questions)}", "#27ae60"),
        ("⏱️ Общее время:", f"{total_time} сек.", theme["text_color"]),
    ]
    
    for i, (label_text, value, color) in enumerate(data):
        tk.Label(res_frame, text=label_text, font=("Arial", 16), bg=theme["card_bg"], fg=theme["text_color"], anchor='w').grid(row=i, column=0, sticky='w', padx=10, pady=5)
        tk.Label(res_frame, text=value, font=("Arial", 16, "bold"), bg=theme["card_bg"], fg=color, anchor='e').grid(row=i, column=1, sticky='e', padx=10, pady=5)

    tk.Button(root, text="🏠 В МЕНЮ", font=("Arial", 14, "bold"), bg="#3498db", 
              fg="white", width=20, command=show_main_menu).pack(pady=30)


# --- 6. ФУНКЦИИ МЕНЮ И УПРАВЛЕНИЯ ЭКРАНАМИ ---

def exit_game():
    """Корректное завершение работы приложения"""
    root.destroy()
    
def show_main_menu():
    """Главное меню"""
    clear_window()
    theme = themes[settings["theme"]]
    root.configure(bg=theme["bg"])
    
    main_frame = tk.Frame(root, bg=theme["bg"])
    main_frame.pack(expand=True, fill='both')
    
    header = tk.Frame(main_frame, bg=theme["header_bg"])
    header.pack(fill='x', pady=(50, 30))
    
    tk.Label(header, text="🎨 ШЕДЕВРЫ РУССКОГО ИСКУССТВА 🏛️", font=("Arial", 28, "bold"),
             bg=theme["header_bg"], fg=theme["accent"], pady=20).pack()
    
    center = tk.Frame(main_frame, bg=theme["bg"])
    center.pack(expand=True, pady=30)

    btns = [
        ("🎮 НАЧАТЬ ИГРУ", "#27ae60", show_login_screen),
        ("⚙️ НАСТРОЙКИ", "#3498db", show_settings),
        ("📊 СТАТИСТИКА", "#9b59b6", show_statistics),
        ("ℹ️ ОБ ИГРЕ", "#1abc9c", show_about),
    ]
    
    for text, color, cmd in btns:
        tk.Button(center, text=text, font=("Arial", 14, "bold"), bg=color, fg='white',
                  width=25, height=2, command=cmd).pack(pady=8)
    
    tk.Button(center, text="🚪 ВЫХОД", font=("Arial", 14, "bold"), bg="#e74c3c",
              fg='white', width=25, height=2, command=exit_game).pack(pady=8)

def show_login_screen():
    """Экран ввода имени пользователя"""
    clear_window()
    theme = themes[settings["theme"]]
    container = tk.Frame(root, bg=theme["bg"])
    container.pack(expand=True)
    
    tk.Label(container, text="👤 ВВЕДИТЕ ВАШЕ ИМЯ", font=("Arial", 24, "bold"),
             bg=theme["bg"], fg=theme["accent"]).pack(pady=30)

    name_entry = tk.Entry(container, font=("Arial", 18), width=25, justify='center')
    name_entry.pack(pady=20, ipady=10)
    name_entry.insert(0, current_user) 

    def save_name():
        global current_user
        name = name_entry.get().strip()
        if len(name) >= 2:
            current_user = name
            show_level_selection()
        else:
            messagebox.showwarning("Ошибка", "Имя должно содержать минимум 2 символа!")

    tk.Button(container, text="🎯 ДАЛЕЕ →", font=("Arial", 14, "bold"), bg=theme["accent"],
              fg='white', width=20, height=2, command=save_name).pack(pady=30)
              
    tk.Button(container, text="← В МЕНЮ", font=("Arial", 12), bg='#95a5a6', 
              fg='white', width=15, command=show_main_menu).pack(pady=10)

def show_level_selection():
    """Экран выбора сложности"""
    clear_window()
    theme = themes[settings["theme"]]
    container = tk.Frame(root, bg=theme["bg"])
    container.pack(expand=True)
    
    tk.Label(container, text=f"Привет, {current_user}! Выберите уровень сложности:", 
             font=("Arial", 24, "bold"), bg=theme["bg"], fg=theme["accent"]).pack(pady=30)

    levels = {
        "легкий": ("✅ Легкий (Базовые факты)", "#2ecc71"),
        "средний": ("🧠 Средний (История и техники)", "#f39c12"),
        "сложный": ("🧐 Сложный (Детали и архитектура)", "#e74c3c"),
        "эксперт": ("👑 Эксперт (Авангард и школы)", "#9b59b6"),
    }
    
    for key, (text, color) in levels.items():
        tk.Button(container, text=text, font=("Arial", 14, "bold"), bg=color, fg='white',
                  width=30, height=2, command=lambda k=key: start_game(k)).pack(pady=10)

    tk.Button(container, text="← В МЕНЮ", font=("Arial", 12), bg='#95a5a6', 
              fg='white', width=15, command=show_main_menu).pack(pady=30)

def show_settings():
    """Экран настроек (темы и т.д.)"""
    global temp_theme_setting
    clear_window()
    theme = themes[settings["theme"]]
    root.configure(bg=theme["bg"])
    
    container = tk.Frame(root, bg=theme["bg"], padx=40, pady=40)
    container.pack(expand=True)
    
    tk.Label(container, text="⚙️ НАСТРОЙКИ ИГРЫ", font=("Arial", 24, "bold"),
             bg=theme["bg"], fg=theme["accent"]).grid(row=0, column=0, columnspan=2, pady=30)

    # --- Настройка темы ---
    
    tk.Label(container, text="Визуальная тема:", font=("Arial", 16), 
             bg=theme["bg"], fg=theme["text_color"]).grid(row=1, column=0, sticky='w', padx=10, pady=10)
    
    theme_var = tk.StringVar(root)
    theme_var.set(settings["theme"])
    temp_theme_setting = settings["theme"] # Запоминаем текущее значение
    
    def on_theme_change(new_theme):
        global temp_theme_setting
        temp_theme_setting = new_theme # Обновляем временную переменную

    theme_combo = ttk.Combobox(container, textvariable=theme_var, values=list(themes.keys()), 
                               font=("Arial", 14), state="readonly", width=15)
    theme_combo.bind("<<ComboboxSelected>>", lambda event: on_theme_change(theme_var.get()))
    theme_combo.grid(row=1, column=1, sticky='e', padx=10, pady=10)

    def save_settings():
        global settings
        settings["theme"] = temp_theme_setting
        apply_theme()
        messagebox.showinfo("Настройки", "Настройки сохранены! Тема применена.")
        show_main_menu()
        
    def preview_theme():
        global settings
        current_theme = settings["theme"] # Сохраняем текущую
        settings["theme"] = temp_theme_setting # Применяем временную
        apply_theme() # Применяем
        settings["theme"] = current_theme # Возвращаем старую (чтобы при выходе тема не слетела, если не нажато "Сохранить")
        
    tk.Button(container, text="✅ СОХРАНИТЬ", font=("Arial", 14, "bold"), bg="#27ae60", 
              fg='white', width=15, command=save_settings).grid(row=3, column=0, padx=10, pady=30)
              
    tk.Button(container, text="🎨 ПРЕДПРОСМОТР", font=("Arial", 14), bg="#3498db", 
              fg='white', width=15, command=preview_theme).grid(row=3, column=1, padx=10, pady=30)

    tk.Button(container, text="← НАЗАД В МЕНЮ", font=("Arial", 12), bg='#95a5a6', 
              fg='white', width=15, command=show_main_menu).grid(row=4, column=0, columnspan=2, pady=10)
              
def show_statistics():
    """Показывает таблицу рекордов"""
    clear_window()
    theme = themes[settings["theme"]]
    root.configure(bg=theme["bg"])

    tk.Label(root, text="📊 ТОП-10 РЕКОРДОВ 📊", font=("Arial", 28, "bold"),
             bg=theme["bg"], fg=theme["accent"]).pack(pady=30)

    # Убедимся, что рекорды загружены
    load_records() 

    if not all_records:
        tk.Label(root, text="Список рекордов пуст. Начните игру, чтобы увидеть рекорды!", font=("Arial", 14),
                 bg=theme["bg"], fg=theme["text_color"]).pack(pady=20)
    else:
        # --- Таблица ---
        table_frame = tk.Frame(root, bg=theme["card_bg"], padx=10, pady=10, bd=2, relief='sunken')
        table_frame.pack(padx=50, pady=10)

        headers = ["#", "Игрок", "Уровень", "Счет", "Правильно", "Время (сек)"]
        
        # Заголовки
        for j, header in enumerate(headers):
            tk.Label(table_frame, text=header, font=("Arial", 11, "bold"), bg=theme["header_bg"], fg='white', width=12, bd=1, relief='solid').grid(row=0, column=j, sticky='nsew', padx=1, pady=1)

        row_index = 1
        
        for i, record in enumerate(all_records):
            try:
                # Безопасный доступ к полям через .get() для избежания KeyError
                user = record.get('user', 'Неизвестно')
                difficulty_key = record.get('difficulty', 'Неизвестно').lower()
                
                total_q = record.get('total_questions')
                if total_q is None:
                    # Рекорд старый, берем из базы, защищаемся от KeyError: 'difficulty'
                    total_q = len(questions_db.get(difficulty_key, []))
                
                score_val = record.get('score', 0)
                correct_val = record.get('correct', 0)
                time_val = record.get('time', 0)
                
                # Форматирование правильных ответов
                correct_str = f"{correct_val}/{total_q}" if total_q > 0 else str(correct_val)
                
                row_data = [
                    str(i + 1),
                    user,
                    record.get('difficulty', '???'), 
                    str(score_val),
                    correct_str, 
                    str(time_val)
                ]
                
                # Создание строки таблицы
                row_color = theme["card_bg"] if i % 2 == 0 else theme["header_bg"]
                text_color = theme["text_color"] if i % 2 == 0 else 'white'

                for j, data in enumerate(row_data):
                    tk.Label(table_frame, text=data, font=("Arial", 10), bg=row_color, fg=text_color, width=12, bd=1, relief='flat').grid(row=row_index, column=j, sticky='nsew', padx=1, pady=1)
                
                row_index += 1
                
            except Exception as e:
                # Пропускаем сильно поврежденные записи
                print(f"Отладка: Пропущена поврежденная запись рекорда: {e}")
                continue 

    # --- КНОПКА НАЗАД (Гарантированный выход) ---
    tk.Button(root, text="← НАЗАД В МЕНЮ", font=("Arial", 12), bg='#95a5a6', 
              fg='white', command=show_main_menu).pack(pady=30)

def show_about():
    """Показывает информацию об игре."""
    clear_window()
    theme = themes[settings["theme"]]
    root.configure(bg=theme["bg"])
    
    container = tk.Frame(root, bg=theme["bg"], padx=50, pady=50)
    container.pack(expand=True)
    
    tk.Label(container, text="ℹ️ ОБ ИГРЕ: 'ШЕДЕВРЫ РУССКОГО ИСКУССТВА' 🏛️", 
             font=("Arial", 20, "bold"), bg=theme["bg"], fg=theme["accent"]).pack(pady=20)
             
    info_text = (
        "Это образовательная викторина, созданная для изучения ключевых памятников и направлений "
        "древнерусского искусства, иконописи, а также русского авангарда.\n\n"
        "Правильные ответы добавляют очки и показывают интересный факт.\n\n"
        "Удачи в изучении шедевров!"
    )
    
    tk.Label(container, text=info_text, font=("Arial", 12), bg=theme["bg"], fg=theme["text_color"], 
             justify='center', wraplength=700).pack(pady=10)
             
    tk.Button(container, text="← НАЗАД В МЕНЮ", font=("Arial", 12), bg='#95a5a6', 
              fg='white', command=show_main_menu).pack(pady=30)
              
# --- 7. ЗАПУСК ПРОГРАММЫ ---

if __name__ == "__main__":
    try:
        load_records() # Загружаем рекорды при старте
        apply_theme() # Применяем сохраненную тему
        show_main_menu() # Показываем главное меню
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Критическая ошибка", f"Произошла критическая ошибка при запуске: {e}")
        print(f"Критическая ошибка: {e}")
