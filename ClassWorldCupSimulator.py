import os
import csv
import random as r

from ClassTeam import Team
from ClassGroup import Group
from ClassMatch import Match
from ClassKnockoutStage import KnockoutStage

class WorldCupSimulator():
    """ کلاس اصلی مدیریت، برنامه ریزی و اجرای کامل مسابقات جام جهانی """
    def __init__(self):
        self.teams = []
        self.groups = []

        self.round_of_16 = None
        self.quarterfinals = None
        self.semifinals = None
        self.final = None
        self.champion = None

        self.last_bracket_data = {} # برای ذخیره براکت آخرین شبیه سازی 

    def load_teams_from_csv(self, filename):

        """ خواندن فایل 
        Arg: filename(string) اسم فایل
        Return: True or False """
         
        self.teams = []
        if not os.path.exists(filename):
            print(f"Error: File '{filename}' not found. Please place it in the project directory.")
            return False

        try:
            with open(filename, mode='r') as f:
                csv_read = csv.DictReader(f)
                for row in csv_read:
                    t = Team(row["name"], int(row["attack"]), int(row["defense"]), int(row["rank"]))
                    self.teams.append(t)
            print(f"Loading {len(self.teams)} teams from file was completed successfully!")
            return True
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            return False
                
    def seed_and_draw_groups(self):
        """ سیدبندی و قرعه کشی گروه  """

        # مرتب کردن تیم ها در لیست براساس رنک برای سید بندی بدون مشکل
        sorted_teams = sorted(self.teams, key=lambda t: t.rank)
        
        seed1 = sorted_teams[0:8]
        seed2 = sorted_teams[8:16]
        seed3 = sorted_teams[16:24]
        seed4 = sorted_teams[24:32]

        # قاطی کردن سیدها برای قرعه کشی گروه 
        r.shuffle(seed1)
        r.shuffle(seed2)
        r.shuffle(seed3)
        r.shuffle(seed4)

        # ایجاد گروه ها و ریختنشان در لیست گروه ها
        self.groups = []
        for i in range(8):
            g = Group(chr(ord("A") + i), [seed1[i], seed2[i], seed3[i], seed4[i]])
            for t in g.group_teams:  #اضافه شدن ویژگی گروه هر تیم برای آن تیم 
                t.group = g.group_name
            self.groups.append(g)
            
        
    def run_group_stage(self):
        """ اجرای مرحله گروهی """
        for group in self.groups:
            group.play_all_matches()
    
    def setup_knockout_bracket(self):
        """ ساخت براکت حذفی """
        leaders = []
        runners = []

        for group in self.groups:
            l, r = group.advance_teams()
            leaders.append(l)
            runners.append(r)

        matches = [
            Match(leaders[0], runners[1], True), # A1 vs B2
            Match(leaders[2], runners[3], True), # C1 vs D2
            Match(leaders[4], runners[5], True), # E1 vs F2
            Match(leaders[6], runners[7], True), # G1 vs H2
            Match(leaders[1], runners[0], True), # B1 vs A2
            Match(leaders[3], runners[2], True), # D1 vs C2
            Match(leaders[5], runners[4], True), # F1 vs E2
            Match(leaders[7], runners[6], True)  # H1 vs G2
        ]
        
        self.round_of_16 = KnockoutStage("Round of 16", matches)
         
    def run_knockout_stage(self):
        """ اجرای تمام مراحل حذفی تا فینال و مشخص کردن قهرمان"""
        # حذفی 16
        self.round_of_16.play_round()
        q = self.round_of_16.get_winners()

        # براکت 8 و اجرا
        # Quarterfinals
        q_matches = [Match(q[0], q[1], True),
                     Match(q[2], q[3], True),
                     Match(q[4], q[5], True),
                     Match(q[6], q[7], True)]
        
        self.quarterfinals = KnockoutStage("Quarterfinals", q_matches)
        self.quarterfinals.play_round()
        s = self.quarterfinals.get_winners()

        #براکت 4 و اجرا 
        # Semifinals
        s_matches = [Match(s[0], s[1], True),
                     Match(s[2], s[3], True)]
        
        self.semifinals = KnockoutStage("Semifinals", s_matches)
        self.semifinals.play_round()
        f = self.semifinals.get_winners()

        # Final
        f_matches = [Match(f[0], f[1], True)]
        self.final = KnockoutStage("Final", f_matches)
        self.final.play_round()

        self.champion = self.final.matches[0].winner

        # ذخیره آخرین اطلاعات براکت برای گزینه ۶ منو
        self.last_bracket_data = {
            'r16': self.round_of_16,
            'qf': self.quarterfinals,
            'sf': self.semifinals,
            'f': self.final
        }

    def run_full_simulation(self, show_results = False):

        """اجرای کامل یک دور تورنومنت
        Arg:
            show_results(bool): آیا نتایج نمایش داده شود؟
        """

        for t in self.teams:
            t.reset_stats()

        # اگر تا الان گروه بندی نشده بود انجام بشه
        if not self.groups:
            self.seed_and_draw_groups()

        self.run_group_stage()
        self.setup_knockout_bracket()
        self.run_knockout_stage()
        
        if show_results:
            self.display_bracket()

        return self.champion
        
    def most_likely_champion(self, num_simulations=1000):
        if num_simulations <= 0:
            print("Error: the number of simulations must be positive")
            return
        
        counter = {t.name: 0 for t in self.teams}

        for _ in range(num_simulations):
            self.seed_and_draw_groups()
            champ = self.run_full_simulation(show_results = False)
            counter[champ.name] += 1

        print(f"Team`s championship probabilities have been simulated {num_simulations} times")

        for name, count in counter.items():
            print(f"{name}: {count / num_simulations * 100: .2f}%")

    def display_bracket(self):
        """ نمایش براکت آخرین شبیه‌سازی حذفی انجام شده """
        # بررسی اینکه آیا براکتی از قبل ذخیره شده یا خیر
        if not self.last_bracket_data:
            if self.round_of_16: # اگر در شبیه‌سازی جاری وجود دارد اما ذخیره نشده
                self.round_of_16.display_results()
                self.quarterfinals.display_results()
                self.semifinals.display_results()
                self.final.display_results()
                print(f"\n🏆 World Cup Champion: {self.champion.name} 🏆")
            else:
                print("Simulation not happen")
            return

        # نمایش داده‌های ذخیره شده
        self.last_bracket_data['r16'].display_results()
        self.last_bracket_data['qf'].display_results()
        self.last_bracket_data['sf'].display_results()
        self.last_bracket_data['f'].display_results()
        print(f"\n🏆 World Cup Champion: {self.champion.name} 🏆")
