from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QTextBrowser

class ResultsDialog(QDialog):
    def __init__(self, db_manager, encryption_manager):
        super().__init__()
        self.db_manager = db_manager
        self.encryption_manager = encryption_manager
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Результаты голосования")
        layout = QVBoxLayout(self)

        self.results_browser = QTextBrowser()
        layout.addWidget(self.results_browser)

        self.load_results()

    def load_results(self):
        votes = self.db_manager.get_votes()
        results = self.process_votes(votes)
        self.display_results(results)

    def process_votes(self, votes):
        city_results = {}
        state_results = {}
        national_results = {"Republican": 0, "Democrat": 0}
        invalid_votes = 0

        for vote in votes:
            vote_id, _, encrypted_choice, _, city_name, state_name = vote

            # Проверка действительности голоса с помощью ZKP
            if not self.db_manager.verify_vote(vote_id):
                invalid_votes += 1
                continue

            choice = self.encryption_manager.decrypt(encrypted_choice)

            if city_name not in city_results:
                city_results[city_name] = {"Republican": 0, "Democrat": 0}
            city_results[city_name][choice] += 1

            if state_name not in state_results:
                state_results[state_name] = {"Republican": 0, "Democrat": 0}

        for city, results in city_results.items():
            state_name = next(state for _, _, _, c, state in votes if c == city)
            winner = max(results, key=results.get)
            if winner:
                state_results[state_name][winner] += 1

        for state, results in state_results.items():
            winner = max(results, key=results.get)
            if winner:
                national_results[winner] += 1

        return {
            "city_results": city_results,
            "state_results": state_results,
            "national_results": national_results,
            "invalid_votes": invalid_votes
        }

    def determine_winner(self, results):
        if results["Republican"] > results["Democrat"]:
            return "Republican"
        elif results["Democrat"] > results["Republican"]:
            return "Democrat"
        else:
            return None  # Ничья

    def display_results(self, results):
        output = "Результаты голосования:\n\n"

        output += "Результаты по городам:\n"
        for city, city_result in results["city_results"].items():
            winner = self.determine_winner(city_result)
            output += f"{city}: Республиканцы - {city_result['Republican']}, Демократы - {city_result['Democrat']}\n"
            output += f" (Победитель: {winner if winner else 'Ничья'})\n"

        output += "\nРезультаты по штатам:\n"
        for state, state_result in results["state_results"].items():
            winner = self.determine_winner(state_result)
            output += f"{state}: Республиканцы - {state_result['Republican']}, Демократы - {state_result['Democrat']}\n"
            output += f" (Победитель: {winner if winner else 'Ничья'})\n"

        output += "\nОбщенациональные результаты:\n"
        national = results["national_results"]
        output += f"Республиканцы: {national['Republican']} штатов\n"
        output += f"Демократы: {national['Democrat']} штатов\n"

        winner = self.determine_winner(national)
        if winner:
            output += f"\nИтоговый победитель: {winner}"
        else:
            output += "\nИтоговый результат: Ничья"
        # winner = max(national, key=national.get)
        # output += f"\nПобедитель: {'Республиканцы' if winner == 'Republican' else 'Демократы'}"

        output += f"\nInvalid votes (failed ZKP verification): {results['invalid_votes']}"

        self.results_browser.setText(output)