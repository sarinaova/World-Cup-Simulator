import numpy as np 
import random as r

class Team():
    """ کلاس معرفی تیم ملی فوتبال و شبیه‌سازی مسابقات آن """
    def __init__(self, name, attack, defense, rank):
        self.name = name
        self.attack = attack
        self.defense = defense
        self.rank = rank 

        self.goals_for = 0
        self.goals_against = 0
        self.points = 0
        self.group = None
        
    def goal_difference(self):
        """ برگرداندن تفاضل گل تیم """
        return self.goals_for - self.goals_against

    def reset_stats(self):
        """ صفر کردن آمار تیم برای شبیه‌سازی جدید """
        self.goals_for = 0
        self.goals_against = 0
        self.points = 0

    def simulate_match(self, opponent, is_knockout=False):
        """شبیه‌سازی نتیجه بازی با تیم حریف.
        
        Args:
            opponent (Team): تیم حریف
            is_knockout (bool): آیا مرحله حذفی است؟
            
        Returns: goals_self, goals_opponent, winner, (self_score, opponent_score)

        """
        # 90 دقیقه بازی
        lambda_self = (self.attack / 100) * 1.5 + (1 - opponent.defense / 100) * 0.8
        lambda_opponent = (opponent.attack / 100) * 1.5 + (1 - self.defense / 100) * 0.8

        goals_self = np.random.poisson(lam= max(0.1, lambda_self))
        goals_opponent = np.random.poisson(lam= max(0.1, lambda_opponent))

        if goals_self != goals_opponent:
            winner = self if goals_self > goals_opponent else opponent
            return goals_self, goals_opponent, winner, None

        # در صورت گروهی بودن حتی با نتیجه مساوی برگردان
        if not is_knockout:
            return goals_self, goals_opponent, None, None
        
        # وقت اضافه برای مساوی شدن در مرحله حذفی
        extra_self = np.random.poisson(lam=lambda_self * 0.33)
        extra_opponent = np.random.poisson(lam=lambda_opponent * 0.33)
        goals_self += extra_self
        goals_opponent += extra_opponent

        # اگر بعد از وقت اضافه برنده مشخص شد
        if goals_self != goals_opponent:
            winner = self if goals_self > goals_opponent else opponent
            return goals_self, goals_opponent, winner, None

        # پنالتی
        def penalty(a, d):
            p = 0.75 + (a - d) / 250
            return max(0.6, min(0.9, p))
            
        p_self = penalty(self.attack, opponent.defense)
        p_opponent = penalty(opponent.attack, self.defense)
        self_score = 0
        opponent_score = 0

        # پنالتی 5
        for _ in range(5):
            if r.random() < p_self:
                self_score += 1
            if r.random() < p_opponent:
                opponent_score += 1

        # پنالتی ناگهانی
        if self_score == opponent_score:
            while True:
                s = r.random() < p_self
                o = r.random() < p_opponent
                if s: self_score += 1
                if o: opponent_score += 1
                if s != o:
                    break

        winner = self if self_score > opponent_score else opponent
        # بازگرداندن تعداد گل‌ها، برنده و نتیجۀ ضربات پنالتی
        return goals_self, goals_opponent, winner, (self_score, opponent_score)
