class KnockoutStage():
    """ کلاس مدیریت و برگزاری مسابقات در یکی از مراحل حذفی جام جهانی """
    def __init__(self, round_name, matches):
        self.round_name = round_name
        self.matches = matches
        
    def play_round(self):
        """ اجرای تمام مسابقات برنامه‌ریزی شده در این مرحله حذفی """
        for match in self.matches:
            match.play()

    def get_winners(self):
        """ برگرداندن لیست تیم‌های برنده صعود کرده به مرحله بعدی """
        return [match.winner for match in self.matches]
    
    def display_results(self):
        """چاپ خلاصه نتایج مرحله حذفی جاری به همراه نتایج پنالتی (در صورت وجود)."""
        print(f"\n===== {self.round_name} =====")
        for match in self.matches:
            # ساختن رشته مربوط به نتیجه گل‌ها
            score_str = f"{match.goals1} - {match.goals2}"
            
            #  بررسی اینکه آیا بازی به پنالتی کشیده شده است یا خیر
            if match.penalty_score:
                pens_self, pens_opp = match.penalty_score
                score_str += f" ({pens_self}-{pens_opp} pens)"
        
            print(f"{match.team1.name} {score_str} {match.team2.name} -> winner : {match.winner.name}")
