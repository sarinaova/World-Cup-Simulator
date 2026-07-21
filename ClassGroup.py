from ClassMatch import Match
import random as r

class Group():
    """ کلاس مدیریت مسابقات، رتبه‌بندی و تعیین تیم‌های صعودکننده هر گروه """
    def __init__(self, group_name, group_teams):
        self.group_name = group_name
        self.group_teams = group_teams
        self.matches = []   # ذخیره مسابقات برای بررسی بازی‌های مستقیم
        
    def play_all_matches(self):
        """ مسابقات گروهی که هر تیم یک بار با تیم های گروهش بازی میکند """
        self.matches = []
        for i in range(4):           
            for j in range(i+1, 4):
                m = Match(self.group_teams[i], self.group_teams[j])
                m.play()                                                 
                self.matches.append(m)
           
    def get_ranking(self):
        """رتبه‌بندی تیم‌های گروه بر اساس قوانین فیفا
        اولوبت 1.امتیاز 2.تفاضل گل 3.گل زده 4.بازی مستقیم 5.قرعه کشی تصادفی
        """
        teams_copy = list(self.group_teams)
        r.shuffle(teams_copy)
        
        ranked = sorted(
            teams_copy, 
            key=lambda t: (t.points, t.goal_difference(), t.goals_for), 
            reverse=True
        )
        # head to head
        for i in range(len(ranked) - 1):
            t1 = ranked[i]
            t2 = ranked[i + 1]
            
            # اگر دو تیم در تمام معیارهای اصلی کاملاً برابر بودند
            if (t1.points == t2.points and 
                t1.goal_difference() == t2.goal_difference() and 
                t1.goals_for == t2.goals_for):
                
                # پیدا کردن مسابقه بین این دو تیم
                # چون قطعا هر تیم با همه تیم های گروهش بازی کرده
                for match in self.matches:
                    if (match.team1 == t1 and match.team2 == t2) or (match.team1 == t2 and match.team2 == t1):
                        # اگر تیم دوم بازی مستقیم را برده باشد، جایشان را عوض کن
                        if match.winner == t2:
                            ranked[i], ranked[i + 1] = ranked[i + 1], ranked[i]
                        break
        return ranked
    
    def advance_teams(self):
        """برگرداندن دو تیم اول هر گروه """
        ranking = self.get_ranking()
        return ranking[0], ranking[1]
    
