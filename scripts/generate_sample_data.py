import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import psycopg2
from dotenv import load_dotenv
import logging
from faker import Faker

load_dotenv()
fake = Faker()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_realistic_edtech_data(num_users=2000, num_days=90):
    """Генерирует реалистичные данные EdTech платформы"""
    
    data = []
    start_date = datetime.now() - timedelta(days=num_days)
    
    # Курсы с разной популярностью
    courses = [
        {'id': 'C101', 'name': 'Python Basics', 'popularity': 0.4},
        {'id': 'C102', 'name': 'Data Science', 'popularity': 0.3}, 
        {'id': 'C103', 'name': 'Machine Learning', 'popularity': 0.15},
        {'id': 'C104', 'name': 'Web Development', 'popularity': 0.1},
        {'id': 'C105', 'name': 'SQL Analytics', 'popularity': 0.05}
    ]
    
    # Устройства с разными характеристиками  
    devices = [
    {'type': 'mobile', 'probability': 0.6, 'avg_session_time': 25, 'completion_rate': 0.65},
    {'type': 'desktop', 'probability': 0.3, 'avg_session_time': 45, 'completion_rate': 0.85},
    {'type': 'tablet', 'probability': 0.1, 'avg_session_time': 35, 'completion_rate': 0.75}
]
    
    logger.info(f"Generating data for {num_users} users over {num_days} days...")
    
    for user_idx in range(1, num_users + 1):
        user_id = f"U{user_idx:04d}"
        
        # Дата регистрации пользователя
        signup_date = start_date + timedelta(days=np.random.randint(0, num_days-30))
        
        # Тип пользователя (влияет на поведение)
        user_type = np.random.choice(['engaged', 'casual', 'trial'], p=[0.2, 0.6, 0.2])
        
        # Выбор основного устройства
        device_probs = [d['probability'] for d in devices]
        primary_device = np.random.choice(devices, p=device_probs)
        
        # Конверсия в premium (зависит от активности)
        converts_to_premium = np.random.random() < (0.4 if user_type == 'engaged' else 0.1)
        conversion_day = np.random.randint(3, 30) if converts_to_premium else None
        
        # Генерация активности пользователя
        current_date = signup_date
        subscription_type = 'free'
        consecutive_inactive = 0
        
        # Параметры активности по типу пользователя
        activity_params = {
            'engaged': {'session_prob': 0.7, 'sessions_per_day': 2.5, 'retention_decay': 0.95},
            'casual': {'session_prob': 0.3, 'sessions_per_day': 1.2, 'retention_decay': 0.85}, 
            'trial': {'session_prob': 0.8, 'sessions_per_day': 3.0, 'retention_decay': 0.7}
        }
        
        params = activity_params[user_type]
        
        while current_date.date() <= datetime.now().date():
            # Проверка конверсии в premium
            if (conversion_day and 
                (current_date - signup_date).days >= conversion_day and 
                subscription_type == 'free'):
                subscription_type = 'premium'
            
            # Вероятность активности (уменьшается со временем)
            days_since_signup = (current_date - signup_date).days
            base_prob = params['session_prob'] * (params['retention_decay'] ** (days_since_signup / 7))
            
            # Снижение активности после периодов неактивности
            if consecutive_inactive > 0:
                base_prob *= (0.7 ** consecutive_inactive)
            
            # Решение об активности в этот день
            if np.random.random() < base_prob:
                consecutive_inactive = 0
                
                # Количество сессий в день
                num_sessions = max(1, int(np.random.poisson(params['sessions_per_day'])))
                
                for session in range(num_sessions):
                    # Выбор курса (с учетом популярности)
                    course_probs = [c['popularity'] for c in courses]
                    course = np.random.choice([c['id'] for c in courses], p=course_probs)
                    
                    # Выбор устройства (80% - основное, 20% - другое)
                    if np.random.random() < 0.8:
                        device = primary_device
                    else:
                        device = np.random.choice(devices)
                    
                    # Продолжительность сессии
                    base_time = device['avg_session_time']
                    if subscription_type == 'premium':
                        base_time *= 1.4  # Premium пользователи дольше занимаются
                    
                    time_spent = max(5, int(np.random.normal(base_time, base_time * 0.3)))
                    
                    # Завершение урока
                    completion_rate = device['completion_rate']
                    if subscription_type == 'premium':
                        completion_rate *= 1.2
                    if user_type == 'engaged':
                        completion_rate *= 1.1
                        
                    lesson_completed = np.random.random() < min(completion_rate, 0.95)
                    
                    # Добавление записи
                    data.append({
                        'date': current_date,
                        'user_id': user_id,
                        'course_id': course,
                        'lesson_completed': lesson_completed,
                        'time_spent': time_spent,
                        'device_type': device['type'],
                        'subscription_type': subscription_type
                    })
            else:
                consecutive_inactive += 1
                
                # Если неактивен больше 14 дней, прекращаем генерацию
                if consecutive_inactive > 14:
                    break
            
            current_date += timedelta(days=1)
        
        if user_idx % 500 == 0:
            logger.info(f"Generated data for {user_idx} users...")
    
    df = pd.DataFrame(data)
    logger.info(f"Generated {len(df)} activity records")
    return df

def save_to_database(df):
    """Сохранение данных в базу"""
    try:
        conn = psycopg2.connect(os.getenv('DB_URL'))
        cursor = conn.cursor()
        
        # Очистка старых данных
        cursor.execute("DELETE FROM activity")
        
        # Вставка новых данных
        for _, row in df.iterrows():
            cursor.execute("""
                INSERT INTO activity (date, user_id, course_id, lesson_completed, 
                                    time_spent, device_type, subscription_type)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, tuple(row))
        
        conn.commit()
        cursor.close()
        conn.close()
        logger.info(f"Successfully saved {len(df)} records to database")
        
    except Exception as e:
        logger.error(f"Error saving to database: {str(e)}")
        raise

def main():
    logger.info("Generating advanced sample data for dashboard...")
    
    # Генерация данных (2000 пользователей, 90 дней)
    df = generate_realistic_edtech_data(num_users=2000, num_days=90)
    
    # Сохранение в базу данных
    save_to_database(df)
    
    # Сохранение в CSV для резервной копии
    df.to_csv('data/advanced_sample_data.csv', index=False)
    
    logger.info("Advanced sample data generation completed!")
    logger.info("You can now launch the dashboard with: python dashboard/app.py")

if __name__ == "__main__":
    main()