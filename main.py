from ClassWorldCupSimulator import WorldCupSimulator
 
def main():
    simulator = WorldCupSimulator()
    while True:
        print("\n================ World Cup Simulator ==========================")
        print("1) Loading teams from CSV file")
        print("2) Draw groups (Seed Automatic)")
        print("3) Run Group Stages and display tables")
        print("4) Run tournament (group and knockout stage) and show champion")
        print("5) 1000 simulation and championship probability report")
        print("6) Display Bracket of Last Simulation")
        print("7) Exit")
        print("===============================================================")

        # مدیریت خطای ورودی عدد بین 1 تا 7
        try:
            choice = int(input("Select an option (1-7): "))
        except ValueError:
            print("Invalid choice. Please enter a number.")
            continue

        if choice == 1:
            simulator.load_teams_from_csv("worldcup_2026_teams.csv")

        elif choice == 2:
            # بررسی وجود تیم ها یعنی خوانده شدن فایل
            if not simulator.teams:
                print("Error: Make sure teams have been loaded in Option 1 first!")
                continue  # بازگشت به ابتدای حلقه و جلوگیری از کرش
            simulator.seed_and_draw_groups()
            print("Groups have been drawn successfully (Seed Automatic)!")

        elif choice == 3:
            # با مطمئن شدن از وجود گروه ها یعنی قرعه کشی انجام شده
            if not simulator.groups:
                print("Error: Perform group draw using Option 2 first!")
                continue
                
            simulator.run_group_stage()
            
            # چاپ جدول رده‌بندی هر گروه
            print("\n----- GROUP STAGE TABLES -----")
            for group in simulator.groups:
                print(f"\nGroup {group.group_name}:")
                print(f"{"Team":<15} | {"Pts":<3} | {"GD":<3} | {"GF":<3} | {"GA":<3}")
                print("-" * 35)
                ranked_teams = group.get_ranking()
                for team in ranked_teams:
                    print(f"{team.name:<15} | {team.points:<3} | {team.goal_difference():<3} | {team.goals_for:<3} | {team.goals_against:<3}")

        elif choice == 4:
            if not simulator.teams:
                print("Error: Make sure teams have been loaded in Option 1 first!")
                continue  
                
            print("\nStarting full tournament simulation...")
            simulator.run_full_simulation(show_results=True)
            
        elif choice == 5:
            if not simulator.teams:
                print("Error: Make sure teams have been loaded in Option 1 first!")
                continue
            # تعداد شبیه سازی را میگیرد در صورت وارد نکردن 1000 باره انجام میشود
            user_input = input("Enter number of simulations (Press Enter for default 1000): ").strip()
            if user_input == "":
                sim_count = 1000
            else:
                try:
                    sim_count = int(user_input)
                except ValueError:
                    print("Invalid input! Using default 1000 simulations.")
                    sim_count = 1000

            print(f"\nRunning {sim_count} simulations, please wait...")
            simulator.most_likely_champion(num_simulations=sim_count)

        elif choice == 6:  
            simulator.display_bracket()

        elif choice == 7:  
            print("Exiting simulator. Good luck with the World Cup!")
            break
            
        else:
            print("Invalid choice. Please choose a number between 1 and 7.")

if __name__ == "__main__":
    main()



