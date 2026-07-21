class Match():
    """ کلاس مدیریت و برگزاری یک مسابقه فوتبال بین دو تیم مشخص """
    def __init__(self, team1, team2, is_knockout = False):
         self.team1 = team1
         self.team2 = team2
         self.is_knockout = is_knockout
         self.goals1 = 0
         self.goals2 = 0
         self.winner = None
         self.penalty_score = None

    def play(self):
        """ اجرای مسابقه، محاسبه و ثبت نتایج و آپدیت امتیازات و گل‌های تیم‌ها """
        g1, g2, winner, pens = self.team1.simulate_match(self.team2, self.is_knockout)
        self.goals1 = g1
        self.goals2 = g2
        self.winner = winner
        self.penalty_score = pens

        # آپدیدت آمار
        self.team1.goals_for += g1
        self.team1.goals_against += g2
        self.team2.goals_for += g2
        self.team2.goals_against += g1

        # امتیازدهی مرحله گروهی
        if not self.is_knockout:
            if g1 > g2:
                self.team1.points += 3
            elif g2 > g1:
                self.team2.points += 3
            else:
                self.team1.points += 1
                self.team2.points += 1
