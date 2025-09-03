class AdvancedQueries:
    """Advanced SQL queries for dashboard analytics"""
    
    @staticmethod
    def get_user_lifecycle_metrics():
        """Get comprehensive user lifecycle metrics"""
        return """
        WITH user_lifecycle AS (
            SELECT 
                user_id,
                MIN(date) as first_session,
                MAX(date) as last_session,
                COUNT(DISTINCT date) as active_days,
                COUNT(*) as total_sessions,
                AVG(time_spent) as avg_session_duration,
                SUM(CASE WHEN lesson_completed THEN 1 ELSE 0 END) as lessons_completed,
                MAX(CASE WHEN subscription_type = 'premium' THEN 1 ELSE 0 END) as became_premium,
                EXTRACT(DAYS FROM (MAX(date) - MIN(date))) + 1 as lifecycle_days
            FROM activity
            GROUP BY user_id
        ),
        lifecycle_segments AS (
            SELECT 
                *,
                CASE 
                    WHEN active_days = 1 THEN 'One-time'
                    WHEN active_days <= 7 AND lifecycle_days <= 14 THEN 'New'
                    WHEN last_session >= CURRENT_DATE - INTERVAL '7 days' THEN 'Active'
                    WHEN last_session >= CURRENT_DATE - INTERVAL '30 days' THEN 'At Risk'
                    ELSE 'Churned'
                END as lifecycle_stage
            FROM user_lifecycle
        )
        SELECT 
            lifecycle_stage,
            COUNT(*) as users,
            AVG(total_sessions) as avg_sessions,
            AVG(avg_session_duration) as avg_duration,
            AVG(lessons_completed) as avg_lessons,
            SUM(became_premium) * 100.0 / COUNT(*) as conversion_rate
        FROM lifecycle_segments
        GROUP BY lifecycle_stage
        ORDER BY 
            CASE lifecycle_stage
                WHEN 'New' THEN 1
                WHEN 'Active' THEN 2
                WHEN 'At Risk' THEN 3
                WHEN 'Churned' THEN 4
                WHEN 'One-time' THEN 5
            END;
        """
    
    @staticmethod
    def get_course_performance_metrics():
        """Get detailed course performance analytics"""
        return """
        WITH course_metrics AS (
            SELECT 
                course_id,
                COUNT(DISTINCT user_id) as total_users,
                COUNT(*) as total_sessions,
                AVG(time_spent) as avg_session_duration,
                SUM(CASE WHEN lesson_completed THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as completion_rate,
                COUNT(DISTINCT CASE WHEN subscription_type = 'premium' THEN user_id END) * 100.0 / 
                    COUNT(DISTINCT user_id) as premium_conversion_rate
            FROM activity
            WHERE date >= CURRENT_DATE - INTERVAL '30 days'
            GROUP BY course_id
        )
        SELECT 
            cm.*,
            c.course_name,
            c.difficulty_level,
            c.category
        FROM course_metrics cm
        LEFT JOIN courses c ON cm.course_id = c.course_id
        ORDER BY total_users DESC;
        """