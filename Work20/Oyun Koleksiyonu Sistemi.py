import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox
from PyQt5.QtGui import QLinearGradient
import random

class Game:
    def __init__(self, name, genre, platform):
        self.name = name
        self.genre = genre
        self.platform = platform
        self.ratings = []

    def __str__(self):
        if self.ratings:
            avg_rating = sum(self.ratings) / len(self.ratings)
        else:
            avg_rating = "N/A"
        return f"{self.name} - {self.genre} - {self.platform} - Değerlendirme: {avg_rating}"

    def add_rating(self, rating):
        self.ratings.append(rating)

class Collection:
    def __init__(self):
        self.games = []

    def add_game(self, game):
        self.games.append(game)

    def __str__(self):
        return '\n'.join(str(game) for game in self.games)

class Player:
    def __init__(self, name):
        self.name = name
        self.collection = Collection()

class GameCollectionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Video Game Collection Manager')
        self.setGeometry(600, 180, 600, 400)

        self.player = None

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.player_name_label = QLabel("Oyuncu Adı:")
        self.player_name_edit = QLineEdit()
        layout.addWidget(self.player_name_label)
        layout.addWidget(self.player_name_edit)

        self.create_player_button = QPushButton("Oyuncu Oluştur")
        self.create_player_button.setStyleSheet("background-color: #4CAF50; color: white; border: none; padding: 10px;")

        self.create_player_button.clicked.connect(self.create_player)
        layout.addWidget(self.create_player_button)

        self.game_name_label = QLabel("Oyun Adı:")
        self.game_name_edit = QLineEdit()
        layout.addWidget(self.game_name_label)
        layout.addWidget(self.game_name_edit)

        self.game_genre_label = QLabel("Oyun Türü:")
        self.game_genre_edit = QLineEdit()
        layout.addWidget(self.game_genre_label)
        layout.addWidget(self.game_genre_edit)

        self.game_platform_label = QLabel("Oyun Platformu:")
        self.game_platform_edit = QLineEdit()
        layout.addWidget(self.game_platform_label)
        layout.addWidget(self.game_platform_edit)

        self.add_game_button = QPushButton("Oyun Ekle")
        self.add_game_button.setStyleSheet("background-color: #4CAF50; color: white; border: none; padding: 10px;")
        self.add_game_button.clicked.connect(self.add_game)
        layout.addWidget(self.add_game_button)

        self.rating_label = QLabel("Oyun Değerlendirme (1-10):")
        self.rating_edit = QLineEdit()
        layout.addWidget(self.rating_label)
        layout.addWidget(self.rating_edit)

        self.rate_game_button = QPushButton("Oyun Değerlendir")
        self.rate_game_button.setStyleSheet("background-color: #c63943; color: white; border: none; padding: 10px;")
        self.rate_game_button.clicked.connect(self.rate_game)
        layout.addWidget(self.rate_game_button)

        self.collection_label = QLabel("Koleksiyon:")
        layout.addWidget(self.collection_label)

        self.collection_list = QListWidget()
        layout.addWidget(self.collection_list)

        self.favorite_game_label = QLabel("Favori Oyun:")
        layout.addWidget(self.favorite_game_label)

        self.favorite_game_list = QListWidget()
        layout.addWidget(self.favorite_game_list)

        self.select_favorite_button = QPushButton("Favori Oyunu Seç")
        self.select_favorite_button.setStyleSheet("background-color: #c63989; color: white; border: none; padding: 10px;")
        self.select_favorite_button.clicked.connect(self.select_favorite_game)
        layout.addWidget(self.select_favorite_button)

        self.get_recommendation_button = QPushButton("Öneri Al")
        self.get_recommendation_button.setStyleSheet("background-color: #c67639; color: white; border: none; padding: 10px;")
        self.get_recommendation_button.clicked.connect(self.get_recommendation)
        layout.addWidget(self.get_recommendation_button)

        self.help_button = QPushButton("Kılavuz")
        self.help_button.setStyleSheet("background-color: #c67639; color: white; border: none; padding: 10px;")
        self.help_button.clicked.connect(self.show_guide)
        layout.addWidget(self.help_button)

        self.setLayout(layout)

    def create_player(self):
        player_name = self.player_name_edit.text()
        if player_name:
            self.player = Player(player_name)
            QMessageBox.information(self, "Bilgi", f"{player_name} adında bir oyuncu oluşturuldu.")
            self.add_default_games()  # Oyuncu oluşturulduktan sonra varsayılan oyunları ekle
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir oyuncu adı girin.")

    def add_game(self):
        if not self.player:
            QMessageBox.warning(self, "Uyarı", "Lütfen önce bir oyuncu oluşturun.")
            return

        game_name = self.game_name_edit.text()
        game_genre = self.game_genre_edit.text()
        game_platform = self.game_platform_edit.text()

        if game_name and game_genre and game_platform:
            game = Game(game_name, game_genre, game_platform)
            self.player.collection.add_game(game)
            self.update_collection_list()
            QMessageBox.information(self, "Bilgi", f"{game_name} adlı oyun koleksiyona eklendi.")
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen tüm oyun bilgilerini girin.")

    def update_collection_list(self):
        self.collection_list.clear()
        if self.player:
            self.collection_list.addItems(str(game) for game in self.player.collection.games)

    def add_default_games(self):
        default_games = [
            ("The Legend of Zelda", "Action-Adventure", "Nintendo Switch"),
            ("Final Fantasy VII", "RPG", "PlayStation 4"),
            ("Super Mario Odyssey", "Platformer", "Nintendo Switch"),
            ("Red Dead Redemption 2", "Action-Adventure", "PlayStation 4"),
            ("The Witcher 3: Wild Hunt", "RPG", "PC"),
            ("Breath of the Wild", "Action-Adventure", "Nintendo Switch"),
            ("Persona 5", "RPG", "PlayStation 4"),
            ("God of War", "Action-Adventure", "PlayStation 4"),
            ("Hollow Knight", "Metroidvania", "PC"),
            ("Celeste", "Platformer", "PC")
        ]
        for game_info in default_games:
            game = Game(*game_info)
            game.add_rating(random.randint(1, 10))  # Rastgele bir değerlendirme puanı ekle
            self.player.collection.add_game(game)
        self.update_collection_list()

    def rate_game(self):
        if not self.player:
            QMessageBox.warning(self, "Uyarı", "Lütfen önce bir oyuncu oluşturun.")
            return

        game_name = self.game_name_edit.text()
        rating_text = self.rating_edit.text()

        if not rating_text.isdigit() or not (1 <= int(rating_text) <= 10):
            QMessageBox.warning(self, "Uyarı", "Lütfen geçerli bir değerlendirme girin (1-10 arası).")
            return

        if not game_name:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir oyun adı girin.")
            return

        for game in self.player.collection.games:
            if game.name == game_name:
                game.add_rating(int(rating_text))
                QMessageBox.information(self, "Bilgi", f"{game_name} adlı oyunu değerlendirme eklendi.")
                self.update_collection_list()  # Oyun değerlendirildikten sonra koleksiyon listesini güncelle
                return

        QMessageBox.warning(self, "Uyarı", f"{game_name} adlı bir oyun koleksiyonda bulunamadı.")

    def select_favorite_game(self):
        selected_items = self.collection_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir oyun seçin.")
            return

        selected_game = selected_items[0].text()
        self.favorite_game_list.addItem(selected_game)
        QMessageBox.information(self, "Bilgi", f"{selected_game} favori oyun olarak seçildi.")

    def get_recommendation(self):
        if not self.player:
            QMessageBox.warning(self, "Uyarı", "Lütfen önce bir oyuncu oluşturun.")
            return

        if not self.player.collection.games:
            QMessageBox.warning(self, "Uyarı", "Koleksiyon boş. Öneri almak için en az bir oyun ekleyin.")
            return

        recommended_game = random.choice(self.player.collection.games)
        QMessageBox.information(self, "Öneri", f"{recommended_game.name} oyununu deneyin!")

    def show_guide(self):
        guide_text = """
        Kılavuz:

        - "Oyuncu Adı" alanına bir oyuncu adı girin ve "Oyuncu Oluştur" düğmesine tıklayarak bir oyuncu oluşturun.
        - Oyuncu oluşturduktan sonra, "Oyun Adı", "Oyun Türü" ve "Oyun Platformu" alanlarına oyun bilgilerini girin ve "Oyun Ekle" düğmesine tıklayarak bir oyun ekleyin.
        - Koleksiyondaki her oyunun yanında, oyunun adı, türü, platformu ve ortalama değerlendirme puanı bulunmaktadır.
        - Bir oyunu değerlendirmek için, "Oyun Adı" ve "Oyun Değerlendirme" (1-10 arası bir sayı) alanlarını doldurun ve "Oyun Değerlendir" düğmesine tıklayın.
        - Favori oyununuzu seçmek için, koleksiyondan bir oyunu seçin ve "Favori Oyunu Seç" düğmesine tıklayın.
        - "Öneri Al" düğmesine tıklayarak, koleksiyondaki oyunlardan rastgele bir öneri alın.
        """
        QMessageBox.information(self, "Kılavuz", guide_text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GameCollectionApp()
    window.show()
    sys.exit(app.exec_())
