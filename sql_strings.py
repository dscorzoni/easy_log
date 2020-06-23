# SQL queries used in log tool app.

def logs_per_day():
    strSQL = """
        SELECT 
            log_string AS log_string,
            COUNT(1) AS log_count
        FROM log
        GROUP BY 1
        ORDER BY log_count DESC
    """
    return strSQL

def time_spent():
    strSQL = """
        SELECT
            user_id,
            SUM(time_spent) AS time_spent
        FROM (
            SELECT 
                user_id,
                log_string AS event_now,
                created_at,
                lag(log_string) OVER (ORDER BY created_at) AS previous_event,
                lag(created_at) OVER (ORDER BY created_at) AS previous_created_at,
                strftime('%s', created_at) - strftime('%s', lag(created_at) OVER (ORDER BY created_at)) AS time_spent
            FROM log
            WHERE
                log_string IN ('load_page_index','exit_page_index')
            ORDER BY created_at
        )
        WHERE
            event_now = 'exit_page_index'
            AND previous_event = 'load_page_index'
        GROUP BY 1

    """
