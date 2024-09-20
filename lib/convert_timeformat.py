class ConvertTimeFormat:
    
    @staticmethod
    def convert_to_minutes_seconds_milliseconds(counter):
        # カウンタを1/60秒単位から秒単位に変換
        total_seconds = counter / 60
        
        # 分、秒、ミリ秒に変換
        minutes = int(total_seconds // 60)
        seconds = int(total_seconds % 60)
        milliseconds = int((total_seconds - int(total_seconds)) * 1000)
        
        return f"{minutes:02}:{seconds:02}.{milliseconds:03}"
